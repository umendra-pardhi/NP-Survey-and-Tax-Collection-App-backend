#!/usr/bin/env python3

"""
Streaming SQL Server INSERT -> PostgreSQL INSERT converter.

Usage:
    python sqlserver_to_postgres.py input.sql output.sql

Features:
    - Streams large files; does not load the whole file into memory
    - Handles INSERT [dbo].[Accounts] (...) VALUES (...)
    - Handles N'Unicode strings'
    - Handles CAST(... AS Decimal(p,s))
    - Converts SQL Server 0/1 to TRUE/FALSE for boolean columns
    - Correctly handles commas inside strings
    - Correctly handles nested parentheses such as CAST(...)
    - Handles multiline INSERT statements
    - Handles SQL escaped quotes ('')
    - Maps [CTID] -> "CTID"
    - Maps [Length] -> "Length"
    - Reports bad records with their original SQL
"""

import re
import sys


# =========================================================
# PostgreSQL boolean columns
# =========================================================

BOOLEAN_COLUMNS = {
    "HasTenant",
    "HasToilet",
    "HasWaterConnection",
    "HasSolarElectricity",
    "HasRainWaterHarvesting",
    "HasTree",
    "HasGharkul",
    "HasBore",
    "HasWell",
    "AsmComplete",
    "HasTower",
    "ManualRatableValue",
    "ManualTax",
}


# PostgreSQL columns which were explicitly quoted
# in your CREATE TABLE.
#
# CREATE TABLE Accounts (
#     "CTID" integer,
#     ...
#     "Length" double precision
# )
# =========================================================

QUOTED_COLUMNS = {
    "CTID": '"CTID"',
    "Length": '"Length"',
}


# =========================================================
# Convert SQL Server identifier
# =========================================================

def convert_identifier(identifier: str) -> str:
    """
    SQL Server:
        [ACID]

    PostgreSQL:
        acid

    Special:
        [CTID]   -> "CTID"
        [Length] -> "Length"
    """

    identifier = identifier.strip()

    # Remove SQL Server brackets
    if identifier.startswith("[") and identifier.endswith("]"):
        identifier = identifier[1:-1]

    # Special case-sensitive PostgreSQL columns
    if identifier in QUOTED_COLUMNS:
        return QUOTED_COLUMNS[identifier]

    # PostgreSQL unquoted identifiers are lowercase
    return identifier.lower()


# =========================================================
# Convert table name
# =========================================================

def convert_table_name(table: str) -> str:
    """
    [dbo].[Accounts] -> accounts
    dbo.Accounts     -> accounts
    Accounts         -> accounts
    """

    table = table.strip()

    # Remove [] from each identifier
    parts = re.findall(r"\[([^\]]+)\]|([A-Za-z_][A-Za-z0-9_]*)", table)

    names = []

    for a, b in parts:
        name = a or b
        names.append(name)

    if not names:
        raise ValueError(f"Invalid table name: {table}")

    # Last part is the actual table name
    return names[-1].lower()


# =========================================================
# Find keyword outside SQL strings
# =========================================================

def find_keyword_outside_string(text: str, keyword: str, start: int = 0):
    """
    Find keyword such as VALUES outside a quoted SQL string.
    """

    keyword_upper = keyword.upper()

    in_string = False
    i = start

    while i < len(text):

        ch = text[i]

        if ch == "'":

            if in_string:

                # SQL escaped quote ''
                if i + 1 < len(text) and text[i + 1] == "'":
                    i += 2
                    continue

                in_string = False

            else:
                in_string = True

            i += 1
            continue

        if not in_string:

            if text[i:i + len(keyword)].upper() == keyword_upper:

                # Make sure this is a word boundary
                before_ok = (
                    i == 0 or not text[i - 1].isalnum()
                )

                after_pos = i + len(keyword)

                after_ok = (
                    after_pos >= len(text)
                    or not text[after_pos].isalnum()
                )

                if before_ok and after_ok:
                    return i

        i += 1

    return -1


