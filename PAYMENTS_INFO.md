# Information on payment data
There are two publications every year. There is the initial data and then a refresh.

## Types and Data Size
1. General Payments (8 GB)
2. Research Payments (1 GB)
3. Physician Ownership (2 MB)

## Strategy
Given that the data is so large, we need a way to process efficiently. The best way to do this is to process in batches and incrementally insert into SQL database.

### Steps to success
1. Check if there is exisiting database
2. (yes) pull last updated date from API, if last updated date doesn't match API pull, update information
3. (no) create database and table with exisiting postgreSQL schema
    3a. Stream csv data and insert into database in batches
    3b. Updated time table was just updated

## Focus
I will first work on General Payments as it is the largest and most comprehesive. I will develop it with the idea that we can add Research Payments and Physician Payments in easily later. When the yearly refresh happens, we obviously will want to pull the changes and check for when that refresh happens.

### 2022 General Payment Data
#### API Information
Get Dataset
/api/1/metastore/schemas/dataset/items/df01c2f8-dc1f-4e79-96cb-8208beaf143c


