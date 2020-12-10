import requests
import json
import sqlite3
import os
import csv

API_key = "43vyNBaRamuvatb61ifsdblzCXp6qmkYz2ZJs9Hs"

def create_database(db_file):
    '''
    This function creates the database named crime_data.db,  
    which will be used to store all the data collected within our project. 
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_file)
    cur = conn.cursor()
    return cur, conn

def create_state_crime_counts_table(cur,conn,start,end,start_year):
    '''
    This function uses an API to get crime counts sorted by crime type, state, and year.
    We're looking at years 2017 and 2018 for data. After running 4 times, all 100 rows of 
    data will be entered into the database under the States_Crime table. This datbase excludes 
    DC since its results were significantly lower in comparison. 
    Source:https://crime-data-explorer.fr.cloud.gov/api
    '''
    end_year = start_year + 1
    for i in range(start,end):
        #get state code from state table
        cur.execute('SELECT abbreviation FROM States WHERE id = ?', (i,))
        state_abr = cur.fetchone()[0]
        cur.execute('SELECT id FROM States WHERE abbreviation = ?', (state_abr,))
        state_id = cur.fetchone()[0]
        if state_id == 8:
            continue
        else:
            try:
                #get state crime data from API url
                url = "https://api.usa.gov/crime/fbi/sapi/api/arrest/states/offense/" + state_abr + "/all/" + str(start_year) + "/" + str(end_year) +"?API_KEY=" + API_key
                r = requests.get(url)
            except:
                print("error when reading from url")
        #store this city's JSON data from the API into a dictionary
        crime_dict = json.loads(r.text)
        #print(crime_dict)

        year = crime_dict["data"][0]["data_year"]
        ag_assault = crime_dict["data"][0]["value"]
        other = crime_dict["data"][2]["value"]
        arson = crime_dict["data"][4]["value"]
        burglary = crime_dict["data"][6]["value"]
        loitering = crime_dict["data"][8]["value"]
        disorderly = crime_dict["data"][10]["value"]
        dui = crime_dict["data"][12]["value"]
        drug_abuse = crime_dict["data"][14]["value"]
        drunkenness = crime_dict["data"][16]["value"]
        embezzlement = crime_dict["data"][18]["value"]
        forgery = crime_dict["data"][20]["value"]
        fraud = crime_dict["data"][22]["value"]
        gambling = crime_dict["data"][24]["value"]
        trafficking = (crime_dict["data"][26]["value"] + crime_dict["data"][28]["value"])
        larceny = crime_dict["data"][30]["value"]
        liquor = crime_dict["data"][32]["value"]
        manslaughter = crime_dict["data"][34]["value"]
        mvt = crime_dict["data"][36]["value"]
        murder = crime_dict["data"][38]["value"]
        family_o = crime_dict["data"][40]["value"]
        prostitution = crime_dict["data"][42]["value"]
        rape = crime_dict["data"][44]["value"]
        robbery = crime_dict["data"][46]["value"]
        sex_o = crime_dict["data"][48]["value"]
        s_assault = crime_dict["data"][50]["value"]
        stolen_p = crime_dict["data"][52]["value"]
        suspicion = crime_dict["data"][54]["value"]
        vagrancy = crime_dict["data"][56]["value"]
        vandalism = crime_dict["data"][58]["value"]
        weapons = crime_dict["data"][60]["value"]
        total_arrests = ag_assault + other + arson + burglary + loitering + disorderly + dui + drug_abuse + drunkenness + embezzlement + forgery + fraud + gambling + trafficking + larceny + liquor + manslaughter + mvt + murder + family_o + prostitution + rape + robbery + sex_o + s_assault + stolen_p + suspicion + vagrancy + vandalism + weapons
        #longest line of code ever written
        cur.execute("INSERT INTO State_Crimes (state_id,year,total_arrests,ag_assault,arson,burglary,disorderly,drug_abuse,drunkenness, dui, embezzlement, family_o, forgery, fraud, gambling, larceny, liquor, loitering, manslaughter, murder, mvt, other, prostitution, rape, robbery, sex_o, s_assault, stolen_p, suspicion, trafficking, vagrancy, vandalism, weapons) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (state_id, year, total_arrests, ag_assault, arson, burglary, disorderly, drug_abuse, drunkenness, dui, embezzlement, family_o, forgery, fraud, gambling, larceny, liquor, loitering, manslaughter, murder, mvt, other, prostitution, rape, robbery, sex_o, s_assault, stolen_p, suspicion, trafficking, vagrancy, vandalism, weapons))

    conn.commit()

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = create_database('crime.db')
    #create state crimes table to add this data, uses id keys from Dangerous_Cities
    cur.execute("CREATE TABLE IF NOT EXISTS State_Crimes (state_id TEXT, year INTEGER, total_arrests INTEGER, ag_assault INTEGER, arson INTEGER, burglary INTEGER, disorderly INTEGER, drug_abuse INTEGER, drunkenness INTEGER, dui INTEGER, embezzlement INTEGER, family_o INTEGER, forgery INTEGER, fraud INTEGER, gambling INTEGER, larceny INTEGER, liquor INTEGER, loitering INTEGER, manslaughter INTEGER, murder INTEGER, mvt INTEGER, other INTEGER, prostitution INTEGER, rape INTEGER, robbery INTEGER, sex_o INTEGER, s_assault INTEGER, stolen_p INTEGER, suspicion INTEGER, trafficking INTEGER, vagrancy INTEGER, vandalism INTEGER, weapons INTEGER)") 
     #limiting amount of data collected to 25 rows each time file is ran
    cur.execute('SELECT COUNT(*) FROM State_Crimes')
    row_count = cur.fetchone()[0]
    if row_count == 0:
        print("Collecting Crime Count Data... (1/4)")
        create_state_crime_counts_table(cur,conn,0,26,2017)
        print("Finshed")
    elif row_count == 25:
        print("Collecting Crime Count Data... (2/4)")
        create_state_crime_counts_table(cur,conn,26,51,2017)
        print("Finshed")
    elif row_count == 50:
        print("Collecting Crime Count Data... (3/4)")
        create_state_crime_counts_table(cur,conn,0,26,2018)
        print("Finshed")
    elif row_count == 75:
        print("Collecting Crime Count Data... (4/4)")
        create_state_crime_counts_table(cur,conn,26,51,2018)
        print("Finshed")
    elif row_count == 100:
        print("All 100 rows of Crime Count Data have been inserted into the database.")

if __name__ == "__main__":
    main()