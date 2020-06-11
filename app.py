"""
This script primarily adds a record to an existing database using a frontend. This data can be used for training of the model

Written By - Manish Kumar
"""

import traceback
from flask import render_template, request, redirect, url_for
import logging.config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData

Base = declarative_base()
class no_show(Base):
    """Create a data model for the database to captire features and response """
    __tablename__ = 'no_show'
    PatientId = Column(Integer, primary_key=True)
    Gender = Column(String(10), unique=False, nullable=False)
    Age = Column(Integer, unique=False, nullable=False)
    Scholarship = Column(Integer, unique=False, nullable=False)
    Hipertension = Column(Integer, unique=False, nullable=False)
    Diabetes = Column(Integer, unique=False, nullable=False)
    Alcoholism = Column(Integer, unique=False, nullable=False)
    Handcap = Column(Integer, unique=False, nullable=False)
    SMS_received = Column(Integer, unique=False, nullable=False)
    Interval = Column(Integer, unique=False, nullable=False)
    Show_No_show = Column(String(100), unique=False, nullable=True)

    def __repr__(self):
        return '<no_show %r>' % self.Show_No_show





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
    """Main view that lists records in the database.

    Create view into index page that uses data queried from msia423_db database and
    inserts it into the msiapp/templates/index.html template.

    Returns: rendered html template

    """

    try:
        tracks = db.session.query(no_show).limit(app.config["MAX_ROWS_SHOW"]).all()
        logger.debug("Index page accessed")
        return render_template('index.html', tracks=tracks)
    except:
        traceback.print_exc()
        logger.warning("Not able to display no_show, error page returned")
        return render_template('error.html')


@app.route('/add', methods=['POST'])
def add_entry():
    """Function for collecting inputs from the front end and pushing them to the database

    :return: redirect to index page
    """

    try:
        no_show1 = no_show(Gender=request.form['Gender'], Age=request.form['Age'], Scholarship=request.form['Scholarship'],Hipertension=request.form['Hypertension'], Diabetes=request.form['Diabetes'], Alcoholism=request.form['Alcoholism'],Interval=request.form['Interval'], Handcap=request.form['Handcap'], SMS_received=request.form['SMS_received'], Show_No_show = request.form['Show(Yes/No)'])
        db.session.add(no_show1)
        db.session.commit()
        logger.info("New data added")
        return redirect(url_for('index'))
    except:
        logger.warning("Not able to display tracks, error page returned")
        return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
