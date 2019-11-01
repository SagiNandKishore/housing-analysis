# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 11:08:17 2019

@author: AChao
"""

#import zillow
#import pyzillow
#from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults

import os
import time
import pandas as pd
import json
import requests
import xmltodict

from time import sleep



time_list = []
start_time = time.time()
time_list.append(time.time())

key = "X1-ZWz1hfncvwesqz_2hwdv"

#os.chdir("C:/users/achao/OneDrive - Environmental Protection Agency (EPA)/profile/Desktop/pythontemp/zillow api")
os.chdir("C:/Users/oldsk/Desktop/personal_dataviz/UNCRAL20190514DATA/Final Project")

# Read in xlsx, only one sheet present
address_file = "Durham Zillow results.xlsx"
df1 = pd.read_excel(address_file)

address_list = df1['address'].tolist()
address_list = address_list[1:10]

# Save config information
#url = "http://www.zillow.com/webservice/GetSearchResults.htm?"
url = "http://www.zillow.com/webservice/GetDeepSearchResults.htm?"
citystate = "Durham NC"


def search_zillow(input_address):
    
    temp_url = url + "zws-id=" + key + "&address=" + input_address + "&citystatezip=" + citystate
    property_response = requests.get(temp_url)
    print('Querying address:', input_address, '- Response is:', property_response)
    
    # Convert the xml to a json
    o = xmltodict.parse(property_response.text)
    xml_json = json.dumps(o)
    temp_json = json.loads(xml_json)
    
    # Convert json to a dataframe
    temp_df = json_to_df(temp_json, input_address)
    
    return(temp_df)
    
# Convert the json file to a dataframe
def json_to_df(input_json, input_address):
    df_list = []
    
    try:
        df1 = pd.DataFrame.from_dict([input_json['SearchResults:searchresults']['response']['results']['result']['address']])
        df_list.append(df1)
    except:
        print('Address info not found')

    try:
        df2 = pd.DataFrame.from_dict([input_json['SearchResults:searchresults']['response']['results']['result']['zestimate']['amount']])
        df2.rename(columns={'#text':'zestimate'}, inplace=True) 
        df2 = df2.drop('@currency', 1)
        df_list.append(df2)
    except:
        print('Zestimate data not found')

    try:
        df3 = pd.DataFrame.from_dict([input_json['SearchResults:searchresults']['response']['results']['result']['localRealEstate']['region']])
        df_list.append(df3)
    except:
        print('localRealEstate data not found')
    
    df_debug = pd.DataFrame.from_dict([input_json['SearchResults:searchresults']['response']['results']['result']])
    
    try:
        df4 = pd.DataFrame.from_dict([input_json['SearchResults:searchresults']['response']['results']['result']])
        #df_debug = pd.DataFrame.from_dict([input_json['SearchResults:searchresults']['response']['results']['result']])
        #df4 = df4.drop(['address', 'lastSoldPrice', 'links', 'localRealEstate', 'zestimate'], 1)
        df4 = try_drop_columns(df4, ['address', 'lastSoldPrice', 'links', 'localRealEstate', 'zestimate'])
        df_list.append(df4)
    except:
        print('Result data not found')
    

    try:
        df5 = pd.DataFrame.from_dict([input_json['SearchResults:searchresults']['response']['results']['result']['lastSoldPrice']])
        df5.rename(columns={'#text':'lastSoldPrice'}, inplace=True) 
        df5 = df5.drop('@currency', 1)
        df_list.append(df5)
    except:
        print('lastSoldPrice info not found')    

    if len(df_list) > 0:
        count = 1
        for df in df_list:
            if count == 1:
                return_df = df
            else:
                return_df = return_df.join(df, how='outer')
            count += 1
    else:
        data = {'street':[input_address]}
        return_df = pd.DataFrame(data)
    return(return_df)
    #return(df_debug)
    
#test_df = search_zillow(address_list[0])    

delay_list = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750]
#delay_list = []

# Iterate through list of addresses, hitting zillow API for each one and storing in df_all dataframe
def process_addresses(input_addresses):
    counter = 1
    for place in input_addresses:
        
        # Delay 1 minute every 50 api calls just in case zillow monitors traffic
        if counter in delay_list:
            print('Delaying for 1 minute, at counter', counter)
            sleep(60)
        
        
        
        if counter == 1:
            df = search_zillow(place)
        else:
            temp_df = search_zillow(place)
            df = pd.concat([df, temp_df])
        counter += 1
        
    return(df)

#df_all = process_addresses(address_list)

# Drop columns that are not needed
def try_drop_columns(input_df, drop_columns):
    for column in drop_columns:
        try:
            input_df = input_df.drop([column], 1)
        except:
            pass
    return(input_df)




def search_debug(input_address):
    
    temp_url = url + "zws-id=" + key + "&address=" + input_address + "&citystatezip=" + citystate
    property_response = requests.get(temp_url)
    print('Querying address:', input_address, '- Response is:', property_response)
    
    # Convert the xml to a json
    o = xmltodict.parse(property_response.text)
    xml_json = json.dumps(o)
    temp_json = json.loads(xml_json)
    
    return(temp_json)

debug = search_debug(address_list[1])


# Export dataframe to csv
#df_all.to_csv('Raleigh_zillow_temp.csv', sep=',', encoding='utf-8', index=False)

    
print ("\n\nTotal runtime: --- %s seconds ---" % round((time.time() - start_time), 1))    