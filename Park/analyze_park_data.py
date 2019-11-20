import pandas as pd
import googlemaps
from datetime import datetime
import pickle

df_parks = pd.read_csv('data/Parks/park_dtl.dbf.csv')

with open('gcp_api_key.pkl', 'rb') as handle:
    dict_api_key = pickle.load(handle)

api_key = dict_api_key['gcp_api_key']

gmaps = googlemaps.Client(key=api_key)

park_name = 'Gorman Avenue Park'

geocode_result = gmaps.geocode(park_name)

len(geocode_result)
geocode_result[0].keys()

## find all parks
parks_all = gmaps.places(query='', type='park', radius=10000) #radius is in meters

for p in parks_all['results']:
    if 'Park' not in p['name']:
        print(p['name'])
