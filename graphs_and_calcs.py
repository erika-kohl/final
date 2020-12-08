import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import os

def access_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn

#using crime_data.py and table Safe_Cities

#using crime_data.py and table Dangerous_Cities

#using crime_counts.py and table State_Crimes
#total number of arrests in 2017 for all states
def arrests_in_2017(cur, conn):
    total = 0
    list_of_total_from_all_states = []

    cur.execute('SELECT total_arrests FROM State_Crimes WHERE year = 2017')
    tup_of_total_from_all_states = cur.fetchall()

    for tup in tup_of_total_from_all_states:
        list_of_total_from_all_states.append(tup[0])

    for total_from_each_state in list_of_total_from_all_states:
        total += total_from_each_state

    return total

#total number of arrests in 2018 for all states
def arrests_in_2018(cur, conn):
    total = 0
    list_of_total_from_all_states = []

    cur.execute('SELECT total_arrests FROM State_Crimes WHERE year = 2018')
    tup_of_total_from_all_states = cur.fetchall()

    for tup in tup_of_total_from_all_states:
        list_of_total_from_all_states.append(tup[0])

    for total_from_each_state in list_of_total_from_all_states:
        total += total_from_each_state

    return total

#for each state, what are they most arrested for? combine data for 2017 and 2018 for each state
def most_arrests_for(cur, conn):
    #return string
    pass

#using demo_api.py and table City_Demos
#perhaps which demographic most populates each state?

def main():
    cur, conn = access_database('crime.db')
    print("The total number of arrests in 2017 in the United States is " + str(arrests_in_2017(cur, conn)) + ".")
    print("The total number of arrests in 2018 in the United States is " + str(arrests_in_2018(cur, conn)) + ".")

main()