# Import the Flask dependency.
from re import M
from flask import Flask, jsonify

# Import other dependencies.
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Set up database engine.
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into the classes.
Base = automap_base()
Base.prepare(engine, reflect=True)

# Create variables for each of the classes.
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link.
session = Session(engine)


# Set up Flask
app = Flask(__name__)

# Create routes

# Welcome route
@app.route('/')
def welcome():
    return(
    '''
    Welcome to the Hawaii Climate Analysis API!<br/>
    Available Routes:<br/>
    /api/v1.0/precipitation<br/>
    /api/v1.0/stations<br/>
    /api/v1.0/tobs<br/>
    /api/v1.0/temp/start/end
    ''')

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Calculate the date from one year ago.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Get the date and precipitation for the previous year.
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    
    # Format results into JSON structured file.
    precip = {date: prcp for date, prcp in precipitation}

    return jsonify(precip)


# Stations route
@app.route("/api/v1.0/stations")
def stations():

    # Get all stations in the database.
    results = session.query(Station.station).all()

    # Unravel results into one-dimensional array.
    stations = list(np.ravel(results))

    # stations=stations formats list into JSON.
    return jsonify(stations=stations)


# Monthly Temperature route
@app.route("/api/v1.0/tobs")
def temp_monthly():

    # Calculate the date from one year ago.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query station with the highest number of temperature observations.
    # Get all the temperature observations from the previous year. 
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    
    # Unravel results into one-dimensional array.
    temps = list(np.ravel(results))
    
    # Format list into JSON.
    return jsonify(temps=temps)

# Stats route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):

    # Select min, avg, and max temperatures from SQLite database.
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # Only start date specified
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps) 
    
    # Start and end dates specified
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))

    return jsonify(temps)




# To run:
# Open Anaconda Powershell
# set FLASK_APP=app.py
# flask run







