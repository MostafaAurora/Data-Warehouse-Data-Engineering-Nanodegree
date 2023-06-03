# Data Warehouse Project
---  
  

## Introduction
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.
As their data engineer, I am tasked with building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for the analytics team of Sparkify to continue finding insights in what songs their users are listening to.  

<br>
<br>

## Project Description
In this project, AWS services will be used to perform ETL on a json data sample from the one million songs dataset using A Redshift cluster to fetch the data stored on a S3 bucket and copy and transform the data into staging tables and then final fact and dimension tables

<br>
<br>

## Requirements
- Python
- AWS S3 bucket 
- A cluster on AWS Redshift - more information you can find here [Getting started with Amazon Redshift](https://docs.aws.amazon.com/redshift/latest/gsg/getting-started.html)  


To use the module `psycopg2` with python you should to install it with the following command:

  ```bash
  pip install psycopg2-binary
  ```  

<br>
<br>

## Project datasets

<br>

### Song Dataset

The first dataset is a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.
```
data/song_data/A/B/C/TRABCEI128F424C983.json
data/song_data/A/A/B/TRAABJL12903CDCF1A.json
```
And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.
```
{
    "num_songs": 1,
    "artist_id": "ARJIE2Y1187B994AB7",
    "artist_latitude": null,
    "artist_longitude": null,
    "artist_location": "",
    "artist_name": "Line Renaud",
    "song_id": "SOUPIRU12A6D4FA1E1",
    "title": "Der Kleine Dompfaff",
    "duration": 152.92036,
    "year": 0
}
```

<br>

### Log Dataset

The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations.  

The log files in the dataset we'll be working with are partitioned by year and month. For example, here are filepaths to two files in this dataset.
```
data/log_data/2018/11/2018-11-12-events.json
data/log_data/2018/11/2018-11-13-events.json
```
Below is an example of what the data in a log file, 2018-11-12-events.json, looks like.
![log-data](https://video.udacity-data.com/topher/2019/February/5c6c15e9_log-data/log-data.png)

<br>
<br>

## Database schema

<br>

### **Staging tables**
![staging tables](staging%20tables.png)

**A note about dtypes in staging tables:**  
In the staging table `staging_songs` the data type TEXT has been chosen instead of FLOAT for the columns artist_latitude, artist_longitude and duration because according to the [AWS Redshift documentation](https://docs.aws.amazon.com/redshift/latest/dg/copy-usage_notes-copy-from-json.html) loading numbers from data files in JSON format may lose precision, and these columns will be converted to FLOAT in the final INSERT queries for the dimension_artists table.  

The data types of all other columns, including the staging_events columns, have been selected based on their content.
Since these tables are only used for staging SORTKEY or DISTKEY have not been assigned.

<br>

### **Fact and dimension tables**
![Alt text](fact%20and%20dimension%20tables.png)



**Notes about assigned distribution keys and sort keys:**  

fact_songplays:
- SORTKEY:
The timestamp `start_time` has been chosen, since the data analysts are likely to make more inquiries over a certain period of time. This improves queries efficiency because they can skip entire blocks that fall outside the desired time range.

- DISTKEY:
The column `song_id` has been chosen, since most of the queries will probably be around it.
The distribution style has not been specified leaving the "Auto" decision to AWS Redshift.

dimension_users:
- DISTKEY:
The column `song_id` has been chosen, since most queries will probably be around it.

dimension_time:
- SORTKEY:
The column `start_time` has been chosen for the same reasons mentioned before.

<br>

## How to run the scripts
You can start the scripts via the terminal, cmd, shell...etc. by opening it and navigating to the project root directory.   
Here is an example of running a python script:
```bash
python etl.py
```
You should start by running the `create_tables.py` script and then run the `etl.py` script.

<br>
<br>

## Explanation of the files in the project  

- `create_tables.py`
  - This file contains a script that drops any previous tables and creating the necessary project tables ensuring a fresh start.
- `etl.py`
  - This file contains a script that maps the ETL task in this project. it loads the json files stored on a S3 bucket into the staging tables and then transfers the data from the staging tables to the fact and dimension tables on RedShift.
- `sql_queries.py`
  - This file contains all necessary queries for the Python scripts mentioned above.
- `dwh_example.cfg`
  - This file contains examples of the necessary configuration and credential files, if true existing credentials and configs are used in it, the project should be fully functional but true configurations and credentials SHOULD NOT BE SHARED ONLINE AND SHOULD BE USED LOCALLY OR ON SECURE MACHINES AND PLATFORMS ONLY.

  <br>
  <br>

  ## Project summary
  - In this project, AWS services are used to perform ETL on a json data sample from the one million songs dataset using A Redshift cluster to fetch the data stored on a S3 bucket and copy and transform the data into staging tables and then final fact and dimension tables.

  - The project starts by creating the appropriate table and database designs as well as the needed queries found in the `sql_queries.py` file.

  - Then 2 scripts are made utilizing the queries in the `sql_queries.py` file and the configs and credentials (yet to be defined) in the `dwh.cfg` file.
    - `create_tables.py` script which drops any previous tables and creates the necessary tables for the project ensuring a fresh start.
    - `etl.py` script which initializes the data copying from the S3 bucket to the staging tables and then the data insertion into the final fact and dimension tables.

  - Then the dataset is uploaded to a S3 bucket.

  - Then a RedShift cluster is created and configured allowing public access for the sake of the project, and then an appropriate role is used with the custer.

  - Then the credentials and configs are filled in the `dwh.cfg` file.

  - Then finally the scripts are run to perform the ETL process.

