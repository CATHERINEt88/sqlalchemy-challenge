import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta

from flask import Flask, jsonify


#########################################
##    Database SETUP
#########################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
                     


# reflect an existing database into a new model
# reflect the tables
# save reference to tables
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)             

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f'Available routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>' 
        f'/api/v1.0/tobs<br/>'
	f'<br/>'
	f'The last two routes will return the summary of temperature for a given start/start-end range.<br/>'
	f'To find the temperature info for a given date, please enter a starting date.<br/>'
        f'/api/v1.0/<start><br/>'
	f'<br/>'
	f'To find the temperature info for a given date, please enter a starting date and the end date in %Y-%M-%D format.<br/>'
        f'/api/v1.0/<start><end><br>'
    )

                     
@app.route("/api/v1.0/stations")
def station():
#  Create our session (link) from Python to the DB
    session = Session(engine)
    station_info = session.query(Station.station, Station.name).all()
    session.close()
                     
    #covert the list of tuples into a normal list
    all_station=[]
    for x,y in station_info:
        st_dic={}
       	st_dic["station"]=x
        st_dic["name"]=y            
        all_station.append(st_dic)
    return jsonify(all_station)   

@app.route("/api/v1.0/precipitation")
def prcp():

#  Create our session (link) from Python to the DB
    session = Session(engine)
    start_date = '2016-08-23'
    end_date = '2017-08-23'
    result = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()

#Create dictionary from the row data and append to a list
    one_year_prcp = []
    for d,p in result:
        prcp_dic={}
       	prcp_dic["Date"]=d
        prcp_dic["PRCP value"]=p
        one_year_prcp.append(prcp_dic)
    return jsonify(one_year_prcp)


@app.route("/api/v1.0/tobs")
def tobs():
#  Create our session (link) from Python to the DB
    session = Session(engine)
    start_date = '2016-08-23'
    end_date = '2017-08-23'
    most_active = 'USC00519281'
    tob_info = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station == most_active).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()
                     
    #covert the list of tuples into a normal list
    all_tobs=[]
    for x,y in tob_info:
       t_dic={}
       t_dic["Date"]=x
       t_dic["Tobs Value"]=y
       all_tobs.append(t_dic)
    return jsonify(all_tobs)  


@app.route("/api/v1.0/<start>")
def start(start):
#  Create our session (link) from Python to the DB

    start_date = datetime.strptime(start,"%Y-%m-%d")
    summary = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    session.close()

## convert the list of tuples into a normal list
    temp_obsv=[]
    for x,y,z in summary:
       sum_dic={}
       sum_dic["Min temperature"]=x
       sum_dic["Avg temperature"]=y
       sum_dic["Max temperature"]=z
       temp_obsv.append(sum_dic)
    return jsonify(temp_obsv)    

@app.route("/api/v1.0/<start>/<end>")
def startandend(start,end):
#  Create our session (link) from Python to the DB

    start_date = datetime.strptime(start,"%Y-%m-%d")
    end_date = datetime.strptime(end,"%Y-%m-%d")
    summary = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()

## convert the list of tuples into a normal list
    temp_obsv2=[]
    for x,y,z in summary:
       sum_dic2={}
       sum_dic2["Min temperature"]=x
       sum_dic2["Avg temperature"]=y
       sum_dic2["Max temperature"]=z
       temp_obsv2.append(sum_dic2)
    return jsonify(temp_obsv2)   



if __name__ == '__main__':
    app.run(debug=True)
      
                   