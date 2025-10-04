# BILL TRANKING APP

# Table of Contents

1. [Introduction](#introduction)
   - [Technical solution](#technical-solution)
2. [ETL components](#etl)
   - [Email loader](#email_loader)
   - [PDF scanner](#pdf-scanner)
   - [Text parser](#text-parser)
   - [Table loader](#table-loader)
3. [API](#api)
4. [Frontend Components](#frontend-components)
5. [Alerts](#alerts)
6. [Postgres Tables](#postgres-tables)
   - [Input layer](#input-layer-schema-in_electric_bills)
   - [Output layer](#output-layer-schema-out_electric_bills)
7. [User Accounts](#user-accounts)

# Introduction
This app scans PDF bills to track electricity expenses, providing a dashboard and alert system to monitor costs over time and compare energy prices with ARERA’s regulated rates.

## Technical solution
The entire application is designed using a microservices architecture, containerized with Docker. This ensures secure network access, leverages built-in components, and enables cross-platform portability for easy environment setup. It also provides the ability to scale components efficiently as your project grows.

The application is composed of the following microservices (explained in more detail in later chapters):

1. **ETL**  
   This component downloads electric bill PDFs from the user’s email (via secure OAuth2 authentication), scans the PDF files to extract relevant information, and uses RAG to extract new context and prompt the LLM. This process transforms unstructured data into structured data, which is then loaded into database tables.

2. **Database**  
   PostgreSQL is used as the database engine. The database is organized into the following schemas/layers:  
   - **Metadata**: In this layer, application run data and logs will be collected. A pgvector-enabled table will be used for RAG operations. Only users with backend privileges will have access to this layer.  
   - **Input Layer**: This layer collects raw data from the ETL pipeline into tables. Only users with backend privileges will have access to this layer.  
   - **Output Layer**: This layer represents refined data from the previous layer in the form of views. This layer will be exposed to APIs.  

3. **Web Backend**  
   A layer of RESTful GET APIs used to query the database output layer.

4. **Web Frontend**  
   The frontend visualizes data and useful metrics in a simple and straightforward way.


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
