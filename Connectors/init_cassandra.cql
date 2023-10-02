CREATE KEYSPACE IF NOT EXISTS users
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE users;

CREATE TABLE IF NOT EXISTS accounts (
    id UUID PRIMARY KEY,
    name TEXT,
    password TEXT,
    flagged BOOLEAN
);

CREATE INDEX IF NOT EXISTS ON accounts (name);

INSERT INTO accounts (id, name, password, flagged)
VALUES (uuid(), 'Jack', '123456', false);

INSERT INTO accounts (id, name, password, flagged)
VALUES (uuid(), 'Tom', '123456', false);

INSERT INTO accounts (id, name, password, flagged)
VALUES (uuid(), 'Aaron', '123456', false);

INSERT INTO accounts (id, name, password, flagged)
VALUES (uuid(), 'Lucas', '123456', false);

INSERT INTO accounts (id, name, password, flagged)
VALUES (uuid(), 'Anna', '123456', false);






