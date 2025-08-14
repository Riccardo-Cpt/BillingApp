-- Create the database if it does not exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'bills') THEN
        CREATE DATABASE bills;
    END IF;
END $$;

-- Create the schema if it does not exist
CREATE SCHEMA IF NOT EXISTS in_electric_bills;

--CREATE INPUT SCHEMA TABLES
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'in_electric_bills' AND table_name = 'supply_data') THEN
        CREATE TABLE in_electric_bills.supply_data (
            PK_BILL_PERIOD VARCHAR(50) NOT NULL,
            PK_SUPPLIER VARCHAR(255) NOT NULL,
            CD_ADDRESS VARCHAR(500) NOT NULL,
            PK_POD VARCHAR(50) NOT NULL,
            CD_SUBSCRIBED_POWER VARCHAR(50),
            CD_AVAILABLE_POWER VARCHAR(50),
            CD_OFFER VARCHAR(255),
            DT_CONTRACT_START DATE,
            DT_CONTRACT_EXPIRE DATE,
            TS_INGESTION TIMESTAMP,
            CONSTRAINT pk_supply_data PRIMARY KEY (PK_BILL_PERIOD, PK_SUPPLIER, PK_POD)
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'in_electric_bills' AND table_name = 'bill_overview') THEN
        CREATE TABLE in_electric_bills.bill_overview (
            FK_BILL_PERIOD VARCHAR(50) NOT NULL,
            FK_SUPPLIER VARCHAR(255) NOT NULL,
            FK_POD VARCHAR(50) NOT NULL,
            CD_ENERGY_EXPENDITURE VARCHAR(50),
            CD_TRANSPORT_MAINTEINANCE_EXPENDITURE VARCHAR(50),
            CD_TAXES VARCHAR(50),
            CD_RECALCULATION VARCHAR(50),
            CD_IVA VARCHAR(50),
            CD_TOTAL_COST VARCHAR(50),
            TS_INGESTION TIMESTAMP,
            CONSTRAINT fk_bill_overview FOREIGN KEY (FK_BILL_PERIOD, FK_SUPPLIER, FK_POD) REFERENCES in_electric_bills.supply_data (PK_BILL_PERIOD, PK_SUPPLIER, PK_POD)
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'in_electric_bills' AND table_name = 'electricity_meter_readings') THEN
        CREATE TABLE in_electric_bills.electricity_meter_readings (
            PK_READING_PERIOD DATE NOT NULL,
            FK_BILL_PERIOD VARCHAR(50) NOT NULL,
            FK_SUPPLIER VARCHAR(255) NOT NULL,
            FK_POD VARCHAR(50) NOT NULL,
            CD_PERIOD VARCHAR(20),
            CD_TYPE VARCHAR(20),
            INT_F1_READ INT,
            INT_F2_READ INT,
            INT_F3_READ INT,
            TS_INGESTION TIMESTAMP,
            CONSTRAINT pk_electricity_meter_readings PRIMARY KEY (PK_READING_PERIOD),
            CONSTRAINT fk_electricity_meter_readings FOREIGN KEY (FK_BILL_PERIOD, FK_SUPPLIER, FK_POD) REFERENCES in_electric_bills.supply_data (PK_BILL_PERIOD, PK_SUPPLIER, PK_POD)
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'in_electric_bills' AND table_name = 'electricity_meter_consumption_inferred') THEN
        CREATE TABLE in_electric_bills.electricity_meter_consumption_inferred (
            PK_READING_PERIOD DATE NOT NULL,
            FK_BILL_PERIOD VARCHAR(50) NOT NULL,
            FK_SUPPLIER VARCHAR(255) NOT NULL,
            FK_POD VARCHAR(50) NOT NULL,
            CD_PERIOD VARCHAR(20),
            CD_TYPE VARCHAR(20),
            INT_F1_READ INT,
            INT_F2_READ INT,
            INT_F3_READ INT,
            TS_INGESTION TIMESTAMP,
            CONSTRAINT pk_electricity_meter_consumption_inferred PRIMARY KEY (PK_READING_PERIOD),
            CONSTRAINT fk_electricity_meter_consumption_inferred FOREIGN KEY (FK_BILL_PERIOD, FK_SUPPLIER, FK_POD) REFERENCES in_electric_bills.supply_data (PK_BILL_PERIOD, PK_SUPPLIER, PK_POD)
        );
    END IF;
