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
- [Build the docker image](#Build-the-docker-image)
- [To copy file on S3](#To-copy-file-on-S3)
- [To create Database locally](#To-create-Database-locally)
- [To create Database on AWS RDS](#To-create-Database-on-AWS-RDS)
- [Setting the environment variables](#Setting-the-environment-variables)
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
├── app
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
|   ├── run.sh                            <- Bash script run by docker
|   ├── run_docker.sh                     <- Bash script to run the Docker image
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
├── Dockerfile                        <- dockerfile 
├── .mysqlconfig                      <- config file Database environment variable
├── .awsconfig                        <- config file for aws environment variable
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

`winpty sh app/run_docker.sh copy`

run_docker.sh is a script in root directory that accepts an argument, either 'copy' or 'db' to copy a file on S3 or creatind a database locally or on AWS RDS respectively. The `winpty` command in the beginnig can be dropped for mac and linux users.
<!-- tocstop -->
## To create Database locally
In order to create a database locally the same script is run with a 'db' argument. However, update 'loc_database' to 'local' in the config/parameter.yaml file.

Run the following command

`winpty sh app/run_docker.sh db`

This will create a msia423.db in the data folder.
<!-- tocstop -->
## To create Database on AWS RDS
In order to create a database locally the same script is run with a 'db' argument. However, update 'loc_database' to 'AWS' in the config/parameter.yaml file and build the docker image again.

Run the following command

`winpty sh app/run_docker.sh db`

This will create a database on RDS with the name set in the .mysqlconfig file against the variable DATABSE_NAME. Currently it is msia423_db.

The created database can be checked and queried using the command below :

`winpty sh run_mysql_client.sh`

## To build features
To build the feature we run the same command with 'features' as the argument
`winpty sh app/run_docker.sh features`
This will create a file on S3 directly which is clean has all the features and ready for training. The testing script for the features is in the test folder

## To train the model
To train the model (XGBoost) same command is to be run with 'model' as the argument.
`winpty sh app/run_docker.sh model`

## Building the pipeline
In order to run the entire pipeline in the order
> copy raw data to s3 > build databse > clean data and featurise > build model
the same command is to be run but the argument becomes 'all'
`winpty sh app/run_docker.sh all`

## Testing
In testing the function in featurise.py script under src folder is tested. The command is same but the argument is 'test' 
`winpty sh app/run_docker.sh test`

Quite clearly app/run_docker.sh is the single entry for all the functionalities.

## Running the app
Much like above a single script is the entry point for the 2 apps one for adding a record to the database and other for getting predictions.
### Building the docker image
The dockerfile is placed in the app folder. Run the below command to build the image
`docker build -f app/Dockerfile -t no_show .`

### Adding records to database (AWS RDS)
To run the app that adds record using the front end use the following command
`winpty sh app/run_docker_app.sh add_db`

### Making predictions
To run the app for making predictions using the front end use the following command 
`winpty sh app/run_docker_app.sh predict`
The prediction will be shown on the webpage itself




