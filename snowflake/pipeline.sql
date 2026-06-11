CREATE OR REPLACE DATABASE weatherapi;

USE DATABASE weatherapi;

CREATE OR REPLACE SCHEMA weather_schema;

USE SCHEMA weather_schema;

-- STORAGE INTEGRATION


CREATE OR REPLACE STORAGE INTEGRATION weather_integration
TYPE = EXTERNAL_STAGE
STORAGE_PROVIDER = S3
ENABLED = TRUE
STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::099538659939:role/snowflake_s3_role'
STORAGE_ALLOWED_LOCATIONS = ('s3://veenapibucket/');


-- CHECK INTEGRATION


DESC STORAGE INTEGRATION weather_integration;

-- STAGE


CREATE OR REPLACE STAGE weather_stage
URL='s3://veenapibucket/'
STORAGE_INTEGRATION = weather_integration
FILE_FORMAT = (TYPE = JSON);


-- VERIFY FILES

LIST @weather_stage;

DESC INTEGRATION weather_integration;
-- FINAL TABLE


CREATE OR REPLACE TABLE weather_table (
    city STRING,
    timestamp TIMESTAMP,
    temperature FLOAT,
    humidity FLOAT
);

-- CLEAR OLD DATA


TRUNCATE TABLE weather_table;

-- LOAD DATA


INSERT INTO weather_table
SELECT
    $1:city.S::STRING AS city,
    TO_TIMESTAMP_NTZ($1:timestamp.S::STRING) AS timestamp,
    $1:temperature.S::FLOAT AS temperature,
    $1:humidity.S::FLOAT AS humidity
FROM @weather_stage;


-- VERIFY


SELECT * FROM weather_table;
