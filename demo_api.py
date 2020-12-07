import requests
import json
import sqlite3
import os
import csv
from bs4 import BeautifulSoup

#API 1 - Gets Demographics from City, State (use string concatanation to create URL)
#response= requests.get("https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-cities-demographics&q=&facet=city&facet=state&refine.city=Memphis&refine.state=Tennessee")

def create_database(db_file):
    '''
    This function creates the database which will be used to store all the data
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_file)
    cur = conn.cursor()
    return cur, conn

def create_city_demos_table(cur, conn):
    '''
    This function uses an API to get the demographics of the top 100 most dangerous US cities + top 100 safest US cities we found with web scraping. 
    Source:https://public.opendatasoft.com/explore/dataset/us-cities-demographics/table/?sort=-count&dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6InVzLWNpdGllcy1kZW1vZ3JhcGhpY3MiLCJvcHRpb25zIjp7fX0sImNoYXJ0cyI6W3siYWxpZ25Nb250aCI6dHJ1ZSwidHlwZSI6ImNvbHVtbiIsImZ1bmMiOiJBVkciLCJ5QXhpcyI6ImNvdW50Iiwic2NpZW50aWZpY0Rpc3BsYXkiOnRydWUsImNvbG9yIjoiI0ZGNTE1QSJ9XSwieEF4aXMiOiJjaXR5IiwibWF4cG9pbnRzIjo1MCwic29ydCI6IiJ9XSwidGltZXNjYWxlIjoiIiwiZGlzcGxheUxlZ2VuZCI6dHJ1ZSwiYWxpZ25Nb250aCI6dHJ1ZX0%3D
    '''
    #create city_demos table to add this data, uses id keys from Dangerous_Cities
    cur.execute("CREATE TABLE IF NOT EXISTS City_Demos (city_id INTEGER, type TEXT, total_pop INTEGER, female_pop INTEGER, male_pop INTEGER, foreign_pop INTEGER, med_age FLOAT, white_pop INTEGER, black_pop INTEGER, asian_pop INTEGER, latin_pop INTEGER, na_pop INTEGER)")
   
    #limit to 25 lines at a time
    cur.execute('SELECT COUNT(*) FROM City_Demos')
    row_count = cur.fetchone()[0]
    cur.execute('SELECT max(city_id) FROM City_Demos')
    city_count = cur.fetchone()[0]
   
    if row_count == 0:
        #loop through dangerous cities table joined with state table to grab city and longform state to use in API request
        for i in range(25):
            #i = city_count + 1
            cur.execute('SELECT Dangerous_Cities.city, States.title FROM Dangerous_Cities JOIN States ON Dangerous_Cities.state = States.id WHERE Dangerous_Cities.id = ?', (i,))
            city_state_tuplist = cur.fetchall()
            city = city_state_tuplist[0][0]
            state = city_state_tuplist[0][1]
            #correction for the different spellings of 'saint'
            city_word_list = city.split(" ")
            if city_word_list[0] == "St.":
                city = "Saint " + city_word_list[1]
            try:
                #get demo data from API url
                url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-cities-demographics&q=&facet=city&facet=state&refine.city=" + city + "&refine.state=" + state
                r = requests.get(url)
            except:
                print("error when reading from url")
            #store this city's JSON data from the API into a dictionary
            demo_dict = json.loads(r.text)
            #now add this JSON data to our database in a new table, 1 row for each city
            # print(demo_dict)
            city_id = i
            if len(demo_dict["records"]) == 0:
                continue
            safety_type = "D"
            total_pop = demo_dict["records"][0]["fields"]["total_population"]
            female_pop = demo_dict["records"][0]["fields"]["female_population"]
            male_pop = demo_dict["records"][0]["fields"]["male_population"]
            foreign_pop = demo_dict["records"][0]["fields"]["foreign_born"]
            med_age = float(demo_dict["records"][0]["fields"]["median_age"])

            cur.execute('INSERT INTO City_Demos (city_id, type, total_pop, female_pop, male_pop, foreign_pop, med_age) VALUES (?,?,?,?,?,?,?)', (city_id, safety_type, total_pop, female_pop, male_pop, foreign_pop, med_age))
            conn.commit()
    elif row_count == 16:
        #loop through dangerous cities table joined with state table to grab city and longform state to use in API request
        for i in range(25, 50):
            #i = city_count + 1
            cur.execute('SELECT Dangerous_Cities.city, States.title FROM Dangerous_Cities JOIN States ON Dangerous_Cities.state = States.id WHERE Dangerous_Cities.id = ?', (i,))
            city_state_tuplist = cur.fetchall()
            city = city_state_tuplist[0][0]
            state = city_state_tuplist[0][1]
            #correction for the different spellings of 'saint'
            city_word_list = city.split(" ")
            if city_word_list[0] == "St.":
                city = "Saint " + city_word_list[1]

            try:
                #get demo data from API url
                url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-cities-demographics&q=&facet=city&facet=state&refine.city=" + city + "&refine.state=" + state
                r = requests.get(url)
            except:
                print("error when reading from url")
            #store this city's JSON data from the API into a dictionary
            demo_dict = json.loads(r.text)
            #now add this JSON data to our database in a new table, 1 row for each city
            # print(demo_dict)
            city_id = i
            if len(demo_dict["records"]) == 0:
                continue
            safety_type = "D"
            total_pop = demo_dict["records"][0]["fields"]["total_population"]
            female_pop = demo_dict["records"][0]["fields"]["female_population"]
            male_pop = demo_dict["records"][0]["fields"]["male_population"]
            foreign_pop = demo_dict["records"][0]["fields"]["foreign_born"]
            med_age = float(demo_dict["records"][0]["fields"]["median_age"])

            cur.execute('INSERT INTO City_Demos (city_id, type, total_pop, female_pop, male_pop, foreign_pop, med_age) VALUES (?,?,?,?,?,?,?)', (city_id, safety_type, total_pop, female_pop, male_pop, foreign_pop, med_age))
            conn.commit()
    elif row_count == 30:
        #loop through dangerous cities table joined with state table to grab city and longform state to use in API request
        for i in range(50, 75):
            #i = city_count + 1
            cur.execute('SELECT Dangerous_Cities.city, States.title FROM Dangerous_Cities JOIN States ON Dangerous_Cities.state = States.id WHERE Dangerous_Cities.id = ?', (i,))
            city_state_tuplist = cur.fetchall()
            city = city_state_tuplist[0][0]
            state = city_state_tuplist[0][1]
            #correction for the different spellings of 'saint'
            city_word_list = city.split(" ")
            if city_word_list[0] == "St.":
                city = "Saint " + city_word_list[1]

            try:
                #get demo data from API url
                url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-cities-demographics&q=&facet=city&facet=state&refine.city=" + city + "&refine.state=" + state
                r = requests.get(url)
            except:
                print("error when reading from url")
            #store this city's JSON data from the API into a dictionary
            demo_dict = json.loads(r.text)
            #now add this JSON data to our database in a new table, 1 row for each city
            # print(demo_dict)
            city_id = i
            if len(demo_dict["records"]) == 0:
                continue
            safety_type = "D"
            total_pop = demo_dict["records"][0]["fields"]["total_population"]
            female_pop = demo_dict["records"][0]["fields"]["female_population"]
            male_pop = demo_dict["records"][0]["fields"]["male_population"]
            foreign_pop = demo_dict["records"][0]["fields"]["foreign_born"]
            med_age = float(demo_dict["records"][0]["fields"]["median_age"])

            cur.execute('INSERT INTO City_Demos (city_id, type, total_pop, female_pop, male_pop, foreign_pop, med_age) VALUES (?,?,?,?,?,?,?)', (city_id, safety_type, total_pop, female_pop, male_pop, foreign_pop, med_age))
            conn.commit()
    elif row_count == 47:
        #loop through dangerous cities table joined with state table to grab city and longform state to use in API request
        for i in range(75, 100):
            #i = city_count + 1
            cur.execute('SELECT Dangerous_Cities.city, States.title FROM Dangerous_Cities JOIN States ON Dangerous_Cities.state = States.id WHERE Dangerous_Cities.id = ?', (i,))
            city_state_tuplist = cur.fetchall()
            city = city_state_tuplist[0][0]
            state = city_state_tuplist[0][1]
            #correction for the different spellings of 'saint'
            city_word_list = city.split(" ")
            if city_word_list[0] == "St.":
                city = "Saint " + city_word_list[1]

            try:
                #get demo data from API url
                url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-cities-demographics&q=&facet=city&facet=state&refine.city=" + city + "&refine.state=" + state
                r = requests.get(url)
            except:
                print("error when reading from url")
            #store this city's JSON data from the API into a dictionary
            demo_dict = json.loads(r.text)
            #now add this JSON data to our database in a new table, 1 row for each city
            city_id = i
            if len(demo_dict["records"]) == 0:
                continue
            safety_type = "D"
            total_pop = demo_dict["records"][0]["fields"]["total_population"]
            female_pop = demo_dict["records"][0]["fields"]["female_population"]
            male_pop = demo_dict["records"][0]["fields"]["male_population"]
            foreign_pop = demo_dict["records"][0]["fields"]["foreign_born"]
            med_age = float(demo_dict["records"][0]["fields"]["median_age"])

            cur.execute('INSERT INTO City_Demos (city_id, type, total_pop, female_pop, male_pop, foreign_pop, med_age) VALUES (?,?,?,?,?,?,?)', (city_id, safety_type, total_pop, female_pop, male_pop, foreign_pop, med_age))
            conn.commit()
    elif row_count == 63:
        #loop through dangerous cities table joined with state table to grab city and longform state to use in API request
        for i in range(25):
            #i = city_count + 1
            cur.execute('SELECT Safe_Cities.city, States.title FROM Safe_Cities JOIN States ON Safe_Cities.state = States.id WHERE Safe_Cities.id = ?', (i,))
            city_state_tuplist = cur.fetchall()
            city = city_state_tuplist[0][0]
            state = city_state_tuplist[0][1]
            #correction for the different spellings of 'saint'
            city_word_list = city.split(" ")
            if city_word_list[0] == "St.":
                city = "Saint " + city_word_list[1]

            try:
                #get demo data from API url
                url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-cities-demographics&q=&facet=city&facet=state&refine.city=" + city + "&refine.state=" + state
                r = requests.get(url)
            except:
                print("error when reading from url")
            #store this city's JSON data from the API into a dictionary
            demo_dict = json.loads(r.text)
            #now add this JSON data to our database in a new table, 1 row for each city
            city_id = i
            if len(demo_dict["records"]) == 0:
                continue
            safety_type = "S"
            total_pop = demo_dict["records"][0]["fields"]["total_population"]
            female_pop = demo_dict["records"][0]["fields"]["female_population"]
            male_pop = demo_dict["records"][0]["fields"]["male_population"]
            foreign_pop = demo_dict["records"][0]["fields"]["foreign_born"]
            med_age = float(demo_dict["records"][0]["fields"]["median_age"])

            cur.execute('INSERT INTO City_Demos (city_id, type, total_pop, female_pop, male_pop, foreign_pop, med_age) VALUES (?,?,?,?,?,?,?)', (city_id, safety_type, total_pop, female_pop, male_pop, foreign_pop, med_age))
            conn.commit()
    elif row_count == 74:
        #loop through dangerous cities table joined with state table to grab city and longform state to use in API request
        for i in range(25):
            #i = city_count + 1
            cur.execute('SELECT Safe_Cities.city, States.title FROM Safe_Cities JOIN States ON Safe_Cities.state = States.id WHERE Safe_Cities.id = ?', (i,))
            city_state_tuplist = cur.fetchall()
            city = city_state_tuplist[0][0]
            state = city_state_tuplist[0][1]
            #correction for the different spellings of 'saint'
            city_word_list = city.split(" ")
            if city_word_list[0] == "St.":
                city = "Saint " + city_word_list[1]

            try:
                #get demo data from API url
                url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-cities-demographics&q=&facet=city&facet=state&refine.city=" + city + "&refine.state=" + state
                r = requests.get(url)
            except:
                print("error when reading from url")
            #store this city's JSON data from the API into a dictionary
            demo_dict = json.loads(r.text)
            #now add this JSON data to our database in a new table, 1 row for each city
            city_id = i
            if len(demo_dict["records"]) == 0:
                continue
            safety_type = "S"
            total_pop = demo_dict["records"][0]["fields"]["total_population"]
            female_pop = demo_dict["records"][0]["fields"]["female_population"]
            male_pop = demo_dict["records"][0]["fields"]["male_population"]
            foreign_pop = demo_dict["records"][0]["fields"]["foreign_born"]
            med_age = float(demo_dict["records"][0]["fields"]["median_age"])

            cur.execute('INSERT INTO City_Demos (city_id, type, total_pop, female_pop, male_pop, foreign_pop, med_age) VALUES (?,?,?,?,?,?,?)', (city_id, safety_type, total_pop, female_pop, male_pop, foreign_pop, med_age))
            conn.commit()
    elif row_count == 85:
        #loop through dangerous cities table joined with state table to grab city and longform state to use in API request
        for i in range(25, 50):
            #i = city_count + 1
            cur.execute('SELECT Safe_Cities.city, States.title FROM Safe_Cities JOIN States ON Safe_Cities.state = States.id WHERE Safe_Cities.id = ?', (i,))
            city_state_tuplist = cur.fetchall()
            city = city_state_tuplist[0][0]
            state = city_state_tuplist[0][1]
            #correction for the different spellings of 'saint'
            city_word_list = city.split(" ")
            if city_word_list[0] == "St.":
                city = "Saint " + city_word_list[1]

            try:
                #get demo data from API url
                url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-cities-demographics&q=&facet=city&facet=state&refine.city=" + city + "&refine.state=" + state
                r = requests.get(url)
            except:
                print("error when reading from url")
            #store this city's JSON data from the API into a dictionary
            demo_dict = json.loads(r.text)
            #now add this JSON data to our database in a new table, 1 row for each city
            city_id = i
            if len(demo_dict["records"]) == 0:
                continue
            safety_type = "S"
            total_pop = demo_dict["records"][0]["fields"]["total_population"]
            female_pop = demo_dict["records"][0]["fields"]["female_population"]
            male_pop = demo_dict["records"][0]["fields"]["male_population"]
            foreign_pop = demo_dict["records"][0]["fields"]["foreign_born"]
            med_age = float(demo_dict["records"][0]["fields"]["median_age"])

            cur.execute('INSERT INTO City_Demos (city_id, type, total_pop, female_pop, male_pop, foreign_pop, med_age) VALUES (?,?,?,?,?,?,?)', (city_id, safety_type, total_pop, female_pop, male_pop, foreign_pop, med_age))
            conn.commit()
    elif row_count == 94:
        #loop through dangerous cities table joined with state table to grab city and longform state to use in API request
        for i in range(50, 75):
            #i = city_count + 1
            cur.execute('SELECT Safe_Cities.city, States.title FROM Safe_Cities JOIN States ON Safe_Cities.state = States.id WHERE Safe_Cities.id = ?', (i,))
            city_state_tuplist = cur.fetchall()
            city = city_state_tuplist[0][0]
            state = city_state_tuplist[0][1]
            #correction for the different spellings of 'saint'
            city_word_list = city.split(" ")
            if city_word_list[0] == "St.":
                city = "Saint " + city_word_list[1]

            try:
                #get demo data from API url
                url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-cities-demographics&q=&facet=city&facet=state&refine.city=" + city + "&refine.state=" + state
                r = requests.get(url)
            except:
                print("error when reading from url")
            #store this city's JSON data from the API into a dictionary
            demo_dict = json.loads(r.text)
            #now add this JSON data to our database in a new table, 1 row for each city
            city_id = i
            if len(demo_dict["records"]) == 0:
                continue
            safety_type = "S"
            total_pop = demo_dict["records"][0]["fields"]["total_population"]
            female_pop = demo_dict["records"][0]["fields"]["female_population"]
            male_pop = demo_dict["records"][0]["fields"]["male_population"]
            foreign_pop = demo_dict["records"][0]["fields"]["foreign_born"]
            med_age = float(demo_dict["records"][0]["fields"]["median_age"])

            cur.execute('INSERT INTO City_Demos (city_id, type, total_pop, female_pop, male_pop, foreign_pop, med_age) VALUES (?,?,?,?,?,?,?)', (city_id, safety_type, total_pop, female_pop, male_pop, foreign_pop, med_age))
            conn.commit()
    elif row_count == 106:
        #loop through dangerous cities table joined with state table to grab city and longform state to use in API request
        for i in range(75,100):
            #i = city_count + 1
            cur.execute('SELECT Safe_Cities.city, States.title FROM Safe_Cities JOIN States ON Safe_Cities.state = States.id WHERE Safe_Cities.id = ?', (i,))
            city_state_tuplist = cur.fetchall()
            city = city_state_tuplist[0][0]
            state = city_state_tuplist[0][1]
            #correction for the different spellings of 'saint'
            city_word_list = city.split(" ")
            if city_word_list[0] == "St.":
                city = "Saint " + city_word_list[1]

            try:
                #get demo data from API url
                url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-cities-demographics&q=&facet=city&facet=state&refine.city=" + city + "&refine.state=" + state
                r = requests.get(url)
            except:
                print("error when reading from url")
            #store this city's JSON data from the API into a dictionary
            demo_dict = json.loads(r.text)
            #now add this JSON data to our database in a new table, 1 row for each city
            # print(demo_dict)
            city_id = i
            if len(demo_dict["records"]) == 0:
                continue
            safety_type = "S"
            total_pop = demo_dict["records"][0]["fields"]["total_population"]
            female_pop = demo_dict["records"][0]["fields"]["female_population"]
            male_pop = demo_dict["records"][0]["fields"]["male_population"]
            foreign_pop = demo_dict["records"][0]["fields"]["foreign_born"]
            med_age = float(demo_dict["records"][0]["fields"]["median_age"])

            cur.execute('INSERT INTO City_Demos (city_id, type, total_pop, female_pop, male_pop, foreign_pop, med_age) VALUES (?,?,?,?,?,?,?)', (city_id, safety_type, total_pop, female_pop, male_pop, foreign_pop, med_age))
            conn.commit()
    

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = create_database('crime.db')
    create_city_demos_table(cur, conn)

main()