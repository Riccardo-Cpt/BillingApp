-- Create the database if it does not exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'bills') THEN
        CREATE DATABASE bills;
    END IF;
END $$;

-- Connect to the 'bills' database to create the schema and user permissions
--\c bills

DO $$
BEGIN
	IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'in_electric_bills' AND table_name = 'supply_data') THEN
	
		CREATE TABLE in_electric_bills.SUPPLY_DATA (
			CD_SUPPLIER VARCHAR(100),
			CD_ADDRESS VARCHAR(255) NOT NULL,
			CD_POD VARCHAR(20) NOT NULL,
			CD_SUBSCRIBED_POWER VARCHAR(20),
			CD_AVAILABLE_POWER VARCHAR(20),
			CD_OFFER VARCHAR(255),
			CD_OFFER_CODE VARCHAR(50),
			DT_CONTRACT_EXPIRE DATE,
			DT_START_ECONOMIC_COND DATE,
			DT_END_ECONOMIC_COND DATE,
			DT_START_SUPPLY DATE,
			CD_ANNUAL_EXP VARCHAR(50),
			DT_START_ANNUAL_EXP DATE,
			DT_END_ANNUAL_EXP DATE,
			DT_INGESTION DATE
		);
		
		
		--DUMMY INSERTS, TO BE REMOVED
		INSERT INTO in_electric_bills.SUPPLY_DATA (
			CD_SUPPLIER,
			CD_ADDRESS,
			CD_POD,
			CD_SUBSCRIBED_POWER,
			CD_AVAILABLE_POWER,
			CD_OFFER,
			CD_OFFER_CODE,
			DT_CONTRACT_EXPIRE,
			DT_START_ECONOMIC_COND,
			DT_END_ECONOMIC_COND,
			DT_START_SUPPLY,
			CD_ANNUAL_EXP,
			DT_START_ANNUAL_EXP,
			DT_END_ANNUAL_EXP,
			DT_INGESTION
		) VALUES (
			'Illumia',
			'VIA PALUSTRI 22',
			'IT00118R4564',
			'6.00kW',
			'6.60kW',
			'STG Domestici Non Vulnerabili',
			'000155ENVFT00DXSERV_TUT_GRADUALI',
			'2099-10-01',
			'2024-07-01',
			'9999-12-31',
			'2024-07-01',
			'34,89 €',
			'2024-09-17',
			'2024-09-17',
			'2025-08-01'
		);
		
		INSERT INTO in_electric_bills.SUPPLY_DATA (
			CD_SUPPLIER,
			CD_ADDRESS,
			CD_POD,
			CD_SUBSCRIBED_POWER,
			CD_AVAILABLE_POWER,
			CD_OFFER,
			CD_OFFER_CODE,
			DT_CONTRACT_EXPIRE,
			DT_START_ECONOMIC_COND,
			DT_END_ECONOMIC_COND,
			DT_START_SUPPLY,
			CD_ANNUAL_EXP,
			DT_START_ANNUAL_EXP,
			DT_END_ANNUAL_EXP,
			DT_INGESTION
		) VALUES (
			'Illumia',
			'VIA PALUSTRI 22',
			'IT00118R4564',
			'6.00kW',
			'6.60kW',
			'STG Domestici Non Vulnerabili',
			'000155ENVFT00DXSERV_TUT_GRADUALI',
			'2099-10-01',
			'2024-07-01',
			'9999-12-31',
			'2024-07-01',
			'190,89 €',
			'2024-09-17',
			'2024-11-24',
			'2025-08-01'
		);
		
	END IF;
END $$


-- Create the users if it does not exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_catalog.pg_user WHERE usename = 'dev_backend') THEN
        CREATE USER dev_backend WITH PASSWORD 'password1';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_catalog.pg_user WHERE usename = 'dev_frontend') THEN
        CREATE USER dev_frontend WITH PASSWORD 'password2';
    END IF;
END $$;

-- Create the schema if it does not exist
CREATE SCHEMA IF NOT EXISTS in_electric_bills;
CREATE SCHEMA IF NOT EXISTS out_electric_bills;

-- Grant all privileges on the database and schema to the user dev_backend
GRANT ALL PRIVILEGES ON DATABASE bills TO dev_backend;
GRANT ALL PRIVILEGES ON SCHEMA in_electric_bills TO dev_backend;
GRANT ALL PRIVILEGES ON SCHEMA out_electric_bills TO dev_backend;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA in_electric_bills TO dev_backend;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA out_electric_bills TO dev_backend;

-- Grant just read privileges to the user dev_frontend
GRANT CONNECT ON DATABASE bills TO dev_frontend;
GRANT USAGE ON SCHEMA out_electric_bills TO dev_frontend;
GRANT SELECT ON ALL TABLES IN SCHEMA out_electric_bills TO dev_frontend;

-- Create table SUPPLY_DATA