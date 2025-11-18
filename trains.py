import requests
import json
import matplotlib.pyplot as plt
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
def list_stations(stations_df):
    df_copy = stations_df[['Code', 'Name', 'Address']].copy(deep=True)
    print(df_copy)
    
# prints a map of the given metro stations 
def print_station_map(df):
    # set up the scatterplot with appropriate axis scales
    plt.scatter(df['Lon'], df['Lat'])
    #list of line codes with associated colors
    lines = [('RD', 'red'), ('YL', 'yellow'), ('GR', 'green'), ('BL', 'blue'), ('OR', 'orange'), ('SV', 'grey')]
    for line in lines:
        coords = df[(df['LineCode1'] == line[0]) | (df['LineCode2'] == line[0]) | (df['LineCode3'] == line[0])][['Lat','Lon']]
        plt.scatter(coords['Lon'], coords['Lat'], color=line[1])
    plt.show()

def get_all_stations():
    stations = []

    for line in linecodes:
        stations = stations + get_stations(line)
    # pandas dataframe implementation. Easier to work with + removes duplicates
    df = pd.DataFrame(stations)
    #  fix the addresses from being a separate object
    addies = pd.json_normalize(df.Address)
    df = pd.concat([df, addies], axis=1)
    df = df.drop('Address', axis = 1)

    return df








