# BILL TRANKING APP

# Table of Contents

1. [Introduction](#introduction)
2. [Backend Components](#Backend-Components)
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

# Postgres Tables
## Input layer
### Table1: SUPPLY_DATA
This table contains information about energy supplier, contract type, reference period and other anagraphical information
| Column Name | Data Type | Constraints |
|-------------|-----------|-------------|
| CD_SUPPLIER|String||
| CD_ADDRESS | String | NOT NULL|
| CD_POD | String | NOT NULL|
| CD_SUBSCRIBED_POWER | String | |
| CD_AVAILABLE_POWER | String | |
| CD_OFFER | String | |
| CD_OFFER_CODE | String | |
| DT_CONTRACT_EXPIRE | Date | Format: YYYY-MM-DD |
| DT_START_ECONOMIC_COND | Date | Format: YYYY-MM-DD |
| DT_END_ECONOMIC_COND | Date | Format: YYYY-MM-DD |
| DT_START_SUPPLY | Date | Format: YYYY-MM-DD |
| CD_ANNUAL_EXP | String | |
| DT_START_ANNUAL_EXP | Date | Format: YYYY-MM-DD |
| DT_END_ANNUAL_EXP | Date | Format: YYYY-MM-DD |
| DT_INGESTION| Date | Format: YYYY-MM-DD |

## Output layer
### View1: V_CURRENT_CUSTOMERS_COSTS
| Column Name | Data Type | Constraints |
|-------------|-----------|-------------|
| CD_SUPPLIER|String||
| CD_ADDRESS | String ||
| CD_POD | String | |
| CD_OFFER | String | |
| CD_ANNUAL_EXP | String | |

# User Accounts
## Postgres
* dev_frontend: read access only to Input layer
* dev_backend: all privileges on all layers