# =========================================================
# Find matching closing parenthesis
# =========================================================

def find_matching_parenthesis(text: str, opening_pos: int):
    """
    Given the position of '(' find its matching ')'.

    Correctly handles:

        VALUES (
            CAST(0.00 AS Decimal(18,2)),
            'hello)'
        )

    """

    if text[opening_pos] != "(":
        raise ValueError("Expected '('")

    depth = 0
    in_string = False

    i = opening_pos

    while i < len(text):

        ch = text[i]

        if ch == "'":

            if in_string:

                # SQL escaped quote ''
                if i + 1 < len(text) and text[i + 1] == "'":
                    i += 2
                    continue

                in_string = False

            else:
                in_string = True

            i += 1
            continue

        if not in_string:

            if ch == "(":
                depth += 1

            elif ch == ")":

                depth -= 1

                if depth == 0:
                    return i

        i += 1

    raise ValueError(
        "Could not find matching ')' for VALUES"
    )


# =========================================================
# Split comma-separated SQL safely
# =========================================================

def split_sql_values(text: str):
    """
    Split:

        1, 'hello, world', CAST(1 AS Decimal(18,2)), NULL

    into:

        1
        'hello, world'
        CAST(1 AS Decimal(18,2))
        NULL

    Commas inside strings and parentheses are ignored.
    """

    values = []

    current = []

    in_string = False
    depth = 0

    i = 0

    while i < len(text):

        ch = text[i]

        # -------------------------------------------------
        # SQL string
        # -------------------------------------------------

        if ch == "'":

            current.append(ch)

            if in_string:

                # SQL escaped quote ''
                if i + 1 < len(text) and text[i + 1] == "'":

                    current.append("'")
                    i += 2
                    continue

                in_string = False

            else:
                in_string = True

            i += 1
            continue

        # -------------------------------------------------
        # Outside string
        # -------------------------------------------------

        if not in_string:

            if ch == "(":
                depth += 1

            elif ch == ")":
                depth -= 1

                if depth < 0:
                    raise ValueError(
                        "Unexpected closing parenthesis"
                    )

            elif ch == "," and depth == 0:

                values.append(
                    "".join(current).strip()
                )

                current = []

                i += 1
                continue

        current.append(ch)
        i += 1

    if current:
        values.append(
            "".join(current).strip()
        )

    return values


# =========================================================
# Convert SQL Server value
# =========================================================

def convert_value(value: str, column: str) -> str:

    value = value.strip()

    # -----------------------------------------------------
    # SQL Server Unicode string
    #
    # N'रामचंद्र'
    # ->
    # 'रामचंद्र'
    # -----------------------------------------------------

    if value.startswith(("N'", "n'")):
        value = value[1:]

    # -----------------------------------------------------
    # Normalize column name for comparisons.
    #
    # PostgreSQL column may already have been converted to:
    #
    #   hastenant
    #
    # while BOOLEAN_COLUMNS contains:
    #
    #   HasTenant
    #
    # So comparison must be case-insensitive.
    # -----------------------------------------------------

    normalized_column = column.strip(
        '[]"'
    ).lower()

    boolean_columns_lower = {
        name.lower()
        for name in BOOLEAN_COLUMNS
    }

    # -----------------------------------------------------
    # Convert SQL Server Decimal CAST
    #
    # CAST(0.00 AS Decimal(18, 2))
    # ->
    # 0.00::numeric(18,2)
    # -----------------------------------------------------

    decimal_cast = re.fullmatch(
        r"""
        CAST
        \s*\(
        \s*(.*?)
        \s+AS
        \s+DECIMAL
        \s*\(
        \s*(\d+)
        \s*,\s*
        (\d+)
        \s*\)
        \s*\)
        """,
        value,
        re.IGNORECASE | re.VERBOSE,
    )

    if decimal_cast:

        number = decimal_cast.group(1)
        precision = decimal_cast.group(2)
        scale = decimal_cast.group(3)

        return (
            f"{number}::numeric"
            f"({precision},{scale})"
        )

    # -----------------------------------------------------
    # Generic NUMERIC / DECIMAL CAST
    # -----------------------------------------------------

    value = re.sub(
        r"""
        CAST
        \s*\(
        \s*(.*?)
        \s+AS
        \s+(?:DECIMAL|NUMERIC)
        \s*\(
        \s*(\d+)
        \s*,\s*
        (\d+)
        \s*\)
        \s*\)
        """,
        lambda m:
            f"{m.group(1)}::numeric"
            f"({m.group(2)},{m.group(3)})",
        value,
        flags=re.IGNORECASE | re.VERBOSE,
    )

    # -----------------------------------------------------
    # SQL Server BIT -> PostgreSQL BOOLEAN
    #
    # IMPORTANT:
    # Only convert 0/1 for columns which are actually
    # boolean in the PostgreSQL table.
    # -----------------------------------------------------

    if normalized_column in boolean_columns_lower:

        if value == "0":
            return "FALSE"

        if value == "1":
            return "TRUE"

    return value


