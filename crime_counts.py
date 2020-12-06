import requests
import json
import sqlite3
import os
import csv
from bs4 import BeautifulSoup

#API_key = "43vyNBaRamuvatb61ifsdblzCXp6qmkYz2ZJs9Hs"
#API 3 - Gets Crime counts by category based on State
#replace IL with for looop through all state abbreviations
response = requests.get("https://api.usa.gov/crime/fbi/sapi/api/arrest/states/offense/IL/all/2017/2018?API_KEY=43vyNBaRamuvatb61ifsdblzCXp6qmkYz2ZJs9Hs")

def json_print():
    # create a formatted string of the Python JSON object
    obj = response.json()
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def main():
    # SETUP DATABASE AND TABLE
    #cur, conn = create_database('crime.db')
    json_print()

main()