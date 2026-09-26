INSERT INTO Users
(
    UserName,
    Mobile,
    DOB,
    EMail,
    LoginID,
    "Password",
    UserRole,
    UserLocation,
    ClientID
)
VALUES
(
    'Admin User',
    '9876543210',
    '1985-01-15',
    'admin@example.com',
    'admin',
    '$argon2id$v=19$m=65536,t=3,p=4$8u9HyJH4BPXV1/4Twh979w$GSpJ8po14Z2Fyv7+NmRcrurMXblP8k4Jm+Y2lM2IY0Q',
    'ADMIN',
    TRUE,
    1
),
(
    'Numbering User',
    '9876543211',
    '1990-03-20',
    'numbering@example.com',
    'numbering',
    '$argon2id$v=19$m=65536,t=3,p=4$EEHSiTSO1EDOMrxx6o/pMQ$XgltFMellJJbZHp9++8Wjw60+h+0FaauzGs5IYnPWDc',
    'NUMBERING',
    TRUE,
    1
),
(
    'Survey User',
    '9876543212',
    '1992-07-10',
    'survey@example.com',
    'survey',
    '$argon2id$v=19$m=65536,t=3,p=4$jM8RQ8WcRMmUDlhvC7z2kQ$FCDeYc0/ffX6VrUAIvuE01dFzO3IF9yUtxy3NF72/aQ',
    'SURVEY',
    TRUE,
    1
),
(
    'Tax User',
    '9876543213',
    '1988-11-25',
    'tax@example.com',
    'tax',
    '$argon2id$v=19$m=65536,t=3,p=4$nswN/IjDUODxuZWga6GJ2g$c1lGjsQ65zwetHlKNt3aPe+uOKZw1/QgrORs2VT63Ds',
    'TAX',
    TRUE,
    1
);
