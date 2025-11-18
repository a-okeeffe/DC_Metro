import trains

cont = True
option = ''

while (cont):
    print('''
          [1] Display Metro Map
          [2]
          [3]
          [Q] Quit ''')
    
    option = input()

    if (option == '1'):
        trains.print_station_map(trains.get_all_stations())
    elif (option == '2'):
        # other stuff
        print('2')
    elif (option == '3'):
        print('3')
    elif (option == 'Q'):
        cont = False
    else:
        print('Invalid Input')