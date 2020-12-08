import requests
import json
import sqlite3
import os
import csv

API_key = "43vyNBaRamuvatb61ifsdblzCXp6qmkYz2ZJs9Hs"

def create_database(db_file):
    '''
    This function creates the database which will be used to store all the data
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_file)
    cur = conn.cursor()
    return cur, conn

def create_state_crime_counts_table(cur,conn):
    '''
    This function uses an API to get crime counts sorted by type, state, and year. We're looking at years 2017 and 2018 for data 
    Source:https://crime-data-explorer.fr.cloud.gov/api
    '''
    #create state crimes table to add this data, uses id keys from Dangerous_Cities
    cur.execute("CREATE TABLE IF NOT EXISTS State_Crimes (state_id TEXT, year INTEGER, total_arrests INTEGER, ag_assault INTEGER, arson INTEGER, burglary INTEGER, disorderly INTEGER, drug_abuse INTEGER, drunkenness INTEGER, dui INTEGER, embezzlement INTEGER, family_o INTEGER, forgery INTEGER, fraud INTEGER, gambling INTEGER, larceny INTEGER, liquor INTEGER, loitering INTEGER, manslaughter INTEGER, murder INTEGER, mvt INTEGER, other INTEGER, prostitution INTEGER, rape INTEGER, robbery INTEGER, sex_o INTEGER, s_assault INTEGER, stolen_p INTEGER, suspicion INTEGER, trafficking INTEGER, vagrancy INTEGER, vandalism INTEGER, weapons INTEGER)")
    
    #limit to 25 lines at a time
    cur.execute('SELECT COUNT(*) FROM State_Crimes')
    row_count = cur.fetchone()[0]
    if row_count == 0:
        for i in range(25):
            #get state code from state table
            cur.execute('SELECT abbreviation FROM States WHERE id = ?', (i,))
            state_id = cur.fetchone()[0]
            try:
                #get state crime data from API url
                url = "https://api.usa.gov/crime/fbi/sapi/api/arrest/states/offense/" + state_id + "/all/2017/2018?API_KEY=" + API_key
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
    elif row_count == 25:
         for i in range(25, 50):
            #get state code from state table
            cur.execute('SELECT abbreviation FROM States WHERE id = ?', (i,))
            state_id = cur.fetchone()[0]
            try:
                #get state crime data from API url
                url = "https://api.usa.gov/crime/fbi/sapi/api/arrest/states/offense/" + state_id + "/all/2017/2018?API_KEY=" + API_key
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
    elif row_count == 50:
         for i in range(25):
            #get state code from state table
            cur.execute('SELECT abbreviation FROM States WHERE id = ?', (i,))
            state_id = cur.fetchone()[0]
            try:
                #get state crime data from API url
                url = "https://api.usa.gov/crime/fbi/sapi/api/arrest/states/offense/" + state_id + "/all/2017/2018?API_KEY=" + API_key
                r = requests.get(url)
            except:
                print("error when reading from url")
            #store this city's JSON data from the API into a dictionary
            crime_dict = json.loads(r.text)
            #print(crime_dict)

            year = crime_dict["data"][1]["data_year"]
            ag_assault = crime_dict["data"][1]["value"]
            other = crime_dict["data"][3]["value"]
            arson = crime_dict["data"][5]["value"]
            burglary = crime_dict["data"][7]["value"]
            loitering = crime_dict["data"][9]["value"]
            disorderly = crime_dict["data"][11]["value"]
            dui = crime_dict["data"][13]["value"]
            drug_abuse = crime_dict["data"][15]["value"]
            drunkenness = crime_dict["data"][17]["value"]
            embezzlement = crime_dict["data"][19]["value"]
            forgery = crime_dict["data"][21]["value"]
            fraud = crime_dict["data"][23]["value"]
            gambling = crime_dict["data"][25]["value"]
            trafficking = (crime_dict["data"][27]["value"] + crime_dict["data"][29]["value"])
            larceny = crime_dict["data"][31]["value"]
            liquor = crime_dict["data"][33]["value"]
            manslaughter = crime_dict["data"][35]["value"]
            mvt = crime_dict["data"][37]["value"]
            murder = crime_dict["data"][39]["value"]
            family_o = crime_dict["data"][41]["value"]
            prostitution = crime_dict["data"][43]["value"]
            rape = crime_dict["data"][45]["value"]
            robbery = crime_dict["data"][47]["value"]
            sex_o = crime_dict["data"][49]["value"]
            s_assault = crime_dict["data"][51]["value"]
            stolen_p = crime_dict["data"][53]["value"]
            suspicion = crime_dict["data"][55]["value"]
            vagrancy = crime_dict["data"][57]["value"]
            vandalism = crime_dict["data"][59]["value"]
            weapons = crime_dict["data"][61]["value"]
            total_arrests = ag_assault + other + arson + burglary + loitering + disorderly + dui + drug_abuse + drunkenness + embezzlement + forgery + fraud + gambling + trafficking + larceny + liquor + manslaughter + mvt + murder + family_o + prostitution + rape + robbery + sex_o + s_assault + stolen_p + suspicion + vagrancy + vandalism + weapons
            #longest line of code ever written
            cur.execute("INSERT INTO State_Crimes (state_id,year,total_arrests,ag_assault,arson,burglary,disorderly,drug_abuse,drunkenness, dui, embezzlement, family_o, forgery, fraud, gambling, larceny, liquor, loitering, manslaughter, murder, mvt, other, prostitution, rape, robbery, sex_o, s_assault, stolen_p, suspicion, trafficking, vagrancy, vandalism, weapons) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (state_id, year, total_arrests, ag_assault, arson, burglary, disorderly, drug_abuse, drunkenness, dui, embezzlement, family_o, forgery, fraud, gambling, larceny, liquor, loitering, manslaughter, murder, mvt, other, prostitution, rape, robbery, sex_o, s_assault, stolen_p, suspicion, trafficking, vagrancy, vandalism, weapons))
    elif row_count == 75:
         for i in range(25,50):
            #get state code from state table
            cur.execute('SELECT abbreviation FROM States WHERE id = ?', (i,))
            state_id = cur.fetchone()[0]
            try:
                #get state crime data from API url
                url = "https://api.usa.gov/crime/fbi/sapi/api/arrest/states/offense/" + state_id + "/all/2017/2018?API_KEY=" + API_key
                r = requests.get(url)
            except:
                print("error when reading from url")
            #store this city's JSON data from the API into a dictionary
            crime_dict = json.loads(r.text)
            #print(crime_dict)

            year = crime_dict["data"][1]["data_year"]
            ag_assault = crime_dict["data"][1]["value"]
            other = crime_dict["data"][3]["value"]
            arson = crime_dict["data"][5]["value"]
            burglary = crime_dict["data"][7]["value"]
            loitering = crime_dict["data"][9]["value"]
            disorderly = crime_dict["data"][11]["value"]
            dui = crime_dict["data"][13]["value"]
            drug_abuse = crime_dict["data"][15]["value"]
            drunkenness = crime_dict["data"][17]["value"]
            embezzlement = crime_dict["data"][19]["value"]
            forgery = crime_dict["data"][21]["value"]
            fraud = crime_dict["data"][23]["value"]
            gambling = crime_dict["data"][25]["value"]
            trafficking = (crime_dict["data"][27]["value"] + crime_dict["data"][29]["value"])
            larceny = crime_dict["data"][31]["value"]
            liquor = crime_dict["data"][33]["value"]
            manslaughter = crime_dict["data"][35]["value"]
            mvt = crime_dict["data"][37]["value"]
            murder = crime_dict["data"][39]["value"]
            family_o = crime_dict["data"][41]["value"]
            prostitution = crime_dict["data"][43]["value"]
            rape = crime_dict["data"][45]["value"]
            robbery = crime_dict["data"][47]["value"]
            sex_o = crime_dict["data"][49]["value"]
            s_assault = crime_dict["data"][51]["value"]
            stolen_p = crime_dict["data"][53]["value"]
            suspicion = crime_dict["data"][55]["value"]
            vagrancy = crime_dict["data"][57]["value"]
            vandalism = crime_dict["data"][59]["value"]
            weapons = crime_dict["data"][61]["value"]
            total_arrests = ag_assault + other + arson + burglary + loitering + disorderly + dui + drug_abuse + drunkenness + embezzlement + forgery + fraud + gambling + trafficking + larceny + liquor + manslaughter + mvt + murder + family_o + prostitution + rape + robbery + sex_o + s_assault + stolen_p + suspicion + vagrancy + vandalism + weapons
            #longest line of code ever written
            cur.execute("INSERT INTO State_Crimes (state_id,year,total_arrests,ag_assault,arson,burglary,disorderly,drug_abuse,drunkenness, dui, embezzlement, family_o, forgery, fraud, gambling, larceny, liquor, loitering, manslaughter, murder, mvt, other, prostitution, rape, robbery, sex_o, s_assault, stolen_p, suspicion, trafficking, vagrancy, vandalism, weapons) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (state_id, year, total_arrests, ag_assault, arson, burglary, disorderly, drug_abuse, drunkenness, dui, embezzlement, family_o, forgery, fraud, gambling, larceny, liquor, loitering, manslaughter, murder, mvt, other, prostitution, rape, robbery, sex_o, s_assault, stolen_p, suspicion, trafficking, vagrancy, vandalism, weapons))


    conn.commit()

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = create_database('crime.db')
    create_state_crime_counts_table(cur,conn)

main()