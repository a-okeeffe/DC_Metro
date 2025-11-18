import trains
import re

def menu():
    cont = True
    option = ''
    stations = trains.get_all_stations()

    while (cont):
        print('''
        [1] List Metro Stations
        [2] Display Metro Map
        [3] Station Lookup
        [Q] Quit ''')
        
        option = input()

        if (option == '1'):
            trains.list_stations(stations)
        elif (option == '2'):
            # other stuff
            trains.print_station_map(stations)
        elif (option == '3'):
            print('Which station would you like to look up? Please enter the station code')
            print('(station codes can be found under \'List Metro Stations\')')
            code = input()
            match = re.search(r'[A-N][0-1][0-9]', code)
            if match:
                trains.station_lookup(code)
            else:
                print('Invalid Station Code')

        elif (option == 'Q'):
            cont = False
        else:
            print('Invalid Input')

if __name__ == '__main__':
    menu()