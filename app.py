# 1. import Flask
from flask import Flask, request
import pickle
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import random

IMAGES_FOLDER = ".\\Images"
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMAGES_FOLDER

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return "Blank Page!"


# 4. Define what to do when a user hits the /about route
@app.route("/getLREGValue", methods = ['POST', 'GET'])
def get_lreg_value():
    if request.method == 'POST':
        lreg_model = pickle.load(open("lreg_model\LinearRegression.pkl", "rb"))
        
        num_bedrooms = request.form.get("num_bedrooms")
        num_baths = request.form.get("num_baths")
        sft = request.form.get("sft")
        last_sold_price = request.form.get("last_sold_price")
        address_lat = request.form.get("lat")
        address_long = request.form.get("long")
        lot_size_sft = request.form.get("lot_size_sft")
        tax_assessment = request.form.get("tax_assessment")
        total_rooms = request.form.get("total_rooms")
        year_built = request.form.get("year_built")
        zip_code = request.form.get("zip_code")

        num_bedrooms = int(num_bedrooms) if num_bedrooms else 0
        num_baths = float(num_baths) if num_baths else 0.0                  # Account for half baths
        sft = float(sft) if sft else 0.0
        last_sold_price = float(last_sold_price) if last_sold_price else 0.0
        #address_lat = float(address_lat) if address_lat else 35.7796       # Raleigh Latitude
        #address_long = float(address_long) if address_long else 78.6382    # Raleigh Longitude
        lot_size_sft = int(lot_size_sft) if lot_size_sft else 0
        tax_assessment = float(tax_assessment) if tax_assessment else 0.0
        total_rooms = float(total_rooms) if total_rooms else 0.0
        year_built = int(year_built) if year_built else 2000                # Default Year Built = 2000
        zip_code = int(zip_code) if zip_code else 27519

        X_Score_df = pd.DataFrame(columns = ['bathrooms','bedrooms','finishedSqFt','lastSoldPrice','lotSizeSqFt','taxAssessment','totalRooms','yearBuilt', 'zip_code'])
        X_Score_df = [[num_baths, num_bedrooms, sft, last_sold_price, lot_size_sft, tax_assessment, total_rooms, year_built, zip_code]]
        caluclated_price = lreg_model.predict(X_Score_df)

        return f'Predicted Price is {caluclated_price}'

    return '''
        <form method = 'POST'>
            <label for = "01" style="display:block;">Number of Bedrooms</label>
            <input id = "01" type = "text" name = "num_bedrooms" style="display:block">
            <br />

            <label for = "02" style="display:block">Number of Bathrooms</label>
            <input id = "02" type = "text" name = "num_baths" style="display:block">
            <br />

            <label for = "03" style="display:block">Finished Square Footage</label>
            <input id = "03" type = "text" name = "sft" style="display:block">
            <br />

            <label for = "05" style="display:block">Last Sold Price</label>
            <input id = "05" type = "text" name = "last_sold_price" style="display:block">
            <br />

            <label for = "06" style="display:block">Latitude</label>
            <input id = "06" type = "text" name = "lat" style="display:block">
            <br />

            <label for = "07" style="display:block">Longitude</label>
            <input id = "07" type = "text" name = "long" style="display:block">
            <br />

            <label for = "08" style="display:block">Lot Size Square Footage</label>
            <input id = "08" type = "text" name = "lot_size_sft" style="display:block">
            <br />

            <label for = "09" style="display:block">Tax Assessment</label>
            <input id = "09" type = "text" name = "tax_assessment" style="display:block">
            <br />

            <label for = "10" style="display:block">Total Rooms</label>
            <input id ="10" type = "text" name = "total_rooms" style="display:block">
            <br />

            <label for = "11" style="display:block">Year Built</label>
            <input id = "11" type = "text" name = "year_built" style="display:block">
            <br />

            <label for = "12" style="display:block">Zip Code</label>
            <input id = "12" type = "text" name = "zip_code" style="display:block">
            <br />

            <input type="submit" formtarget = "_blank">
        </form>
    '''

@app.route("/getKMeansValue", methods = ['POST', 'GET'])
def get_kmeans_value():
    if request.method == 'POST':

        num_bedrooms = request.form.get("num_bedrooms")
        num_baths = request.form.get("num_baths")
        sft = request.form.get("sft")
        last_sold_price = request.form.get("last_sold_price")
        address_lat = request.form.get("lat")
        address_long = request.form.get("long")
        lot_size_sft = request.form.get("lot_size_sft")
        tax_assessment = request.form.get("tax_assessment")
        total_rooms = request.form.get("total_rooms")
        year_built = request.form.get("year_built")
        zip_code = request.form.get("zip_code")

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
        zip_code = int(zip_code) if zip_code else 27519

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
        file_name=f".\\Images\\Image.png"
        plt.savefig(file_name)
        return file_name


    return '''
        <form method = 'POST'>
            <label for = "01" style="display:block;">Number of Bedrooms</label>
            <input id = "01" type = "text" name = "num_bedrooms" style="display:block">
            <br />

            <label for = "02" style="display:block">Number of Bathrooms</label>
            <input id = "02" type = "text" name = "num_baths" style="display:block">
            <br />

            <label for = "03" style="display:block">Finished Square Footage</label>
            <input id = "03" type = "text" name = "sft" style="display:block">
            <br />

            <label for = "05" style="display:block">Last Sold Price</label>
            <input id = "05" type = "text" name = "last_sold_price" style="display:block">
            <br />

            <label for = "06" style="display:block">Latitude</label>
            <input id = "06" type = "text" name = "lat" style="display:block">
            <br />

            <label for = "07" style="display:block">Longitude</label>
            <input id = "07" type = "text" name = "long" style="display:block">
            <br />

            <label for = "08" style="display:block">Lot Size Square Footage</label>
            <input id = "08" type = "text" name = "lot_size_sft" style="display:block">
            <br />

            <label for = "09" style="display:block">Tax Assessment</label>
            <input id = "09" type = "text" name = "tax_assessment" style="display:block">
            <br />

            <label for = "10" style="display:block">Total Rooms</label>
            <input id ="10" type = "text" name = "total_rooms" style="display:block">
            <br />

            <label for = "11" style="display:block">Year Built</label>
            <input id = "11" type = "text" name = "year_built" style="display:block">
            <br />

            <label for = "12" style="display:block">Zip Code</label>
            <input id = "12" type = "text" name = "zip_code" style="display:block">
            <br />

            <input type="submit" formtarget = "_blank">
        </form>
    '''






if __name__ == "__main__":
    app.run(debug=True)
