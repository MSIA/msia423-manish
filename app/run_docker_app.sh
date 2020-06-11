#!/bin/bash

if [ $1 = 'add_db' ];
then
  winpty docker run -v "$(pwd)":"$(pwd)" -it --env aws_access_key_id --env aws_secret_access_key -p 5000:5000 no_show app.py
elif [ $1 = 'predict' ];
then
  winpty docker run -v "$(pwd)":"$(pwd)" -it --env aws_access_key_id --env aws_secret_access_key  -p 5000:5000 no_show app_predict.py
fi
