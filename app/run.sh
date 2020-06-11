#!/bin/bash

#############################################################################################
#                                                                                           #
#Written by : Manish Kumar                                                                  #
#                                                                                           #
#Script that accepts argument wether copy or db and correspondingly runs the python files   #
#                                                                                           #
#############################################################################################

val="$(grep 'loc_database' config/parameter.yaml)"
val2="$(cut -d':' -f2 <<<$val)"

if [ $1 = 'copy' ];

then
        python3 src/copy_to_s3.py

elif [ $1 = 'db' ];

then

	python3 src/rds_db.py

elif [ $1 = 'features' ];

then

    python3 src/transform_data.py

elif [ $1 = 'model' ];

then

    python3 src/model.py

elif [ $1 == 'all' ];

then
    python3 src/copy_to_s3.py
    python3 src/rds_db.py
    python3 src/transform_data.py
    python3 src/model.py

elif [ $1 = 'test' ];

then
    python3 -m pytest test/test.py
fi