# =========================================================
# Parse one INSERT
# =========================================================

def convert_insert(sql: str) -> str:

    original = sql

    sql = sql.strip()

    # -----------------------------------------------------
    # Check INSERT
    # -----------------------------------------------------

    insert_match = re.match(
        r"INSERT\s+(.+?)\s*\(",
        sql,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if not insert_match:
        raise ValueError(
            "Statement does not start with INSERT"
        )

    table_text = insert_match.group(1).strip()

    table = convert_table_name(table_text)

    # -----------------------------------------------------
    # Find opening '(' of column list
    # -----------------------------------------------------

    columns_open = insert_match.end() - 1

    columns_close = find_matching_parenthesis(
        sql,
        columns_open,
    )

    columns_text = sql[
        columns_open + 1:
        columns_close
    ]

    # -----------------------------------------------------
    # Find VALUES
    # -----------------------------------------------------

    values_keyword = find_keyword_outside_string(
        sql,
        "VALUES",
        columns_close + 1,
    )

    if values_keyword == -1:
        raise ValueError(
            "VALUES keyword not found"
        )

    # -----------------------------------------------------
    # Find opening '(' after VALUES
    # -----------------------------------------------------

    values_open = sql.find(
        "(",
        values_keyword + len("VALUES"),
    )

    if values_open == -1:
        raise ValueError(
            "Opening '(' after VALUES not found"
        )

    # -----------------------------------------------------
    # Find matching ')' for VALUES
    # -----------------------------------------------------

    values_close = find_matching_parenthesis(
        sql,
        values_open,
    )

    values_text = sql[
        values_open + 1:
        values_close
    ]

    # -----------------------------------------------------
    # Parse columns
    # -----------------------------------------------------

    columns_raw = split_sql_values(
        columns_text
    )

    columns = [
        convert_identifier(column)
        for column in columns_raw
    ]

    # -----------------------------------------------------
    # Parse values
    # -----------------------------------------------------

    values = split_sql_values(
        values_text
    )

    # -----------------------------------------------------
    # Validate
    # -----------------------------------------------------

    if len(columns) != len(values):

        raise ValueError(
            f"Column/value count mismatch: "
            f"{len(columns)} columns vs "
            f"{len(values)} values"
        )

    # -----------------------------------------------------
    # Convert values
    # -----------------------------------------------------

    converted_values = []

    for column, value in zip(
        columns,
        values,
    ):

        converted_values.append(
            convert_value(
                value,
                column,
            )
        )

    # -----------------------------------------------------
    # Generate PostgreSQL SQL
    # -----------------------------------------------------

    return (
        f"INSERT INTO {table} ("
        + ", ".join(columns)
        + ") VALUES ("
        + ", ".join(converted_values)
        + ");"
    )


# =========================================================
# SQL statement accumulator
# =========================================================

def process_file(input_path: str, output_path: str):

    converted = 0
    failed = 0

    statement_lines = []

    # -----------------------------------------------------
    # Error file
    # -----------------------------------------------------

    error_path = output_path + ".errors"

    with open(
        input_path,
        "r",
        encoding="utf-8-sig",
        errors="replace",
    ) as infile, open(
        output_path,
        "w",
        encoding="utf-8",
        newline="\n",
    ) as outfile, open(
        error_path,
        "w",
        encoding="utf-8",
        newline="\n",
    ) as errorfile:

        for line_number, line in enumerate(
            infile,
            start=1,
        ):

            line = line.rstrip("\r\n")

            # -------------------------------------------------
            # Ignore empty lines
            # -------------------------------------------------

            if not line.strip():
                continue

            statement_lines.append(line)

            # -------------------------------------------------
            # Determine whether the current accumulated text
            # contains a complete INSERT.
            #
            # We don't simply look for ")" because CAST(...)
            # can contain ")" before the end of VALUES.
            # -------------------------------------------------

            statement = "\n".join(
                statement_lines
            ).strip()

            try:

                # If it looks like an INSERT and has VALUES,
                # attempt to parse it.
                if (
                    re.search(
                        r"\bVALUES\b",
                        statement,
                        re.IGNORECASE,
                    )
                    and re.match(
                        r"\s*INSERT\b",
                        statement,
                        re.IGNORECASE,
                    )
                ):

                    # -------------------------------------------------
                    # Try conversion.
                    #
                    # If the VALUES parenthesis is incomplete,
                    # keep collecting lines.
                    # -------------------------------------------------

                    converted_sql = convert_insert(
                        statement
                    )

                    outfile.write(
                        converted_sql
                        + "\n"
                    )

                    converted += 1

                    statement_lines.clear()

                    if converted % 10000 == 0:

                        print(
                            f"Converted: "
                            f"{converted:,}",
                            file=sys.stderr,
                        )

            except ValueError as exc:

                message = str(exc)

                # ---------------------------------------------
                # These errors may simply mean that the INSERT
                # continues on another line.
                # ---------------------------------------------

                incomplete_messages = (
                    "matching ')' for VALUES",
                    "Opening '(' after VALUES",
                    "VALUES keyword not found",
                )

                is_incomplete = any(
                    x in message
                    for x in incomplete_messages
                )

                if is_incomplete:
                    continue

                # ---------------------------------------------
                # Real error.
                # ---------------------------------------------

                failed += 1

                print(
                    f"ERROR near input line "
                    f"{line_number}: {message}",
                    file=sys.stderr,
                )

                errorfile.write(
                    f"-- ERROR near input line "
                    f"{line_number}: {message}\n"
                )

                errorfile.write(
                    statement
                )

                errorfile.write(
                    "\n\n"
                )

                statement_lines.clear()

        # -----------------------------------------------------
        # Anything left at EOF
        # -----------------------------------------------------

        if statement_lines:

            statement = "\n".join(
                statement_lines
            ).strip()

            if statement:

                failed += 1

                print(
                    "ERROR: incomplete SQL statement "
                    "at end of file",
                    file=sys.stderr,
                )

                errorfile.write(
                    "-- INCOMPLETE STATEMENT AT EOF\n"
                )

                errorfile.write(
                    statement
                )

                errorfile.write(
                    "\n\n"
                )

    print()
    print(
        f"Finished."
    )
    print(
        f"Converted : {converted:,}"
    )
    print(
        f"Failed    : {failed:,}"
    )
    print(
        f"Errors    : {error_path}"
    )


# =========================================================
# Main
# =========================================================

def main():

    if len(sys.argv) != 3:

        print(
            "Usage:"
        )

        print(
            "  python "
            "sqlserver_to_postgres.py "
            "input.sql output.sql"
        )

        print()

        print(
            "Example:"
        )

        print(
            "  python "
            "sqlserver_to_postgres.py "
            "accounts.sql "
            "accounts_pg.sql"
        )

        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    process_file(
        input_path,
        output_path,
    )


if __name__ == "__main__":
    main()
