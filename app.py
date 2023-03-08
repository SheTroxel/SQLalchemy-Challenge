
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

#############################################################################
#Database Setup
############################################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#refect on existing database into a new model
Base = automap_base()
#refect the tables
Base.prepare(engine, reflect = True)
print(Base.classes.keys())

# Save references to each tables
measurement = Base.classes.measurement
station = Base.classes.station

########################################################################
#Flask Set up
#######################################################################
app = Flask(__name__)

##########################################################################
# Flask Routes
#########################################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
    )

#set up first route for preciptiation data values and date
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return precipitation values and dates"""
    # determine time frame
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0],'%Y-%m-%d').date()
    beginning_date = dt.date(last_date.year - 1, last_date.month, last_date.day)
    #Query for percipitation data
    precip_query = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= beginning_date).all()
    #    print(precip_query)

    # Convert list to Dictionary
    precip_dictionary = {key:value for (key,value) in precip_query}

    session.close()
    return jsonify(precip_dictionary)

#set up route for all Stations
@app.route("/api/v1.0/station")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all Stations by prcp measurement"""
    # Query all stations 
    active_station = session.query(measurement.station, func.count(measurement.prcp)).group_by(measurement.station).order_by(func.count(measurement.prcp).desc()).all()
    
    #print(active_station)
    
    session.close()
    return jsonify(active_station)

#set up route for tobs
@app.route("/api/v1.0/tobs")
def tobs():
    #create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of tobs"""
    
    # define time period
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0],'%Y-%m-%d').date()
    beginning_date = dt.date(last_date.year - 1, last_date.month, last_date.day)

    #find most active station's temperature data for past 12 months
    most_active_station = session.query(measurement.date, measurement.station, measurement.tobs).\
    filter(measurement.station == "USC00519281").all()
    
    session.close()
    return jsonify(most_active_station)  

if __name__ == '__main__':
    app.run(debug=True)

