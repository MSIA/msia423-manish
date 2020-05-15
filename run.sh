#!/bin/bash

#############################################################################################
#                                                                                           #
#Written by : Manish Kumar                                                                  #
#                                                                                           #
#Script that accepts argument wether copy or db and correspondingly runs the python files   #
#                                                                                           #
#############################################################################################


if [ $1 = 'copy' ];

then
	python3 src/copy_to_s3.py

else
	python3 src/rds_db.py

fi
