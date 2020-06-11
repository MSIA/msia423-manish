"""
This script provides predictions to the user based on the values entered of the input features
Written by - Manish
"""

import traceback
from flask import render_template, request, redirect, url_for
import logging.config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import pickle
import yaml
from xgboost import XGBClassifier
cred_list = {}

with open(r'config/parameter.yaml') as file:
    cred_list = yaml.load(file, Loader=yaml.FullLoader)
# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)


@app.route('/')
def index():
    """
    This function simply takes the user to the prediction page
    Returs : predict.html template
    """

    try:
        return render_template('predict.html')
    except:
        traceback.print_exc()
        logger.warning("Not able to display no_show, error page returned")
        return render_template('error.html')


@app.route('/add', methods=['POST'])
def predict():
    """Function to make prediction

    :return: redirect to prediction page with the predictions for previous entries
    """

    #try:
    c = 0
    if request.form['Gender'] =='M':
        c = 1
    else :
        c = 0
    df = pd.DataFrame([[c, int(request.form['Age']), int(request.form['Scholarship']),int(request.form['Hypertension']),int(request.form['Diabetes']),int(request.form['Alcoholism']),int(request.form['Handcap']),int(request.form['SMS_received']),int(request.form['Interval'])]], columns=['Gender', 'Age', 'Scholarship','Hipertension','Diabetes','Alcoholism','Handcap','SMS_received','interval'])

    loaded_model = pickle.load(open(cred_list['model_local'], 'rb'))
    pred = loaded_model.predict(df)[0]
    if pred == 0:
        prediction = 'Will show for the appointment'
    if pred == 1:
        prediction = 'Will not show for the appointment'

    return render_template("predict.html", prediction = prediction)
    #except:
    #    logger.warning("Not able to display tracks, error page returned")
    #    return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])


