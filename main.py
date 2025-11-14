import requests
import json
import matplotlib as plt
import pandas as pd

api_key = '91421952b2724860be5b514ccfdf48db'  # personal API Key
headers = {'api_key': api_key}

#url = 'https://api.wmata.com/' # base api url
#rail_req = 'Rail.svc/json/jStationsRD'
#train_req = 'TrainPositions/TrainPositions?contentType={json}'

# Specific codes for each metro line
linecodes = ['RD', 'YL', 'GR', 'BL', 'OR', 'SV']

# returns a list of station names/info for a given line
def get_stations(line):
    url = 'http://api.wmata.com/Rail.svc/json/jStations?LineCode='
    response = requests.get(url + line, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        #print(data)
        stops = []
        for  i in range(len(data['Stations'])):
            stops.append(data['Stations'][i])
        return stops
    else:
        print('still not working - ', response.status_code)
        return None


# prints the name, code, lines, and station
def list_stations(stations):

    for station in stations:
        lines = [station['LineCode1']]
        if station['LineCode2']:
            lines.append(station['LineCode2'])
        if station['LineCode3']:
            lines.append(station['LineCode3'])
        if station['LineCode4']:
            lines.append(station['LineCode4'])
        print(f"\nStation: {station['Name']} ({station['Code']})\nLine(s): {lines}\nAddress: {station['Address']['Street']}, {station['Address']['City']}, {station['Address']['State']}")

# prints a map of the given metro stations 
def print_station_map(stations):
    for station in stations:
        lat = station['Lat']
        lon = station['Lon']

# list of all the stations in the metro system
stations = []

for line in linecodes:
    stations = stations + get_stations(line)

# cuts out duplicate stations
unique_stations = []
seen_stations = []
for i in range(len(stations)):
    cur_stat_code = stations[i]['Code']
    if not(cur_stat_code in seen_stations):
        seen_stations.append(cur_stat_code)
        unique_stations.append(stations[i])


stations = unique_stations
#list_stations(stations)