END $$;
	

CREATE SCHEMA IF NOT EXISTS out_electric_bills;
--CREATE OUTPUT SCHEMA TABLES/VIEWS

DO $$
BEGIN
		--create view for out schema
		CREATE OR REPLACE VIEW out_electric_bills.V_CURRENT_CUSTOMERS_COSTS AS
		SELECT 		
		    PK_BILL_PERIOD
			, PK_SUPPLIER
			, CD_ADDRESS
			, PK_POD
			, CD_OFFER
		FROM (
			SELECT 
				PK_BILL_PERIOD
				, PK_SUPPLIER
				, CD_ADDRESS
				, PK_POD
				, CD_OFFER
				, ROW_NUMBER() OVER(PARTITION BY PK_SUPPLIER, PK_POD, CD_OFFER ORDER BY PK_BILL_PERIOD DESC) RN
			FROM IN_ELECTRIC_BILLS.SUPPLY_DATA
		)
		WHERE RN = 1;
END $$;



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





--DUMMY INSTERTS, TO BE REMOVED

DO $$
BEGIN
		
		--DUMMY INSERTS, TO BE REMOVED
		INSERT INTO in_electric_bills.SUPPLY_DATA (
			PK_BILL_PERIOD,
			PK_SUPPLIER,
			CD_ADDRESS,
			PK_POD,
			CD_SUBSCRIBED_POWER,
			CD_AVAILABLE_POWER,
			CD_OFFER,
			DT_CONTRACT_START,
			DT_CONTRACT_EXPIRE,
			TS_INGESTION
		) VALUES (
			'01/01/2025 - 28/02/2025',
			'Illumia',
			'VIA PALUSTRI 22',
			'IT00118R4564',
			'6.00kW',
			'6.60kW',
			'STG Domestici Non Vulnerabili',
			'2024-01-01',
			'2099-10-01',
			'2025-08-01 00:00:00'
		);

				
		INSERT INTO in_electric_bills.SUPPLY_DATA (
			PK_BILL_PERIOD,
			PK_SUPPLIER,
			CD_ADDRESS,
			PK_POD,
			CD_SUBSCRIBED_POWER,
			CD_AVAILABLE_POWER,
			CD_OFFER,
			DT_CONTRACT_START,
			DT_CONTRACT_EXPIRE,
			TS_INGESTION
		) VALUES (
			'01/03/2025 - 31/04/2025',
			'Illumia',
			'VIA PALUSTRI 22',
			'IT00118R4564',
			'6.00kW',
			'6.60kW',
			'STG Domestici Non Vulnerabili',
			'2024-01-01',
			'2099-10-01',
			'2025-08-01 00:00:00'
		);

		
		INSERT INTO in_electric_bills.SUPPLY_DATA (
			PK_BILL_PERIOD,
			PK_SUPPLIER,
			CD_ADDRESS,
			PK_POD,
			CD_SUBSCRIBED_POWER,
			CD_AVAILABLE_POWER,
			CD_OFFER,
			DT_CONTRACT_START,
			DT_CONTRACT_EXPIRE,
			TS_INGESTION
		) VALUES (
			'01/05/2025 - 31/06/2025',
			'New_forn',
			'VIA PALUSTRI 22',
			'IT00118R4564',
			'6.00kW',
			'6.60kW',
			'STG Domestici Non Vulnerabili',
			'2024-06-01',
			'2099-10-01',
			'2025-08-01 00:00:00'
		);
END $$;