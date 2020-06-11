#!/bin/bash

###########################################################################################################
#                                                                                                         #
# Written by - Manish Kumar                                                                               #
#                                                                                                         #
# This script runs the docker for copying file to s3 or creating a database locally or                    #
# or on AWS RDS. It takes an argument as 'db','transform' or 'copy'. If the input is 'db'                 #
# it checks parameter.yaml for loc_database. If the value is local it directly runs the                   #
# rds_db.py else runs the docker                                                                          #
#                                                                                                         #
###########################################################################################################



val="$(grep 'loc_database' config/parameter.yaml)"
val2="$(cut -d':' -f2 <<<$val)"

if [ $1 = 'db' ] && [ $val2 = 'local' ];
then
    python src/rds_db.py

else

    docker run -v "$(pwd)":"$(pwd)" -it \
    --env aws_access_key_id \
    --env aws_secret_access_key \
    --env MYSQL_HOST \
    --env MYSQL_PORT \
    --env MYSQL_USER \
    --env MYSQL_PASSWORD \
    --env DATABASE_NAME \
    s3_rds app/run.sh $1

fi
