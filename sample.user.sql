INSERT INTO Users
(
    UserName,
    Mobile,
    DOB,
    EMail,
    LoginID,
    [Password],
    UserRole,
    UserLocation,
    ClientID
)
VALUES
(
    N'Admin User',
    N'9876543210',
    '1985-01-15',
    N'admin@example.com',
    N'admin',
    CONVERT(varbinary(MAX), '$argon2id$v=19$m=65536,t=3,p=4$8u9HyJH4BPXV1/4Twh979w$GSpJ8po14Z2Fyv7+NmRcrurMXblP8k4Jm+Y2lM2IY0Q'),
    N'ADMIN',
    1,
    1
),
(
    N'Numbering User',
    N'9876543211',
    '1990-03-20',
    N'numbering@example.com',
    N'numbering',
    CONVERT(varbinary(MAX), '$argon2id$v=19$m=65536,t=3,p=4$EEHSiTSO1EDOMrxx6o/pMQ$XgltFMellJJbZHp9++8Wjw60+h+0FaauzGs5IYnPWDc'),
    N'NUMBERING',
    1,
    1
),
(
    N'Survey User',
    N'9876543212',
    '1992-07-10',
    N'survey@example.com',
    N'survey',
    CONVERT(varbinary(MAX), '$argon2id$v=19$m=65536,t=3,p=4$jM8RQ8WcRMmUDlhvC7z2kQ$FCDeYc0/ffX6VrUAIvuE01dFzO3IF9yUtxy3NF72/aQ'),
    N'SURVEY',
    1,
    1
),
(
    N'Tax User',
    N'9876543213',
    '1988-11-25',
    N'tax@example.com',
    N'tax',
    CONVERT(varbinary(MAX), '$argon2id$v=19$m=65536,t=3,p=4$nswN/IjDUODxuZWga6GJ2g$c1lGjsQ65zwetHlKNt3aPe+uOKZw1/QgrORs2VT63Ds'),
    N'TAX',
    1,
    1
);
