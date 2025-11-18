import trains

def menu():
    cont = True
    option = ''
    stations = trains.get_all_stations()

    while (cont):
        print('''
        [1] List Metro Stations
        [2] Display Metro Map
        [3]
        [Q] Quit ''')
        
        option = input()

        if (option == '1'):
            trains.list_stations(stations)
        elif (option == '2'):
            # other stuff
            trains.print_station_map(stations)
        elif (option == '3'):
            print('3')
        elif (option == 'Q'):
            cont = False
        else:
            print('Invalid Input')

if __name__ == '__main__':
    menu()