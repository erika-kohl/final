import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import os

def access_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn

def write_file(filename, information):
    """
    This function uses the crime data information and
    writes the information in a text file called crime_information.txt.
    """
    
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filename), "a") as out_file:
        if information not in filename:
            out_file.write(information)

#using crime_data.py and table Dangerous_Cities
def state_with_most_dangerous_cities(cur, conn):
    cur.execute('SELECT state_id FROM Dangerous_Cities')
    dangerous_states = cur.fetchall()
    dangerous_states_ids = []
    
    for value in dangerous_states:
        state_id = str(value)
        state_code = state_id.strip("(,)")
        dangerous_states_ids.append(state_code)

    dangerous_state_counts = {}
    state_list = []

    for code in dangerous_states_ids:
        cur.execute('SELECT state_name FROM States JOIN Dangerous_Cities on States.id = Dangerous_Cities.state_id WHERE Dangerous_Cities.state_id = ?', (code,))
        state_name = cur.fetchone()[0]
        state_list.append(state_name)
    
    for state in state_list:
        dangerous_state_counts[state] = dangerous_state_counts.get(state, 0) + 1
    
    ranked_dangerous_states = sorted(dangerous_state_counts.items(), key=lambda x: x[1], reverse=True) 
    print("_______ States with their Counts of Top 100 Dangerous Cities _______") 
    
    for state_ranking in ranked_dangerous_states:
        print(state_ranking)
    
    #print(ranked_dangerous_states)

#using crime_data.py and table Safe_Cities
def state_with_most_safe_cities(cur, conn):
    cur.execute('SELECT state_id FROM Safe_Cities')
    safe_states = cur.fetchall()
    safe_states_ids = []
    
    for value in safe_states:
        state_id = str(value)
        state_code = state_id.strip("(,)")
        safe_states_ids.append(state_code)

    safe_state_counts = {}
    state_list = []

    for code in safe_states_ids:
        cur.execute('SELECT state_name FROM States JOIN Safe_Cities on States.id = Safe_Cities.state_id WHERE Safe_Cities.state_id = ?', (code,))
        state_name = cur.fetchone()[0]
        state_list.append(state_name)
    
    for state in state_list:
        safe_state_counts[state] = safe_state_counts.get(state, 0) + 1
    
    ranked_safe_states = sorted(safe_state_counts.items(), key=lambda x: x[1], reverse=True) 
    print("_______ States with their Counts of Top 100 Safest Cities _______") 
    
    for state_ranking in ranked_safe_states:
        print(state_ranking)

#using crime_counts.py and table State_Crimes
#total number of arrests in 2017 or 2018 for all states
def arrests_in_year(cur, conn, year):
    total = 0
    list_of_total_from_all_states = []

    cur.execute('SELECT total_arrests FROM State_Crimes WHERE year = ?', (year,))
    tup_of_total_from_all_states = cur.fetchall()

    for tup in tup_of_total_from_all_states:
        list_of_total_from_all_states.append(tup[0])

    for total_from_each_state in list_of_total_from_all_states:
        total += total_from_each_state

    return total

#for each state and year, what are they most arrested for (besides other category)? 
def most_arrests_for(cur, conn, state_abbrev, year):
    cur.execute('SELECT ag_assault, arson, burglary, disorderly, drug_abuse, drunkenness, dui, embezzlement, family_o, forgery, fraud, gambling, larceny, liquor, loitering, manslaughter, murder, mvt, prostitution, rape, robbery, sex_o, s_assault, stolen_p, suspicion, trafficking, vagrancy, vandalism, weapons FROM State_Crimes WHERE state_id = ? and year = ?', (state_abbrev, year))
    tup_of_all_arrests_for_each_category = cur.fetchone()
    
    #does this count as hardcoding?
    categories_list = ["ag_assault","arson","burglary","disorderly","drug_abuse","drunkenness", "dui", "embezzlement", "family_o", "forgery", "fraud", "gambling", "larceny", "liquor", "loitering", "manslaughter", "murder", "mvt", "prostitution", "rape", "robbery", "sex_o", "s_assault", "stolen_p", "suspicion", "trafficking", "vagrancy", "vandalism", "weapons"]
    
    maximum = 0
    category = ""

    for i in range(len(tup_of_all_arrests_for_each_category)):
        if tup_of_all_arrests_for_each_category[i] > maximum:
            maximum = tup_of_all_arrests_for_each_category[i]
            category = categories_list[i] 

    return category

