import pandas as pd
import json, sys, os
from datastructures import *
from urllib import request
import threading
from time import sleep

Systems = {}
Commodities = {}
Stations = {}
Listings = []
toprint = []
loading = False
finished = False

def write(text):
    toprint.append(text)

def print_handler():
    global toprint
    global loading
    loading_status = '|'
    while True:
        if finished:
            break
        if len(toprint) > 0:
            print(f"\r{toprint[0]}")
            del toprint[0]
        if loading:
            print(f"\r{loading_status}", end='')
            loading_status = ("|" if loading_status == '\\' else ("\\" if loading_status == '-' else ("-" if loading_status == '/' else '/')))
        sleep(0.1)

print_handler_thread = threading.Thread(target=print_handler)
print_handler_thread.name = "Printhandler"
print_handler_thread.start()

def _requ(end):
    url = f"https://eddb.io/archive/v6/{end}"
    return request.urlopen(url)

def get_css():
    global Listings
    write('Started Css')
    if os.path.exists("data/Listings.json"):
        write("Reading from file...")
        with open("data/Listings.json", "r") as f:
            Listings = json.load(f)
        write('Css finsihed from file')
        return
    write("Downloading data")
    tmp = _requ('listings.csv').read().decode('utf-8').split('\n')
    write('Data downloaded')
    del tmp[0]
    for item in tmp:
        if item == '':
            continue
        sp = item.split(',')
        del sp[4], sp[8]
        Listings.append(sp)
    write('Data finished')
    write("Writing file")
    with open("data/Listings.json", 'w') as f:
        json.dump(Listings, f)
    write('Data saved')
    del tmp

def get_jsons(what):
    return json.loads(_requ(what).read())

def systems():
    global Systems
    tmp = get_jsons('systems_populated.json')
    write('Systems downloaded.')
    for i in tmp:
        Systems[i['id']] = System(i['name'], i['x'], i['y'], i['z'], i['population'], i['security'])
    write('Systems finished')
    del tmp

def stations():
    global Stations
    tmp = get_jsons('stations.json')
    write('Stations downloaded.')
    for i in tmp:
        Stations[i['id']] = Station(i['name'], i['system_id'], i['max_landing_pad_size'], i['has_docking'], i['has_commodities'])
    write('Stations finished')
    del tmp

def commodities():
    global Commodities
    tmp = get_jsons('commodities.json')
    write('Commodities downloaded.')
    for i in tmp:
        Commodities[i['id']] = Commoditie(i['name'], i['is_rare'], i['max_buy_price'], i['max_sell_price'], i['min_buy_price'], i['min_sell_price'])
    write('Commodities finished.')
    del tmp

def populate():
    systems_thread = threading.Thread(target=systems)
    stations_thread = threading.Thread(target=stations)
    commodities_thread = threading.Thread(target=commodities)
    systems_thread.name = "Systems"
    stations_thread.name = "Stations"
    commodities_thread.name = "Commodities"
    systems_thread.start()
    stations_thread.start()
    commodities_thread.start()
    global loading
    loading = True
    get_css()
    while stations_thread.is_alive() or systems_thread.is_alive() or commodities_thread.is_alive():
        pass
    loading = False

def clear():
    os.system('cls' if os.name == "nt" else 'clear')

def reader(max):
    inp = ""
    while True:
        try:
            inp = int(input(": "))
            if inp > max:
                print('Only use the numbers abowe!')
            else:
                return inp
        except:
            print('Use only numbers!')

