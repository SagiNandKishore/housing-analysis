# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 18:13:17 2019

@author: oldsk

This code generates the clusters for the Zillow data, and iterates through the number of clusters to find the optimal cluster size.

The optimal cluster size is the one which generates clusters that have houses all close in price.

This is evaluated by calculating the standard deviation of housing zestimate values within the clusters and getting the average for each number n of clusters.


"""

#from mpl_toolkits import mplot3d

import matplotlib.pyplot as plt
import os
import time
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
#from mpl_toolkits.mplot3d import axes3d, Axes3D
import statistics

time_list = []
start_time = time.time()
time_list.append(time.time())

os.chdir("C:/Users/oldsk/Desktop/personal_dataviz/UNCRAL20190514DATA/Final Project")

# Read in csv
df1 = pd.read_csv('Zillow_data_20191023_(Raleigh Durham Cary).csv')

df1 = df1.dropna(subset=['zestimate'])

df1['log_zest'] = np.log10(df1['zestimate'])


fig = plt.figure()
plt.figure(figsize=(10,10))
#ax = plt.axes(projection='3d')

zdata = df1['zestimate'].tolist()
ydata = df1['latitude'].tolist()
xdata = df1['longitude'].tolist()

dim_type = '2d'

if dim_type == '3d':

    data = pd.DataFrame(
        {'0': xdata,
         'l': ydata,
         '2': zdata
        })

else:
    data = pd.DataFrame(
        {'0': xdata,
         'l': ydata
        })

#ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens')

# Use n_clusters=4 as the k value
# We can see from the plot above that there are 4 clusters

cluster_list = list(range(1, 101))

std_list = []
std_med = []
norm_std = []


range_list = []
range_med = []
norm_range = []


def remove_outlier(df):
  q1 = df['zestimate'].quantile(0.25)
  q3 = df['zestimate'].quantile(0.75)

  iqr = q3 - q1
  lower_bound  = q1 - (1.5  * iqr)
  upper_bound = q3 + (1.5 * iqr)

  out_df = df.loc[(df['zestimate'] > lower_bound) & (df['zestimate'] < upper_bound)]
  return out_df

def deoutlier_list(prices):
    prices = sorted(prices)
    q1, q3= np.percentile(prices,[25,75])
    iqr = q3 - q1
    lower_bound = q1 -(1.5 * iqr) 
    upper_bound = q3 +(1.5 * iqr)
    
    output_list = list(filter(lambda x: lower_bound <= x <= upper_bound, prices))
    return(output_list)

for cluster in cluster_list:
    print('Performing K means for', cluster, 'clusters.')
    kmeans = KMeans(n_clusters=cluster)
    kmeans.fit(data)
    
    # Predict the clusters
    predicted_clusters = kmeans.predict(data)
    
    df1['cluster'] = predicted_clusters
    
    # Remove outliers
    #df2 = df1.groupby("cluster")["zestimate"].quantile([0.05, 0.95]).unstack(level=1)
    #df2 = df1.groupby('cluster').apply(remove_outlier)
    
    temp_dict = {k: list(v) for k, v in df1.groupby('cluster')['zestimate']}
    
    temp_dict_2 = {}
    
    for i in range(len(temp_dict)):
        temp_dict_2[i] = deoutlier_list(temp_dict[i])
    
    #df2 = pd.Series(temp_dict_2, name='zestimate')
    
    temp_std = []
    temp_mean = []
    temp_range = []
    
    
    # Perform std/range calculations on each group (each list), get list of those stds/ranges, and get means
    for i in range(len(temp_dict_2)):
        temp_std.append(statistics.stdev(temp_dict_2[0]))
        temp_range.append(max(temp_dict_2[0]) - min(temp_dict_2[0]))
        temp_mean.append(sum(temp_dict_2[0])/len(temp_dict_2[0]))
        
        
    std_list.append(sum(temp_std)/len(temp_std))
    range_list.append(sum(temp_range)/len(temp_range))
    
        
    
    '''
    #price_group = df1.groupby('cluster')['zestimate']
    price_group_avg = df1.groupby('cluster')['zestimate'].mean()
    price_group_std = df1.groupby('cluster')['zestimate'].std()
    
    #normalized_std = [int(s) / int(a) for s,a in zip(price_group_std, price_group_avg)]
    
    price_group_count = df1.groupby('cluster')['zestimate'].count()
    price_group_min = df1.groupby('cluster')['zestimate'].min()
    price_group_max = df1.groupby('cluster')['zestimate'].max()
    
    std_range = price_group_max - price_group_min
    
    #normalized_range = [int(r) / int(a) for r,a in zip(std_range, price_group_avg)]
    
    range_average = std_range.mean()
    range_median = statistics.median(std_range)
    range_med.append(range_median)
    range_list.append(range_average)
    
    #norm_range_avg = np.mean(normalized_range)
    #norm_range.append(norm_range_avg)
    
    std_average = price_group_std.mean()
    std_median = statistics.median(price_group_std)
    std_list.append(std_average)
    std_med.append(std_median)
    
    #norm_std_avg = np.mean(normalized_std)
    #norm_std.append(norm_std_avg)
    '''

# Remove outliers from groups to get non-outlier averages
# Return histogram of prices in that group, list of prices, min, max


cluster_export = pd.DataFrame(
        {'average range':range_list,
         'average std':std_list}
        )

#cluster_export.to_csv('cluster_optimization.csv', encoding='utf-8')


'''
# The below generates the files for the specified cluster numbersize
# Optimal cluster size is 65
    
clusters = 65
    
kmeans = KMeans(n_clusters=clusters)
kmeans.fit(data)

# Predict the clusters
predicted_clusters = kmeans.predict(data)

df1 = pd.read_csv('Zillow_data_20191023_(Raleigh Durham Cary).csv')

df1 = df1.dropna(subset=['zestimate'])
df1 = df1.reset_index(drop=True)

df1['cluster'] = predicted_clusters

#df1['cluster_price_avg'] = df1.groupby(['cluster'])['zestimate'].mean() # Not working for some reason


export_means = []

for k in range(0, 65):
    #print(k)
    temp_df = df1[df1['cluster'] == k]
    temp_mean = temp_df['zestimate'].mean()
    #print(temp_mean)
    export_means.append(temp_mean)

# Print the cluster centers and cluster labels
centers = kmeans.cluster_centers_
center_df = pd.DataFrame({'longitude': centers[:, 0], 'latitude': centers[:, 1]})
center_df['zestimate_average'] = export_means
#labels = kmeans.labels_


plt.figure(figsize=(12,12))
plt.scatter(xdata, ydata, c=predicted_clusters, s=100, cmap='coolwarm') # coolwarm
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=50, marker='X')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

df1['cluster'] = predicted_clusters

#price_group = df1.groupby('cluster')['zestimate']
price_group_avg = df1.groupby('cluster')['zestimate'].mean()
price_group_std = df1.groupby('cluster')['zestimate'].std()
price_group_count = df1.groupby('cluster')['zestimate'].count()
price_group_min = df1.groupby('cluster')['zestimate'].min()
price_group_max = df1.groupby('cluster')['zestimate'].max()
std_average = price_group_std.mean()


#df1.to_csv('Zillow_data_65_clusters.csv', encoding='utf-8')
#center_df.to_csv('Zillow_data_65_clusters_centers.csv', encoding='utf-8')
'''
print ("\n\nTotal runtime: --- %s seconds ---" % round((time.time() - start_time), 1))  