#from each state, took the crime category that had the most arrests. saw how often each category appeared
#to have the most arrests for the other states / counted the appearance of categories with most arrests
def us_most_arrests_categories_viz(cur, conn, year_one, year_two):
    cur.execute('SELECT state_id FROM State_Crimes WHERE year = ?', (year_one,))
    all_state_abbrev = cur.fetchall()
    list_of_states_abbrev = []

    list_of_most_arrest_categories = []
    dict_of_category_and_count = {}

    for tup in all_state_abbrev:
        list_of_states_abbrev.append(tup[0])

    for state_abbrev in list_of_states_abbrev:
        crime_category = most_arrests_for(cur, conn, state_abbrev, year_one)
        list_of_most_arrest_categories.append(crime_category)

    for category in list_of_most_arrest_categories:
        dict_of_category_and_count[category] = dict_of_category_and_count.get(category, 0) + 1

    labels = []
    sizes = []

    for category in dict_of_category_and_count.keys():
        labels.append(category)
    for count in dict_of_category_and_count.values():
        sizes.append(count)

    colors = ['magenta', 'lightskyblue', 'yellowgreen', 'gold', 'pink', 'lightcoral', 'red', 'blue', 'green']

    plt.figure()
    plt.subplot(121)
    plt.title("US Arrests Mainly For These Crime Categories \n (excludes the other category) in " + str(year_one))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
    plt.axis('equal')

    cur.execute('SELECT state_id FROM State_Crimes WHERE year = ?', (year_two,))
    all_states_abbrev = cur.fetchall()
    list_states_abbrev = []

    list_most_arrest_categories = []
    dict_category_and_count = {}

    for tup in all_states_abbrev:
        list_states_abbrev.append(tup[0])

    for state_abbrev in list_of_states_abbrev:
        crime_category_year_two = most_arrests_for(cur, conn, state_abbrev, year_two)
        list_most_arrest_categories.append(crime_category_year_two)

    for category in list_most_arrest_categories:
        dict_category_and_count[category] = dict_category_and_count.get(category, 0) + 1

    labels_two = []
    sizes_two = []

    for category in dict_category_and_count.keys():
        labels_two.append(category)
    for count in dict_category_and_count.values():
        sizes_two.append(count)

    plt.subplot(122)
    plt.title("US Arrests Mainly For These Crime Categories \n (excludes the other category) in " + str(year_two))
    plt.pie(sizes_two, labels=labels_two, autopct='%1.1f%%', colors=colors)
    plt.axis('equal')
    
    plt.tight_layout(w_pad=-5)
    plt.show()

#using demo_api.py and table City_Demos
#perhaps which demographic most populates each state?

#average median age for dangerous cities vs safe cities
def average_age_by_city_type(cur, conn):
    #find average median age for dangerous cities
    cur.execute('SELECT med_age FROM City_Demos WHERE type = "D"')
    dangerous_city_ages = cur.fetchall()
    print(dangerous_city_ages)
    age_list = []

    for value in dangerous_city_ages:
        age = str(value)
        add_age = age.strip("(,)")
        age_list.append(add_age)

    age_total = 0
    number_of_ages = 0
    
    for age in age_list:
        age_total += float(age)
        number_of_ages += 1

    average_age_in_dangerous_city = round((age_total/number_of_ages), 1)
    print("The average age in a dangerous city is " + str(average_age_in_dangerous_city) + " year old.")

    #find average median age for safe cities
    cur.execute('SELECT med_age FROM City_Demos WHERE type = "S"')
    safe_city_ages = cur.fetchall()
    age_list = []

    for value in safe_city_ages:
        age = str(value)
        add_age = age.strip("(,)")
        age_list.append(add_age)

    age_total = 0
    number_of_ages = 0
    
    for age in age_list:
        age_total += float(age)
        number_of_ages += 1

    average_age_in_safe_city = round((age_total/number_of_ages), 1)
    print("The average age in a safe city is " + str(average_age_in_safe_city) + " year old.")

def main():
    cur, conn = access_database('crime.db')

    write_file("crime_information.txt", "The total number of arrests in 2017 in the United States is " + str(arrests_in_year(cur, conn, 2017)) + ".\nThe total number of arrests in 2018 in the United States is " + str(arrests_in_year(cur, conn, 2018)) + ".\n")

    if arrests_in_year(cur, conn, 2017) < arrests_in_year(cur, conn, 2018):
        write_file("crime_information.txt", "The total number of arrests increased from 2017 to 2018.\n\n")
    else:
        write_file("crime_information.txt", "The total number of arrests decreased from 2017 to 2018.\n\n")

    write_file("crime_information.txt", "The most amount of arrests for Michigan in 2017 (exluding the other category) come from " + most_arrests_for(cur, conn, 'MI', 2017) + ".\n")
    write_file("crime_information.txt", "The most amount of arrests for Michigan in 2018 (exluding the other category) come from " + most_arrests_for(cur, conn, 'MI', 2018) + ".\n")
    write_file("crime_information.txt", "The most amount of arrests for Delaware in 2017 (exluding the other category) come from " + most_arrests_for(cur, conn, 'DE', 2017) + ".\n")
    write_file("crime_information.txt", "The most amount of arrests for Delaware in 2018 (exluding the other category) come from " + most_arrests_for(cur, conn, 'DE', 2018) + ".\n")

    #calling of 3 OR 5 visualizations
    us_most_arrests_categories_viz(cur, conn, 2017, 2018)
    #us_most_arrests_categories_viz(cur, conn, 2018)

main()