def search_system(inp=None):
    import vector
    clear()
    print('=====Search for system=====')
    if inp == None:
        inp = input("Type in the system's name: ")
    options = []
    for system in Systems.values():
        if comparer(system.name, inp, 80):
            options.append(system)
    if len(options) > 1:
        print("Select from the list below")
        for i, system in enumerate(options):
            print(f"{i + 1}. {system}'s Distance from Sol: {system.Distance(vector.vector(0,0,0))}")
        print("0. exit")
        ansv = reader(len(options) + 1)
        if ansv == 0:
            return
        else:
            print(f"Stations in {options[ansv - 1]}")
            for station in Stations.values():
                if Systems[station.system_id] == options[ansv - 1]:
                    co = ('has' if station.has_commodities else "doesn't have")
                    print(f"{station.name} max pad: {station.max_landing} and {co} commodities market.")
    elif len(options) == 1:
        print(f"Stations in {options[0]}")
        for station in Stations.values():
            if Systems[station.system_id] == options[0]:
                co = ('has' if station.has_commodities else "doesn't have")
                print(f"{station.name} max pad: {station.max_landing} and {co} commodities market.")
    else:
        print("No system found!")
    input('...Press return to return...')

def search_station(inp=None):
    import vector
    clear()
    print('=====Search for station=====')
    if inp == None:
        inp = input("Type in the station's name: ")
    for station in Stations.values():
        if comparer(station.name, inp, 80):
            print(f"The {station.name} station is in the {Systems[station.system_id]} system, that is {Systems[station.system_id].Distance(vector.vector(0,0,0))} ly's away from Sol.")
    input('...Press return to return...')

def search_for_lowest():
    """
               0       1         2          3       4         5          6         7
    Listings: ID, StationID, CommodityID, Suply, BuyPrice, SellPrice, Demand, CollectedAt
    """
    id = None
    global loading
    global Commodities
    loading = True
    id = 1
    while True:
        for key, item in Commodities.items():
            try:
                if item.min_buy < Commodities[id].min_buy and item.max_sell > Commodities[id].max_sell:
                    id = key
            except:
                pass
        write(f"Best commoditie: {Commodities[id].name}")
        best = Commodities[id]
        best_buy = []
        best_sell = []
        for item in Listings:
            if int(item[2]) == int(id):
                if int(item[4]) == int(best.min_buy):
                    best_buy = item
                elif int(item[5]) == int(best.max_sell):
                    best_sell = item
        write(f'The best buy is at {Stations[int(best_buy[1])]} in the {Systems[Stations[int(best_buy[1])].system_id]} system. It has {best_buy[3]} t suply.')
        write(f'The best sell is at {Stations[int(best_sell[1])]} in the {Systems[Stations[int(best_sell[1])].system_id]} system. It has {best_sell[6]} t demand')
        loading = False
        write(f"The distance between the two system is {Systems[int(Stations[int(best_sell[1])].system_id)].Distance(Systems[int(Stations[int(best_buy[1])].system_id)])}")
        write(f"Min sell: {Commodities[id].min_buy}")
        write(f"Max buy: {Commodities[id].max_sell}")
        break
    input('...Press return to return...')


def comparer(fix, usrinp, perc):
    good = 0
    for char in fix.lower():
        if len(usrinp) > good+1 and char == usrinp.lower()[good]:
            good += 1
    perc = ((len(usrinp) / 100 + len(fix) / 100) / 2) * perc
    if good >= perc:
        return True
    return False

def main():
    global finished
    print('Downloading data...')
    populate()
    while True:
        clear()
        print('=====Main menu=====')
        keys = list(functions.keys())
        for i, key in enumerate(functions.keys()):
            print(f"{i+1} {key}")
        print('0 Exit')
        print('-1 Test')
        ansv = reader(len(keys) + 1)
        if ansv == 0:
            finished = True
            exit(0)
        elif ansv == -1:
            test()
        else:
            functions[keys[ansv-1]]()

def test():
    from datetime import datetime
    start = datetime.now()
    populate()
    print(f"Station_count: {len(Stations)}")
    print(f"System_count: {len(Systems)}")
    print(f"Commodity_count: {len(Commodities)}")
    print(f"Listing_count: {len(Listings)}")
    print(f'{Stations[5611]} is in {Systems[Stations[5611].system_id]}')
    end = datetime.now()
    print(f"Total runtime: {end-start}")
    input('...Press return to return to the main menu...')

functions = {"Search system":search_system, "Search station":search_station, "Search for best commoditie":search_for_lowest}

if __name__=='__main__':
    main()