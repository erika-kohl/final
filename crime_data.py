import requests
import json
import sqlite3
import os
import csv
from bs4 import BeautifulSoup

#API_key = "43vyNBaRamuvatb61ifsdblzCXp6qmkYz2ZJs9Hs"
#API 3 - Gets Crime counts by category based on State
response = requests.get("https://api.usa.gov/crime/fbi/sapi/api/arrest/states/offense/IL/all/2017/2019?API_KEY=43vyNBaRamuvatb61ifsdblzCXp6qmkYz2ZJs9Hs")

#Extra API -  Gets State population by year
#response = requests.get("https://datausa.io/api/data?drilldowns=State&measures=Population&year=2016")

#API 1 - Gets Demographics from City, State (use string concatanation to create URL)
#response= requests.get("https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-cities-demographics&q=&facet=city&facet=state&refine.city=Memphis&refine.state=Tennessee")

#print(response.status_code)
#print(response.json())

def get_city_list(cur, conn):
    '''
    This function uses a website to webscrape the names of the top 100 most dangerous US cities. 
    Source: https://www.neighborhoodscout.com/blog/top100dangerous
    '''
    city = str()
    city_list = []
    city_list_URL = "https://www.neighborhoodscout.com/blog/top100dangerous"
    page = requests.get(city_list_URL) 
    soup = BeautifulSoup(page.content, 'html.parser')
    tags = soup.find_all("h3")
    for location in tags:
        title = location.find("a")
        city_state = title.text
        city_list.append(city_state)

    cityList = []
    stateList = []
    #separate city from state
    for location in city_list:
        separated_location = location.split(", ")
        city = separated_location[0]
        cityList.append(city)
        state = separated_location[1]
        stateList.append(state)
    
    print(cityList)
    print(stateList)

    cur.execute("CREATE TABLE IF NOT EXISTS Dangerous_Cities (id INTEGER PRIMARY KEY, city TEXT, state TEXT)")
    for i in range((stateList)):
        cur.execute("INSERT INTO States (id,city,state) VALUES (?,?,?)",(i,cityList[i],stateList[i]))
    conn.commit() 


def create_database(db_file):
    '''
    This function creates the database which will be used to the data
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_file)
    cur = conn.cursor()
    return cur, conn

def create_state_table(cur, conn):
    '''
    This function creates the States lookup table and adds it to the database.It sets the abbreviation for each state as the primary key since each is unique."
    '''
    
    states = ["Alabama","Alaska", "Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","IllinoisIndiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","MontanaNebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","PennsylvaniaRhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
    state_abr = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
    
    cur.execute("CREATE TABLE IF NOT EXISTS States (id TEXT PRIMARY KEY, title TEXT)")
    for i in range(len(states)):
        cur.execute("INSERT INTO States (id,title) VALUES (?,?)",(state_abr[i],states[i]))
    conn.commit() 


def json_print():
    # create a formatted string of the Python JSON object
    obj = response.json()
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def main():
    # SETUP DATABASE AND TABLE
    cur, conn = create_database('crime.db')
    create_state_table(cur, conn)
    get_city_list(cur, conn)
    json_print()

    
if __name__ == "__main__":
    main()
