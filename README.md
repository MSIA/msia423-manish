# MSiA423 Template Repository
Created by - Manish Kumar (MSiA Class of 2020)
QA by Skye Sheng
<!-- toc -->
- [Project Charter](#Project-Charter)
- [Sprint Plan](#Sprint-Plan)
- [Backlog](#Backlog)
- [Icebox](#Icebox)

## Project Charter
<!-- toc -->
### Vision 
A doctor's time is of an extreme importance. A no show on an appointment with a doctor means the time being stolen by someone who actually needed it. This project aims to quantify the possibility of a person not showing up for his appointment. Based on the entries provided by the person a Machine Learning algorithm will be used to train on a historical data and output prediction containing the probability of a person not showing up.  

### Mission
This project is going to assist hospitals and clinics in order to book their appointments in right number. If there are too many patients having a high probability of not showing up on a particular day they might book more. This is not only going to increase the revenue of the clinics but also help out someone who actually needs a consultation. 

### Success Criteria
To assess the performance of model Lift analysis will be used. More commonly used metrics like accuracy, precision or AUC-ROC(Area under the curve- Receiver Operating Charecteristics) is not being used here because the project is going to provide a soft classification rendering these methods not applicable here. 
Business impact of the project is going to be studied using a carefully designed experiments. A/B testing to be done on clinics and there revenues as the response variable to be monitored over 6 months period of time. Current assumption is that revenues will be normally distributed and therefore Welch's Test will be used keeping a p-value of 0.05. 

<!-- toc -->

## Sprint Plan
### Initiative 1 : Loading Data on cloud and creating the environment
#### Epic-1 
* Story 1 (1 pt): Install Docker, anaconda and python libraries
* Story 2 (3 pt): Perform an end to end run of pennylane to check the availability of every requirement
#### Epic-2
* Story 1 (1 pt): Place the .CSV file on the staging area (S3 AWS)
* Story 2 (1 pt): Host the data from .CSV file on Redshift

### Initiative 2 : Model training
#### Epic-1
* Story 1 (2 pt): Perform Exploratory Data Analysis and look for any trends or skewness in the data
* Story 2 (2 pt): Perform Data cleaning or transformation as per requirement
#### Epic-2
* Story 1 (5 pt): Train the model on the dataset after splitting it in k-fold
* Story 3 (3 pt): Finetune the best model using k-fold crossvalidation and save the model in pickel format

### Initiative 3 : Building Web based app and performing A/B testing
#### Epic-1
* Story 1 (5 pt): Building fromt end that prompts user to enter the needed information for rating prediction
#### Epic-2
* Story 1 (5 pt): Identifying the treatment and control group for A/B testing
* Story 2 (5 pt): Providing the app to the control group and monitoring the revenues 
* Story 3 (2 pt): Using t-test to find the usefulness of the app

<!-- toc -->
## Backlog
* I1E1 (Completed)
* I1E2 (Planned)
* I1E3 (Planned)

<!-- toc -->
## Icebox
* I2E1
* I2E2
* I3E1
* I3E2
* I3E3



----------------------------------------------------------------------------------------------------------------------------------------



- [Directory structure](#directory-structure)
- [Build the docker image](#Build the docker image)
- [To copy file on S3](#To copy file on S3)
- [To create Database locally](#To create Database locally)
- [To create Database on AWS RDS](#To create Database on AWS RDS)
- [Setting the environment variables](#Setting the environment variables)
- [Running the app](#running-the-app)
  * [1. Initialize the database](#1-initialize-the-database)
    + [Create the database with a single song](#create-the-database-with-a-single-song)
    + [Adding additional songs](#adding-additional-songs)
    + [Defining your engine string](#defining-your-engine-string)
      - [Local SQLite database](#local-sqlite-database)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Run the Flask app](#3-run-the-flask-app)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Build the image](#1-build-the-image)
  * [2. Run the container](#2-run-the-container)
  * [3. Kill the container](#3-kill-the-container)

<!-- tocstop -->

## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── parameter.yaml                <- Config file to store variables
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│   ├── rds_db.py                     <- Python file for db creation
|   ├── copy_s3.py                    <- Python file for copying files to s3
|
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies
├── run.sh                            <- Bash script run by docker
├── run_docker.sh                     <- Bash script to run the Docker image
├── Dockerfile                        <- dockerfile 
├── .mysqlconfig                      <- config file Database environment variable
├── .awscongig                        <- config file for aws environment variable
```

<!-- tocstop -->
## Setting the environment variables
As a first step the environment variables need to be set. Please change the place holder values in the .mysqlconfig and .awsconfig files. Next run the following commands :

`echo 'source .awsconfig' >> ~/.bashrc`

`source ~/.bashrc`

`echo 'source .mysqlconfig' >> ~/.bashrc`

`source ~/.bashrc`

<!-- tocstop -->
## Build the docker image
The docker file lies in the root directory. 
`docker build -t s3_rds . `

This command will the build the docker image s3_rds
<!-- tocstop -->
## To copy file on S3
The data for this project can be found on https://www.kaggle.com/joniarroba/noshowappointments. This data has been made available by Joni Hoppen and licensed under https://creativecommons.org/licenses/by-nc-sa/4.0/ terms. Once downloaded place the .csv file in the data folder or update the config/parameter.yaml file with the location of the data. Also, update the bucket name, and address and name of the file intended to be kept on s3.
Next, run the following command to pjut the file on S3 :

`winpty sh run_docker.sh copy`

run_docker.sh is a script in root directory that accepts an argument, either 'copy' or 'db' to copy a file on S3 or creatind a database locally or on AWS RDS respectively. The `winpty` command in the beginnig can be dropped for mac and linux users.
<!-- tocstop -->
## To create Database locally
In order to create a database locally the same script is run with a 'db' argument. However, update 'loc_database' to 'local' in the config/parameter.yaml file.

Run the following command

`winpty sh run_docker.sh db`

This will create a no_show.db in the data folder.
<!-- tocstop -->
## To create Database on AWS RDS
In order to create a database locally the same script is run with a 'db' argument. However, update 'loc_database' to 'AWS' in the config/parameter.yaml file.

Run the following command

`winpty sh run_docker.sh db`

This will create a database on RDS with the name set in the .mysqlconfig file against the variable DATABSE_NAME. Currently it is msia423_db.

The created database can be checked and queried using the command below :

`winpty sh run_mysql_client.sh`




## Running the app
### 1. Initialize the database 

#### Create the database with a single song 
To create the database in the location configured in `config.py` with one initial song, run: 

`python run.py create_db --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py create_db` creates a database at `sqlite:///data/tracks.db` with the initial song *Radar* by Britney spears. 
#### Adding additional songs 
To add an additional song:

`python run.py ingest --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py ingest` adds *Minor Cause* by Emancipator to the SQLite database located in `sqlite:///data/tracks.db`.

#### Defining your engine string 
A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used. For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/13/core/engines.html). We will cover SQLAlchemy and connection strings in the SQLAlchemy lab session on 
##### Local SQLite database 

A local SQLite database can be created for development and local testing. It does not require a username or password and replaces the host and port with the path to the database file: 

```python
engine_string='sqlite:///data/tracks.db'

```

The three `///` denote that it is a relative path to where the code is being run (which is from the root of this directory).

You can also define the absolute path with four `////`, for example:

```python
engine_string = 'sqlite://///Users/cmawer/Repos/2020-MSIA423-template-repository/data/tracks.db'
```


### 2. Configure Flask app 

`config/flaskconfig.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
HOST = "0.0.0.0" # the host that is running the app. 0.0.0.0 when running locally 
PORT = 5000  # What port to expose app on. Must be the same as the port exposed in app/Dockerfile 
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/tracks.db'  # URI (engine string) for database that contains tracks
APP_NAME = "penny-lane"
SQLALCHEMY_TRACK_MODIFICATIONS = True 
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100 # Limits the number of rows returned from the database 
```

### 3. Run the Flask app 

To run the Flask app, run: 

```bash
python app.py
```

You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

## Running the app in Docker 

### 1. Build the image 

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run from this directory (the root of the repo): 

```bash
 docker build -f app/Dockerfile -t pennylane .
```

This command builds the Docker image, with the tag `pennylane`, based on the instructions in `app/Dockerfile` and the files existing in this directory.
 
### 2. Run the container 

To run the app, run from this directory: 

```bash
docker run -p 5000:5000 --name test pennylane
```
You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

This command runs the `pennylane` image as a container named `test` and forwards the port 5000 from container to your laptop so that you can access the flask app exposed through that port. 

If `PORT` in `config/flaskconfig.py` is changed, this port should be changed accordingly (as should the `EXPOSE 5000` line in `app/Dockerfile`)

### 3. Kill the container 

Once finished with the app, you will need to kill the container. To do so: 

```bash
docker kill test 
```

where `test` is the name given in the `docker run` command.
