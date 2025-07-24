-- Create the database if it does not exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'bills') THEN
        CREATE DATABASE bills;
    END IF;
END $$;

-- Connect to the 'bills' database to create the schema and user permissions
\c bills

-- Create the user if it does not exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_user WHERE usename = 'localhost') THEN
        CREATE USER localhost WITH PASSWORD 'password1';
    END IF;
END $$;

-- Create the schema if it does not exist
CREATE SCHEMA IF NOT EXISTS electric_bills;

-- Grant all privileges on the database and schema to the user
GRANT ALL PRIVILEGES ON DATABASE bills TO localhost;
GRANT ALL PRIVILEGES ON SCHEMA electric_bills TO localhost;
