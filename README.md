# BILL TRANKING APP

# Table of Contents

1. [Introduction](#introduction)
   - [Technical solution](#technical-solution)
2. [ETL components](#etl)
   - [Email loader](#email_loader)
   - [PDF processing](#pdf-processing)
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
This app is designed to **scan and analyze PDF electricity bills**, helping users track their energy expenses over time. It provides a dashboard for visualizing costs and an alert system to notify users of significant changes. The app also compares actual energy prices with the regulated rates set by ARERA (the Italian Regulatory Authority for Energy, Networks, and Environment), ensuring transparency and fairness in billing.
Key Advantages:

1. **Local Hosting**: The app can be hosted locally, ensuring that sensitive billing data is never uploaded to third-party services, thus protecting user privacy.
2. **Price Monitoring**: It verifies that the prices charged in bills align with ARERA’s average regulated rates, helping users detect unjustified price increases.
3. **Historical Comparison**: The app tracks how current energy prices compare to the same period in previous years, allowing users to identify potential issues such as leaks, inefficiencies, or poorly maintained electrical lines or devices.

Origin of the Idea:
The app was inspired by the introduction of the **"mercato libero"** (free market) for electricity providers in Italy. A common issue in this system is that providers often raise prices without notifying users after a few years of a contract. This app addresses this problem by automating price monitoring and ensuring users are aware of any discrepancies or unexpected increases

## Technical solution
The entire application is designed using a microservices architecture, containerized with Docker. This ensures secure network access, leverages built-in components, and enables cross-platform portability for easy environment setup. It also provides the ability to scale components efficiently as your project grows.

The application is composed of the following microservices (explained in more detail in later chapters):

1. **ETL**  
   This component downloads electric bill PDFs from the user’s email (via secure OAuth2 authentication), scans the PDF files to extract relevant information, and uses RAG to extract new context and prompt the LLM. This process transforms unstructured data into structured data, which is then loaded into database tables.

3. 

4. **Database**  
   PostgreSQL is used as the database engine. The database is organized into the following schemas/layers:
   - **Embeddings**: In this layer, embeddings vector will be stored to perform a RAG pipeline. These embeddings provide the LLM model a defined structure on how to parse the input and and transform in a structured output.
   - **Metadata**: In this layer, application run data and logs will be collected. A pgvector-enabled table will be used for RAG operations. Only users with backend privileges will have access to this layer.  
   - **Input Layer**: This layer collects raw data from the ETL pipeline into tables. Only users with backend privileges will have access to this layer.  
   - **Output Layer**: This layer represents refined data from the previous layer in the form of views. This layer will be exposed to APIs.  

6. **Web Backend**  
   A layer of Django RESTful GET APIs used to query the database output layer.

7. **Web Frontend**  
   The frontend visualizes data and useful metrics in a simple and straightforward way.


# ETL

## Email_loader
TBD: goal access gmail account throug Oauth2 autentication, intercept new files and download them in dedicated folder. Understand how to securely download files inside docker container.

## PDF processing
This module is designed to parse PDF files sent by the billing company. Since most of the data in these PDFs is stored in tables, the PyPDFPlumber library was the best choice due to its extract_tables() function, which has proven more reliable than similar functions in competing libraries (e.g., PyMuPDF).

## Text parser
TBD: provided list of keywords, associate to each keyword an information extracted from text. Return a file in JSON format

## Table loader
JSON file read as dataframe throug pandas library. Dataframe are then loaded to Postgres through sqlalchemy python library

# API 
Will be developed in Django

# Frontend Components
TBD
# Alerts
- CD_RECALCULATION <> 0
- An alert to define when mean energy consumpion increases from one bill to the next
- Alert to trigger when cost per Kw is higher than average cost declared in ARERA website (understand if possible)

# Postgres Tables
## Embedding vector table: energy_bill_embeddings
This table is used in the RAG system to instruct the LLM on what data to extract from the input free text and to structure the output in a specific format, enabling it to be loaded into the associated database table.
| Column Name | Data Type | Constraints |Description |
|-------------|-----------|-------------|-------------|
| ID|Serial|NOT NULL|Unique incremental integer|
| DOCUMENT_NAME|String||Name of the document used to load data to this table|
| CD_TEXT_CONTENT | String ||Text loaded in the table. This text will be used in a RAG pipeline to add addidional context to user prompt to the LLM |
| VC_EMBEDDING | Vector(768) ||Embedding calculated from CD_TEXT_CONTENT associated value. Algorithm nomic-embed-text model is used to compute this value|
|TS_CREATION|Timestamp||Timestap of creation of the record|

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
