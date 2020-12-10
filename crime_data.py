import requests
import json
import sqlite3
import os
import csv
from bs4 import BeautifulSoup

def create_database(db_file):
    '''
    This function creates the database which will be used to store all data.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_file)
    cur = conn.cursor()
    return cur, conn

def create_state_table(cur, conn):
    '''
    This function creates the States lookup table and adds it to the database.
    It assigns the state to a unique primary key id, inserts the abbreviation for 
    each state, and inserts the full name of the state."
    '''
    
    states = ["Alabama","Alaska", "Arizona","Arkansas","California","Colorado","Connecticut","Delaware","District of Colombia","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
    state_abr = ["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
    
    cur.execute("CREATE TABLE IF NOT EXISTS States (id INTEGER PRIMARY KEY, abbreviation TEXT , state_name TEXT)")

    cur.execute('SELECT COUNT(*) FROM States')
    row_count = cur.fetchone()[0]
    if row_count == 0:
        for i in range(len(states)):
            cur.execute("INSERT INTO States (id,abbreviation,state_name) VALUES (?,?,?)",(i,state_abr[i],states[i]))
        conn.commit() 

def create_dangerous_cities_table(cur, conn):
    '''
    This function uses a website to webscrape the names of the top 100 most dangerous US cities.
    After seperating the city name from the state, it assigns the city to an id, and inserts the
    state_id as a foreign key. 
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

    cur.execute("CREATE TABLE IF NOT EXISTS Dangerous_Cities (id INTEGER PRIMARY KEY, city TEXT, state_id INTEGER)")
    #uncomment this if you want to collect all 100 rows at once
    '''
    for i in range(len(stateList)):
        cur.execute("INSERT INTO Dangerous_Cities (id,city,state_id) VALUES (?,?,?)",(i,cityList[i],stateList[i]))
    conn.commit() 
    '''
    # want the loop to run 25 times
    cur.execute('SELECT COUNT(*) FROM Dangerous_Cities')
    row_count = cur.fetchone()[0]
    if row_count == 0:
        for i in range(25):
            #insert state_id as foreign key
            state = stateList[i]
            cur.execute("SELECT id FROM States WHERE abbreviation = ?", (state,))
            state_id = cur.fetchone()[0]
            cur.execute("INSERT INTO Dangerous_Cities (id,city,state_id) VALUES (?,?,?)",(i,cityList[i],state_id))
        conn.commit() 
    elif row_count == 25:
        for i in range(25, 50):
            #insert state_id as foreign key
            state = stateList[i]
            cur.execute("SELECT id FROM States WHERE abbreviation = ?", (state,))
            state_id = cur.fetchone()[0]
            cur.execute("INSERT INTO Dangerous_Cities (id,city,state_id) VALUES (?,?,?)",(i,cityList[i],state_id))
        conn.commit()  
    elif row_count == 50:
        for i in range(50, 75):
            #insert state_id as foreign key
            state = stateList[i]
            cur.execute("SELECT id FROM States WHERE abbreviation = ?", (state,))
            state_id = cur.fetchone()[0]
            cur.execute("INSERT INTO Dangerous_Cities (id,city,state_id) VALUES (?,?,?)",(i,cityList[i],state_id))
        conn.commit()  
    elif row_count == 75:
        for i in range(75, 100):
            #insert state_id as foreign key
            state = stateList[i]
            cur.execute("SELECT id FROM States WHERE abbreviation = ?", (state,))
            state_id = cur.fetchone()[0]
            cur.execute("INSERT INTO Dangerous_Cities (id,city,state_id) VALUES (?,?,?)",(i,cityList[i],state_id))
        conn.commit()  

def create_safe_cities_table(cur, conn):
    '''
    This function uses a website to webscrape the names of the top 100 most safe 
    US cities by selecting 25 at a time, and adding them to the database.
    After separating the city name from the state, it assigns the city name 
    an id and inserts the state_id as a foreign key.
    Source: https://www.safehome.org/safest-cities/
    '''
    city = str()
    city_list = []
    city_list_URL = "https://www.safehome.org/safest-cities/"
    page = requests.get(city_list_URL) 
    soup = BeautifulSoup(page.content, 'html.parser')
    tags = soup.find_all("h3")
    for location in tags:
        city_state = location.text
        city_list.append(city_state)
        if len(city_list) >= 100:
            break

    cityList = []
    stateList = []
    #separate city from state
    for location in city_list:
        separated_location = location.split(", ")
        city = separated_location[0]
        cityList.append(city)
        state = separated_location[1]
        stateList.append(state)

    cur.execute("CREATE TABLE IF NOT EXISTS Safe_Cities (id INTEGER PRIMARY KEY, city TEXT, state_id INTEGER)")
    #uncomment this if you want to collect all 100 rows at once
    '''
    for i in range(len(stateList)):
        cur.execute("INSERT INTO Dangerous_Cities (id,city,state_id) VALUES (?,?,?)",(i,cityList[i],stateList[i]))
    conn.commit() 
    '''
    # want the loop to run 25 times
    cur.execute('SELECT COUNT(*) FROM Safe_Cities')
    row_count = cur.fetchone()[0]
    if row_count == 0:
        print("Collecting Web Data...(1/4)")
        for i in range(25):
            state = stateList[i]
            cur.execute("SELECT id FROM States WHERE abbreviation = ?", (state,))
            state_id = cur.fetchone()[0]
            cur.execute("INSERT INTO Safe_Cities (id,city,state_id) VALUES (?,?,?)",(i,cityList[i],state_id))        
        conn.commit()
    elif row_count == 25:
        print("Collecting Web Data...(2/4)")
        for i in range(25, 50):
            state = stateList[i]
            cur.execute("SELECT id FROM States WHERE abbreviation = ?", (state,))
            state_id = cur.fetchone()[0]
            cur.execute("INSERT INTO Safe_Cities (id,city,state_id) VALUES (?,?,?)",(i,cityList[i],state_id))        
        conn.commit()
    elif row_count == 50:
        print("Collecting Web Data...(3/4)")
        for i in range(50, 75):
            state = stateList[i]
            cur.execute("SELECT id FROM States WHERE abbreviation = ?", (state,))
            state_id = cur.fetchone()[0]
            cur.execute("INSERT INTO Safe_Cities (id,city,state_id) VALUES (?,?,?)",(i,cityList[i],state_id))        
        conn.commit()  
    elif row_count == 75:
        print("Collecting Web Data...(4/4)")
        for i in range(75, 100):
            state = stateList[i]
            cur.execute("SELECT id FROM States WHERE abbreviation = ?", (state,))
            state_id = cur.fetchone()[0]
            cur.execute("INSERT INTO Safe_Cities (id,city,state_id) VALUES (?,?,?)",(i,cityList[i],state_id))        
        conn.commit()  
    
    print("Finished")

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = create_database('crime.db')
    create_state_table(cur, conn)

    create_dangerous_cities_table(cur, conn)
    
    create_safe_cities_table(cur, conn)
    
if __name__ == "__main__":
    main()