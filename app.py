# 1. import Flask
import os

import math
import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

import sqlite3 as sql
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt
import random

from geopy.geocoders import Nominatim

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return render_template("index.html")


# 4. Define what to do when a user hits the /about route
@app.route("/getLREGValue",methods=['POST','GET'])
def get_lreg_value():
    if request.method == 'POST':
        lreg_model = pickle.load(open("lreg_model\LinearRegression.pkl", "rb"))
        #return jsonify(request.form)

        num_bedrooms = request.form.get("beds")
        num_baths = request.form.get("baths")
        sft = request.form.get("houseArea")
        address = request.form.get("address")
        lot_size_sft = request.form.get("plotArea")
        tax_assessment = request.form.get("taxA")
        year_built = request.form.get("year")

        last_sold_price = 0
        total_rooms = 0
        #return(jsonify(address))
        nom = Nominatim()
        #loc = nom.geocode(str(address))
        #return loc
        #address_lat = loc.latitude
        #address_long = loc.longitude
        address_lat = 35
        address_long = 37

        num_bedrooms = int(num_bedrooms) if num_bedrooms else 0
        num_baths = float(num_baths) if num_baths else 0.0                  # Account for half baths
        sft = float(sft) if sft else 0.0
        last_sold_price = float(last_sold_price) if last_sold_price else 0.0
        address_lat = float(address_lat) if address_lat else 35.7796       # Raleigh Latitude
        address_long = float(address_long) if address_long else 78.6382    # Raleigh Longitude
        lot_size_sft = int(lot_size_sft) if lot_size_sft else 0
        tax_assessment = float(tax_assessment) if tax_assessment else 0.0
        total_rooms = float(total_rooms) if total_rooms else 0.0
        year_built = int(year_built) if year_built else 2000                # Default Year Built = 2000

        age=2019-year_built

        X_Score_df = pd.DataFrame(columns = ['bathrooms','bedrooms','finishedSqFt','yearBuilt'])
        X_Score_df = [[num_baths, num_bedrooms, sft, age]]
        caluclated_price = lreg_model.predict(X_Score_df)
        cp = "{:.2f}".format(caluclated_price[0][0])
        print(caluclated_price)
        return jsonify(f'Our expert Larry gives a predicted price of ${cp}')
        #return jsonify(f'{calculated_price[0][0]}')
    return jsonify("blah")


@app.route("/getSVMValue",methods=['POST','GET'])
def get_svm_value():
    if request.method == 'POST':
        lreg_model = pickle.load(open("lreg_model\LinearRegression.pkl", "rb"))
        #return jsonify(request.form)

        num_bedrooms = request.form.get("beds")
        num_baths = request.form.get("baths")
        sft = request.form.get("houseArea")
        address = request.form.get("address")
        lot_size_sft = request.form.get("plotArea")
        tax_assessment = request.form.get("taxA")
        year_built = request.form.get("year")

        last_sold_price = 0
        total_rooms = 0
        #return(jsonify(address))
        nom = Nominatim()
        loc = nom.geocode(str(address))
        #return loc
        address_lat = loc.latitude
        address_long = loc.longitude
        #address_lat = 35
        #address_long = 37

        num_bedrooms = int(num_bedrooms) if num_bedrooms else 0
        num_baths = float(num_baths) if num_baths else 0.0                  # Account for half baths
        sft = float(sft) if sft else 0.0
        last_sold_price = float(last_sold_price) if last_sold_price else 0.0
        address_lat = float(address_lat) if address_lat else 35.7796       # Raleigh Latitude
        address_long = float(address_long) if address_long else 78.6382    # Raleigh Longitude
        lot_size_sft = int(lot_size_sft) if lot_size_sft else 0
        tax_assessment = float(tax_assessment) if tax_assessment else 0.0
        total_rooms = float(total_rooms) if total_rooms else 0.0
        year_built = int(year_built) if year_built else 2000                # Default Year Built = 2000


        df1 = pd.read_csv('Resources\\Zillow_data_65_clusters.csv')
        df1['log_zest'] = np.log10(df1['zestimate'])

        df2 = pd.read_csv('Resources\\Zillow_data_65_clusters_centers.csv')
        df2.columns = ['cluster', 'longitude', 'latitude', 'zestimate_average']

        center_lat = df2['latitude'].tolist()
        center_long = df2['longitude'].tolist()

        distance_list=[]

        # Calculate distance between input coords and each cluster center
        for i in range(len(center_lat)):
            t_lat = center_lat[i]
            t_long = center_long[i]

            distance = math.sqrt((address_lat-t_lat)**2 + (address_long-t_long)**2)
            distance_list.append(distance)

        df2['distance'] = distance_list

        # PUll out housing data for the closest cluster
        closest_cluster_df = df2[df2['distance'] == min(df2['distance'])]
        closest_cluster_temp1 = closest_cluster_df.drop('latitude', axis=1)
        closest_cluster_temp2 = closest_cluster_temp1.drop('longitude', axis=1)

        cluster_average = closest_cluster_temp2.iloc[0]['zestimate_average']
        df3 = pd.merge(closest_cluster_temp2, df1, on='cluster', how='left')
        price_list = df3['zestimate'].tolist()

        # Graph prices for the closest cluster
        #plt.hist(price_list)
        x = [1]*len(price_list)
        jittered_x = x + 0.1 * np.random.rand(len(x)) -0.05
        plt.figure(figsize=(10,10))
        plt.scatter(jittered_x,price_list,s=100,alpha=0.5)
        axes = plt.gca()
        axes.set_xlim([0, 2])
        axes.set_ylim([0, max(price_list)+50000])
        now_var = dt.now()
        random_value= random.randint(1,1000001)*10 + 12345
        #file_name=f".\\Images\\{now_var.strftime('%d%m%Y%H%M%S')}_{random_value}.png"
        file_name=f".\\static\\data\\Image.png"
        plt.savefig(file_name)
        return jsonify(file_name)
        #return jsonify(f'{calculated_price[0][0]}')
    return jsonify("blah")


if __name__ == "__main__":
    app.run(debug=True)
