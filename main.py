import pandas as pd
import json, sys
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
    write('Started Css')
    global Listings
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


if __name__=='__main__':
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
    finished = True