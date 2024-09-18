CREATE DATABASE "finapp-ms-inout";

CREATE USER "sa-finapp-ms-reports" WITH PASSWORD 'jw8s0F4';
CREATE USER "sa-finapp-ms-inout" WITH PASSWORD 'jw8s0F4';

REVOKE CONNECT ON DATABASE "finapp-ms-inout" FROM PUBLIC;

GRANT CONNECT
ON DATABASE "finapp-ms-inout" 
TO "sa-finapp-ms-inout";

GRANT CONNECT
ON DATABASE "finapp-ms-inout" 
TO "sa-finapp-ms-reports";

\connect "finapp-ms-inout"

CREATE TABLE expenses (
    id BIGSERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL,
    category INTEGER NOT NULL,
    value DECIMAL(10, 2) NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO expenses (description, category, value, month, year) 
VALUES 
    ('buying a new computer because the old one broke', 1, 2500, 9, 2024),
    ('buying a new computer because the old one broke', 1, 2500, 9, 2024),
    ('buying a new computer because the old one broke', 1, 2500, 9, 2024),
    ('buying a new computer because the old one broke', 1, 2500, 9, 2024),
    ('buying a new computer because the old one broke', 1, 2500, 9, 2024),
    ('buying a new computer because the old one broke', 1, 2500, 9, 2024),
    ('buying a new computer because the old one broke', 1, 2500, 9, 2024),
    ('buying a new computer because the old one broke', 1, 2500, 9, 2024);

REVOKE ALL
ON ALL TABLES IN SCHEMA public 
FROM PUBLIC;

GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA public 
TO "sa-finapp-ms-inout";

GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA public 
TO "sa-finapp-ms-reports";