
import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List of all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date_only/<start><br/>"
        f"/api/v1.0/start_end/<start><end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of data"""
    # Query 
    previous_year = dt.date(2017,8,23)-dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=previous_year).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)
    
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list"""
    # Query all stations
    results = session.query(Station.station).all()
    session.close()
    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list """
    # Query date, temperature, for last year of data for USC00519281 
    previous_year = dt.date(2017,8,23)-dt.timedelta(days=365)
    
    all_tobi = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station =='USC00519281').\
        filter(Measurement.date>=previous_year).all()

    session.close()

    return jsonify(all_tobi)

@app.route("/api/v1.0/start_date_only/<start>") 

def startdateonly(start):

    session = Session(engine)

    #TO DO: for all stations
    ## 1.) Extract user input into variable
    
    # print(start)
    date = start.split("-")
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    start_date = dt.date(year, month, day)
    

    ## 2.) Build query based on user input
            #session.query = query
            #filter on date = filter      
   
    start_date_input = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date>=start_date).all()
   
    
    ## 3.) jsonify results
    session.close()
    return jsonify(start_date_input)
        
@app.route("/api/v1.0/start_end/<start>/<end>") 
  
def startend(start, end):

    session = Session(engine)

    date = start.split("-")
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    start_date = dt.date(year, month, day)

    date = end.split("-")
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    end_date = dt.date(year, month, day)

    #2.) Remove station filter, customize date filter 
  
    start_end_date_input = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date>=start_date).\
        filter(Measurement.date<=end_date).all()
    
    session.close()
    return jsonify(start_end_date_input)
    
if __name__ == '__main__':
    app.run(debug=True)

