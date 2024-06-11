CREATE TABLE application (
    timestamp String,
    full_name String,
    user_id String,
    email String,
    phone_number String,
    address String,
    date_of_birth String,
    gender String,
    event_description String
) ENGINE = MergeTree() ORDER BY timestamp;

