
import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

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
        f"/api/v1.0/start_end/<start>/<end>"
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

#@app.route("/api/v1.0/start_date_only/<start>") 

#def startonly(start):

#for x in x:

        #if search_term == 20170101:
            #return jsonify(character)

    #return jsonify({"error": "Character not found."}), 404



    # Create our session (link) from Python to the DB
    #session = Session(engine)
    
    #start_date = "%Y-%m-%d"

   # if start_date >= 2017,1,1
        #previous_year_start = dt.date(2018,1,1)-dt.timedelta(days=365)
        #previous_year_end = dt.date(2018,1,7)-dt.timedelta(days=365)

        #tmin, tavg, tmax = calc_temps(previous_year_start.strftime("%Y-%m-%d"), previous_year_end.strftime("%Y-%m-%d"))[0]

        #return jsonify(tmin, tavg, tmax)
    #else:
        #return jsonify({"error": f"Date not found. Try a date between 2017-1-1 or later."}), 404  

#@app.route("/api/v1.0/start_end/<start>/<end>") 

#def startend(start, end):
    
    # Create our session (link) from Python to the DB
    #session = Session(engine)
    
    #start_date = "%Y-%m-%d"

   # if start_date >= 2017,1,1
        #previous_year_start = dt.date(2018,1,1)-dt.timedelta(days=365)
        #previous_year_end = dt.date(2018,1,7)-dt.timedelta(days=365)

        #tmin, tavg, tmax = calc_temps(previous_year_start.strftime("%Y-%m-%d"), previous_year_end.strftime("%Y-%m-%d"))[0]

        #return jsonify(tmin, tavg, tmax)
    #else:
        #return jsonify({"error": f"Date not found. Try a date between 2017-1-1 or later."}), 404  

if __name__ == '__main__':
    app.run(debug=True)
