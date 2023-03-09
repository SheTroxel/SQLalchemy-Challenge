#Set up dependencies
#################################################################################
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#############################################################################
#Set database engine for Flask and connect to SQLite database file
############################################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#refect on existing database into classes
Base = automap_base()
#refect the tables
Base.prepare(engine, reflect = True)
print(Base.classes.keys())

# Set class variables
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
        f"List of precipatation values from all stations for prior year<br/>"
        f"/api/v1.0/station<br/>"
        f"List of stations with total precipitation values<br/>"
        f"/api/v1.0/tobs<br/>"
        f"List of temperatures observed<br/>"
        f"/api/v1.0/temp/<start>"
        f"When given a start date (YYYY-MM-DD), calculates the MIN/AVG/MAX For a specified start date greater than or equal to the start date.<br/>"
        f"/api/v1.0/temp_range<start>/<end>"
        f"When given a start and end date (YYYY-MM-DD), calculates the MIN/AVG/MAX for the start date to the end date, inclusive<br/>"
    )
#/api/v1.0/temp/start/end
##########################################################################
#set up first route for preciptiation data values and date
#########################################################################
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
###################################################################################
#set up route for all Stations
###################################################################################
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
##################################################################################################################################################################################
#set up route for Tobs 
######################################################################################################
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
######################################################################################################
#set up weather statistics route one (start)
#############################################################################################################
@app.route ("/api/v1.0/temp/<start>")
def stats1 (start ):
    session = Session(engine)
    # define time period. Online assist from git hub user davidwjones for this one.
    start_date =dt.datetime.strptime(start,'%Y-%m-%d')
    data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()
    stats = list(np.ravel(data))

    session.close()
    return jsonify(stats)    
    
######################################################################################################
#set up weather statistics route two (start and end date)
#############################################################################################################                           
@app.route ("/api/v1.0/temp_range/<start>/<end>")
def stats2 (start,end):
    session = Session(engine)
    # define time period from start to end date
    # and get MIN/AVG/MAX temperatures from back one year
    #  Online assist from git hub user davidwjones for this one.
    start_date =dt.datetime.strptime(start,'%Y-%m-%d')
    end_date =dt.datetime.strptime(end,'%Y-%m-%d')
    data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    stats2 = list(np.ravel(data))

    print(start_date, end_date, stats2)

    session.close()
    return jsonify(stats2)  

if __name__ == '__main__':
    app.run(debug=True)

