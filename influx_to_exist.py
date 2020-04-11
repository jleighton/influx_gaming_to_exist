import requests
import json
import datetime
from datetime import datetime
from datetime import timedelta
import os
import requests
import config_influx

today = datetime.today()

#Exist API endpoint
exist_url = 'https://exist.io/api/1/attributes/update/'
#Content type must be included in the header for Influx
header = {"content-type": "application/x-www-form-urlencoded"}

i=0

while i < 3:
        date = today - timedelta(days=i)
        date = date.strftime('%Y-%m-%d')
        response=requests.post(config_influx.influx_url,data="q=SELECT SUM(value) FROM \"time\" WHERE \"time\" >= '" + date + "T00:00:00Z' AND \"time\" <= '" + date + "T23:59:59Z'", headers=header, verify=False)
        json_data = response.json()

        x = json_data["results"]

        try:
                value = (x[0]["series"][0]["values"][0][1])
                value = value / 60

                data = dict(
                        date=date,
                        value=value,
                        name="gaming_min" )
                payload = json.dumps(data)
                update = requests.post(exist_url, headers={'Authorization':'Bearer '+config_influx.ACCESS_TOKEN,'Content-Type': 'application/json'},data=payload)
                print (update.json())

        except KeyError:
                data = dict(
                        date=date,
                        value=0,
                        name="gaming_min" )

                payload = json.dumps(data)
                update = requests.post(exist_url, headers={'Authorization':'Bearer '+config_influx.ACCESS_TOKEN, 'Content-Type': 'application/json'}, data=payload)
                print (update.json())
        i = i +1
