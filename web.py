import os
import sqlalchemy
import numpy as np
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import create_engine , func
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from flask import Flask, jsonify, render_template


app = Flask(__name__)

#############################################
# Database Setup
#############################################

app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/db/world_happiness.sqlite"
db = SQLAlchemy(app)

Base = automap_base()

Base.prepare(db.engine,reflect=True)




Happy_2015 = Base.classes.happiness_2015
Happy_2016 = Base.classes.happiness_2016
Happy_2017 = Base.classes.happiness_2017
Countries = Base.classes.countries



@app.route("/")
def index():
	return render_template("index.html")





@app.route("/years")
def years():
	return jsonify(['2015','2016','2017'])





@app.route("/countries")
def countries():
	countries_sel = [Countries.country,Countries.code]
	countries_results = db.session.query(*countries_sel).all()



	countries_name = {}

	for result in countries_results:
		countries_name[result[0]] = result[1]
		

	return jsonify([countries_name])





@app.route("/<year>")
def countries_happy_year(year):
	years ={
	'2015': Happy_2015,
	'2016': Happy_2016,
	'2017': Happy_2017,
	}


	Happy_year = years.get(year)


	year_sel = [
		Happy_year.country_id,
		Happy_year.Country,
		Happy_year.HappinessRank,
		Happy_year.HappinessScore,
		Happy_year.Economy_GDPperCapita,
		Happy_year.Family,
		Happy_year.Health_LifeExpectancy,
		Happy_year.Freedom,
		Happy_year.Trust_GovernmentCorruption,
		Happy_year.Generosity,
		Happy_year.DystopiaResidual,
		Happy_year.Code,
		Happy_year.Latitude,
		Happy_year.Longitude,
		Happy_year.Region,
	]



	year_results = db.session.query(*year_sel).all()




	happy_year_data_list = []


	for result in year_results:

		happy_year_data = {}

		happy_year_data['Country']= result[1]
		happy_year_data['Code'] = result[11]
		happy_year_data['Region'] = result[14]
		happy_year_data['country_id'] = result[0]
		happy_year_data['HappinessRank'] = result[2]
		happy_year_data['HappinessScore'] = result[3]
		happy_year_data['Economy_GDPperCapita'] = result[4]
		happy_year_data['Family'] = result[5]
		happy_year_data['Health_LifeExpectancy'] = result[6]
		happy_year_data['Freedom'] = result[7]
		happy_year_data['Trust_GovernmentCorruption'] = result[8]
		happy_year_data['Generosity'] = result[9]
		happy_year_data['DystopiaResidual'] = result[10]
		happy_year_data['Latitude'] = result[12]
		happy_year_data['Longitude'] = result[13]
		happy_year_data_list.append(happy_year_data)
	
	
	return jsonify(happy_year_data_list)





@app.route("/<year>/<country>")
def countries_happy(year,country):
	years ={
	'2015': Happy_2015,
	'2016': Happy_2016,
	'2017': Happy_2017,
	}


	Happy_year = years.get(year)



	sel = [
		Happy_year.country_id,
		Happy_year.Country,
		Happy_year.HappinessRank,
		Happy_year.HappinessScore,
		Happy_year.Economy_GDPperCapita,
		Happy_year.Family,
		Happy_year.Health_LifeExpectancy,
		Happy_year.Freedom,
		Happy_year.Trust_GovernmentCorruption,
		Happy_year.Generosity,
		Happy_year.DystopiaResidual,
		Happy_year.Code,
		Happy_year.Latitude,
		Happy_year.Longitude,
	]



	results = db.session.query(*sel).filter(Happy_year.Country == country).all()



	happy_data = {}


	for result in results:

		happy_data['year'] = year
		happy_data['country_id'] = result[0]
		happy_data['Country'] = result[1]
		happy_data['Code'] = result[11]
		happy_data['HappinessRank'] = result[2]
		happy_data['HappinessScore'] = result[3]
		happy_data['Economy_GDPperCapita'] = result[4]
		happy_data['Family'] = result[5]
		happy_data['Health_LifeExpectancy'] = result[6]
		happy_data['Freedom'] = result[7]
		happy_data['Trust_GovernmentCorruption'] = result[8]
		happy_data['Generosity'] = result[9]
		happy_data['DystopiaResidual'] = result[10]
		happy_data['Latitude'] = result[12]
		happy_data['Longitude'] = result[13]


	return jsonify(happy_data)





@app.route("/region/<year>")
def region_happy(year):
	years ={
	'2015': Happy_2015,
	'2016': Happy_2016,
	'2017': Happy_2017,
	}


	Happy_year = years.get(year)



	avg_region_results = db.session.query(
		func.avg(Happy_year.HappinessScore),
		Happy_year.Region
		).group_by(
		Happy_year.Region
		).all()


	avg_region_Happiness ={}
	for result in avg_region_results:
		avg_region_Happiness[result[1]] = result[0]




	return(jsonify(avg_region_Happiness))
		





if __name__ =="__main__":
	app.run(debug = True)