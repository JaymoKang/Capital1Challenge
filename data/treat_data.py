import csv
import json
from math import log

WORLD_FACTOR = 1.78e-07
NO20_FACTOR = 1.78e-06
G20 = ["Argentina", "Australia", "Brazil", "Canada", "China", "France", "Germany", "India", "Indonesia" , "Italy", "Japan", "Mexico", "Russia", "Saudi Arabia", "South Africa", "South Korea", "Turkey", "United Kingdom", "United States", "European Union"]

class Coordinate:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

csv_reader = csv.reader(open("GDP.csv", "rb"), delimiter=",")
GDPs = {}
for row in csv_reader:
    country = row[2]
    gdp = int(row[3].replace("\"", "").replace(",", ""))
    GDPs[country] = gdp

csv_reader = csv.reader(open("locations.tsv", "rb"), delimiter="\t")
locations = {}
for row in csv_reader:
    latitude = float(row[1])
    longitude = float(row[2])
    country = row[3]
    coor = Coordinate(latitude, longitude)
    locations[country] = coor

world = []
no20 = []
g20 = []

def addToList(array, country, loc, factor):
    array.append(int(loc.latitude))
    array.append(int(loc.longitude))
    array.append(factor * GDPs[country])

for country in GDPs:
    try:
        loc = locations[country]
        addToList(world, country, loc, WORLD_FACTOR)
        if country in G20:
            addToList(no20, country, loc, 0)
        else:
            addToList(no20, country, loc, NO20_FACTOR)
    except KeyError:
        pass

toReturn = [["World", world],["No20", no20]]

json.dump(toReturn, open ("mapping_data.json", "w+"))
