# BILL TRANKING APP

# Table of Contents

1. [Introduction](#introduction)
2. [ETL](#ETL)
   - [Email loader](#Email-loader)
   - [PDF scanner](#PDF-scanner)
   - [Text parser](#Text-parser)
   - [Table loader](#Table-loader)
4. [Postgres Tables](#Postgres-Tables)
   - [Input layer](#Input-layer)
   - [Output layer](#Output-layer)
6. [Frontend Components](#getting-started)
   - [TBD](#installation)
7. [User Accounts](#User-Accounts)

# Introduction
Goal of this app is to track electrical bills expenses by scanning PDF files, extract relevant information and store them in a Postgres DB.
A frontend service should pull data from postgres and create dashboards showing only relevant information.

# ETL

## Email_loader
TBD: goal access gmail account throug Oauth2 autentication, intercept new files and download them in dedicated folder. Understand how to securely download files inside docker container.

## PDF scanner
Pybplumber library used to parse each page of target PDF file. Irrelevant pages must be recognized and ignored in this step.

## Text parser
TBD: provided list of keywords, associate to each keyword an information extracted from text. Return a file in JSON format

## Table loader
JSON file read as dataframe throug pandas library. Dataframe are then loaded to Postgres through sqlalchemy python library

# API 
Will be developed in Django
1. 
Exports data to frontend Flask/Django REST framework (whatever is simpler).

# Frontend Components
TBD
# Alerts
- CD_RECALCULATION <> 0
- An alert to define when mean energy consumpion increases from one bill to the next
- Alert to trigger when cost per Kw is higher than average cost declared in ARERA website (understand if possible)

# Postgres Tables
## Input layer: schema in_electric_bills
### Table1: SUPPLY_DATA
This table contains information about energy supplier, contract type, reference period and other anagraphical information
| Column Name | Data Type | Constraints |Description |
|-------------|-----------|-------------|-------------|
| PK_BILL_PERIOD|String|NOT NULL|Billing period|
| PK_SUPPLIER|String|NOT NULL|Supplier name|
| CD_ADDRESS | String |NOT NULL|Customer's Address|
| PK_POD | String |NOT NULL|Unique identifier of electricity meter|
| CD_SUBSCRIBED_POWER | String ||Kw subscribed in the offer|
| CD_AVAILABLE_POWER | String ||Max Kw allowed by electricity meter|
| CD_OFFER | String ||Name of subscribed offer|
| DT_CONTRACT_START | Date | Format: YYYY-MM-DD |Contract start date|
| DT_CONTRACT_EXPIRE | Date | Format: YYYY-MM-DD |Contract expire date|
| TS_INGESTION| Timestamp | Format: YYYY-MM-DD hh:mm:ss |Timestamp of ingestion|

### Table2: BILL_OVERVIEW
This table contains information about energy supplier, contract type, reference period and other anagraphical information
| Column Name | Data Type | Constraints |Description |
|-------------|-----------|-------------|-------------|
| FK_BILL_PERIOD|String|NOT NULL|Billing period|
| FK_SUPPLIER|String|NOT NULL|Supplier name|
| FK_POD | String | NOT NULL|Unique identifier of electricity meter|
| CD_ENERGY_EXPENDITURE | String ||Expenses for energy|
| CD_TRANSPORT_MAINTEINANCE_EXPENDITURE | String ||Fees for maintaining and operating the infrastructure|
| CD_TAXES | String ||Taxes expenditure|
| CD_RECALCULATION | String ||Corrections for previous bill|
| CD_IVA | String ||Imposta Valore Aggiunto (additional tax)|
| CD_TOTAL_COST|String||Total amount of costs read from the bill (fixed + variable + taxes)|
| TS_INGESTION| Timestamp | Format: YYYY-MM-DD hh:mm:ss |Timestamp of ingestion|

### Table3: ELECTRICITY_METER_READINGS
This table contains information about what the supplier has read from my electricity meter.

**Remember**: PK_READING_PERIOD in this case must be inferred from CD_PERIOD String (try defining a dictionary for translation9

| Column Name | Data Type | Constraints |Description |
|-------------|-----------|-------------|-------------|
| PK_READING_PERIOD|Date|NOT NULL|This field allow join between ELECTRICITY_METER_CONSUMPION_INFERRED and ELECTRICITY_METER_READINGS|
| FK_BILL_PERIOD|String|NOT NULL|Billing period|
| FK_SUPPLIER|String|NOT NULL|Supplier name|
| FK_POD | String | NOT NULL|Unique identifier of electricity meter|
| CD_PERIOD| String||Month of reading|
| CD_TYPE | String||Effettivo/Stimato (Effective/Estimated)|
| INT_F1_READ | int | |Electric meter reading for time band F1 (Kwh)|
| INT_F2_READ | int | |Electric meter reading for time band F2 (Kwh)|
| INT_F3_READ | int | |Electric meter reading for time band F3 (Kwh)|
| TS_INGESTION| Timestamp | Format: YYYY-MM-DD hh:mm:ss |Timestamp of ingestion|

### Table4: ELECTRICITY_METER_CONSUMPION_INFERRED
This table contains information about what the supplier has defined as consumed since last read from electricity meter.

**Remember**: PK_READING_PERIOD in this case is just a conversion of CD_PERIOD to Date format 

| Column Name | Data Type | Constraints |Description |
|-------------|-----------|-------------|-------------|
| PK_READING_PERIOD|Date|NOT NULL|This field allow join between ELECTRICITY_METER_CONSUMPION_INFERRED and ELECTRICITY_METER_READINGS|
| FK_BILL_PERIOD|String|NOT NULL|Billing period|
| FK_SUPPLIER|String|NOT NULL|Supplier name|
| FK_POD | String | NOT NULL|Unique identifier of electricity meter|
| CD_PERIOD| String||Month of reading|
| CD_TYPE | String||Effettivo/Stimato (Effective/Estimated)|
| INT_F1_CONSUMED | int | |Electricity consumption since last reading for time band F1 (Kwh)|
| INT_F2_CONSUMED | int | |Electricity consumption since last reading for time band F2 (Kwh)|
| INT_F3_CONSUMED | int | |Electricity consumption since last reading for time band F3 (Kwh)|
| TS_INGESTION| Timestamp | Format: YYYY-MM-DD hh:mm:ss |Timestamp of ingestion|

## Output layer: schema out_electric_bills
### View1: V_CURRENT_CUSTOMERS_COSTS
| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| PK_BILL_PERIOD|String|||
| PK_SUPPLIER|String|||
| CD_ADDRESS | String |||
| PK_POD | String |||
| CD_OFFER | String |||
| FL_MEDIUM_PRICE_ELE|Float||Energy costs + Charges + Tax costs in €/kWh|

# User Accounts
## Postgres
* dev_frontend: read access only to Input layer
* dev_backend: all privileges on all layers
