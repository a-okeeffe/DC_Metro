import requests
import json
import matplotlib.pyplot as plt
import pandas as pd

api_key = '91421952b2724860be5b514ccfdf48db'  # personal API Key
headers = {'api_key': api_key}

#url = 'https://api.wmata.com/' # base api url
#rail_req = 'Rail.svc/json/jStationsRD'
#train_req = 'TrainPositions/TrainPositions?contentType={json}'

# returns a list of station names/info for a given line (line should be in the form of a linecode)
def get_stations(line):
    url = 'http://api.wmata.com/Rail.svc/json/jStations?LineCode='
    response = requests.get(url + line, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        stops = []
        for  i in range(len(data['Stations'])):
            stops.append(data['Stations'][i])
        return stops
    else:
        print('Error', response.status_code)
        return None

# creates a dataframe from info of every line in the metro system
def get_all_stations():
    # Specific codes for each metro line
    linecodes = ['RD', 'YL', 'GR', 'BL', 'OR', 'SV']
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

# prints the station name and address for the given stations
# input must be a dataframe with at least Code, Name, Street, City, and State fields
def list_stations(stations_df):
    df_copy = stations_df[['Code', 'Name', 'Street', 'City', 'State']].copy(deep=True)
    for i, row in df_copy.iterrows():
        print(f'Station: {row['Name']}')
        print(f'Station Code: {row['Code']}')
        print(f'Address: {row['Street']}, {row['City']}, {row['State']}')
        print('---')
    
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

# finds the name of a station along with trains en route + their destinations
def station_lookup(station_code):
    url = 'http://api.wmata.com/StationPrediction.svc/json/GetPrediction/'
    response = requests.get(url + station_code, headers=headers)

    if response.status_code != 200:
        print('Error', response.status_code)
        return None
    data = json.loads(response.text)
    incoming_trains = []
    for  i in range(len(data['Trains'])):
        incoming_trains.append(data['Trains'][i])
    incoming_trains_df = pd.DataFrame(incoming_trains)
    
    url = 'http://api.wmata.com/Rail.svc/json/jStationInfo?StationCode='
    response = requests.get(url + station_code, headers=headers)

    if response.status_code != 200:
        print('Error', response.status_code)
        return None
    data = json.loads(response.text)
    print(f'{station_code} is {data['Name']}')

    for i, row in incoming_trains_df.iterrows():
        if (row['DestinationName'] == 'No Passenger'):
            continue
        if row['Min'].isdigit():
            print(f'In {row['Min']} minutes a train is arriving at {data['Name']}, headed for {row['DestinationName']}')
        else:
            print(f'Train is {row['Min']} at {data['Name']}, headed for {row['DestinationName']}')
      

if __name__ == '__main__':
    list_stations(get_all_stations())








