# -*- coding: utf-8 -*-
"""AIS_Disabling_Pre_Processing_Final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1x3AK7nEomdFRIs1QQYgBS3RvL2FMrJbM
"""

import pandas as pd

import io
 
df = pd.read_csv("ais_disabling_events_main_csv.csv")
print(df.head())

"""### **AIS Disabling in EEZ**"""

# did ais get disabled in eez (dist from shore) (check length of eez from google 200 nautical miles to km)

gap_start_distance_from_shore_m = df['gap_start_distance_from_shore_m'].tolist()

eez_check = []
for x in gap_start_distance_from_shore_m:
  if x > 370400:
    eez_check.append(0)
  else:
    eez_check.append(1)

import pandas as pd

column_name = "eez_check"

df_eez = pd.DataFrame(eez_check, columns = [column_name])
df_eez.head()

df_eez.to_csv("eez_check.csv")

"""### **Distance Traversed during AIS disabling event**"""

# distance traversed during ais disabling event

import numpy as np
import pandas as pd
from math import radians, cos, sin, asin, acos, sqrt, pi
from geopy import distance
from geopy.geocoders import Nominatim
import networkx as nx

def calculate_spherical_distance(lat1, lon1, lat2, lon2, r=6371):
    # Convert degrees to radians
    coordinates = lat1, lon1, lat2, lon2
    # radians(c) is same as c*pi/180
    phi1, lambda1, phi2, lambda2 = [
        radians(c) for c in coordinates
    ]  
    
    # Apply the haversine formula
    a = (np.square(sin((phi2-phi1)/2)) + cos(phi1) * cos(phi2) * 
         np.square(sin((lambda2-lambda1)/2)))
    d = 2*r*asin(np.sqrt(a))
    return d

gap_start_lat = list(df['gap_start_lat'])
gap_start_lon = list(df['gap_start_lon'])
gap_end_lat = list(df['gap_end_lat'])
gap_end_lon = list(df['gap_end_lon'])

spherical_distances = []

for i in range(len(gap_start_lat)):
  spherical_distances.append(calculate_spherical_distance(
      gap_start_lat[i],
      gap_start_lon[i],
      gap_end_lat[i],
      gap_end_lon[i]
  ))

spherical_distances[:5]

import pandas as pd

column_name = "spherical_distances"

df_dist = pd.DataFrame(spherical_distances, columns = [column_name])
df_dist.head()

df_dist.to_csv("distance_traversed.csv")

"""### **CHECK POINT IN FAO JSON**"""

!pip install streamlit
!pip install geojson

# import streamlit as st
import pandas as pd
import geojson
import folium
# from streamlit_folium import st_folium
from shapely.geometry import Point, MultiPolygon
import re

with open('FAO_AREAS_CWP.json') as f:
    geojson_file = geojson.load(f)

from shapely.geometry import Point, Polygon

ocean_list = []

def identify_ocean(longitude, latitude):
  # Creating a Shapely point from the longitude and latitude (first long then lat VERY IMP)
  point = Point(longitude, latitude)

  # Iterating through the features in the GeoJSON file
  for feature in geojson_file['features']:
    # Checking if the point is within the polygon defined by the feature
    if Point(point).within(Polygon(feature['geometry']['coordinates'][0][0])):
      print(feature['properties']['OCEAN'])
      return feature['properties']['OCEAN']
  
  # If point is in none of the oceans return false
  return False

# make list of all the lat and long of all the ais disabling events
gap_start_lat = df['gap_start_lat'].tolist()
gap_start_lon = df['gap_start_lon'].tolist()

for i in range(len(gap_start_lon)):
  temp = identify_ocean(gap_start_lon[i], gap_start_lat[i])
  ocean_list.append(temp)


print(ocean_list[:5])

import pandas as pd

column_name = "oceans_list"

df = pd.DataFrame(ocean_list, columns = [column_name])
df.head()

df.to_csv("csv_name.csv")