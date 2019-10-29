# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 22:24:29 2019

@author: oldsk
"""

import os
import time
import pandas as pd
import math
import matplotlib.pyplot as plt

time_list = []
start_time = time.time()
time_list.append(time.time())

os.chdir("C:/Users/oldsk/Desktop/personal_dataviz/UNCRAL20190514DATA/Final Project")

# Read in csvs
df1 = pd.read_csv('Zillow_data_65_clusters.csv')

df1['log_zest'] = np.log10(df1['zestimate'])

df2 = pd.read_csv('Zillow_data_65_clusters_centers.csv')
df2.columns = ['cluster', 'longitude', 'latitude', 'zestimate_average']

input_lat = 35.9798
input_long = -78.9972

center_lat = df2['latitude'].tolist()
center_long = df2['longitude'].tolist()

distance_list = []

# Calculate distance between input coords and each cluster center
for i in range(len(center_lat)):
    t_lat = center_lat[i]
    t_long = center_long[i]

    distance = math.sqrt((input_lat-t_lat)**2 + (input_long-t_long)**2)

    distance_list.append(distance)

df2['distance'] = distance_list



# PUll out housing data for the closest cluster
closest_cluster_df = df2[df2['distance'] == min(df2['distance'])]
closest_cluster_df.drop('latitude', axis=1, inplace=True)
closest_cluster_df.drop('longitude', axis=1, inplace=True)

cluster_average = closest_cluster_df.iloc[0]['zestimate_average']

df3 = pd.merge(closest_cluster_df, df1, on='cluster', how='left')

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


'''
The below is strictly for graphing

df_ral = df1[df1['city'] == 'Raleigh']
df_dur = df1[df1['city'] == 'Durham']
df_cary = df1[df1['city'] == 'Cary']

scaling = 5000
trans = 0.2

plt.figure(figsize=(12,12))
plt.scatter(df_ral['longitude'], df_ral['latitude'], s=df_ral['zestimate']/scaling, alpha = trans)
plt.scatter(df_dur['longitude'], df_dur['latitude'], s=df_dur['zestimate']/scaling, alpha = trans)
plt.scatter(df_cary['longitude'], df_cary['latitude'], s=df_cary['zestimate']/scaling, alpha = trans)





plt.scatter(df_ral['longitude'], df_ral['latitude'], s=df_ral['zestimate']/scaling, alpha = trans)
plt.scatter(df_dur['longitude'], df_dur['latitude'], s=df_dur['zestimate']/scaling, alpha = trans)
plt.scatter(df_cary['longitude'], df_cary['latitude'], s=df_cary['zestimate']/scaling, alpha = trans)



plt.scatter(df_ral['longitude'], df_ral['latitude'], s=df_ral['log_zest']*scaling)
plt.scatter(df_dur['longitude'], df_dur['latitude'], s=df_dur['log_zest']*scaling)
plt.scatter(df_cary['longitude'], df_cary['latitude'], s=df_cary['log_zest']*scaling)


plt.figure(figsize=(12,12))
plt.scatter(df1['longitude'], df1['latitude'], s=100, c=df1['log_zest'], cmap='inferno')

plt.scatter(df1['longitude'], df1['latitude'], c=df1['zestimate'], cmap='inferno')

'''


print ("\n\nTotal runtime: --- %s seconds ---" % round((time.time() - start_time), 1))  