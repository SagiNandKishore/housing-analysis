# 1. import Flask
from flask import Flask, request
import pickle
import pandas as pd

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


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


        X_Score_df = pd.DataFrame(columns = ['bathrooms','bedrooms','finishedSqFt','lastSoldPrice','latitude','longitude','lotSizeSqFt','taxAssessment','totalRooms','yearBuilt'])
        X_Score_df = [[num_baths, num_bedrooms, sft, last_sold_price, address_lat, address_long, lot_size_sft, tax_assessment, total_rooms, year_built]]
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

            <input type="submit" formtarget = "_blank">
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
