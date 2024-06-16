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

CREATE TABLE logs_services
(
    timestamp   datetime,
    service_name String,
    event       String,
    text        String,
    error       Bool
) ENGINE = MergeTree() ORDER BY timestamp;

ENTRYPOINT ["/entrypoint.sh"]
CMD ["clickhouse-server"]