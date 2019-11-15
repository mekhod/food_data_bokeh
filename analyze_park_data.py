import pandas as pd

df_parks = pd.read_csv('data/Parks/park_dtl.dbf.csv')

df_parks.shape

df_parks[1000:1100]

import requests

park_name = 'Gorman Avenue Park'

response = requests.get("""https://maps.googleapis.com/maps/api/geocode/json?address={}""".format(park_name))

resp_json_payload = response.json()

print(resp_json_payload['results'][0]['geometry']['location'])