import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np #used for calculating trendlines
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

    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filename), "w") as out_file:
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
    #print("_______ States with their Counts of Top 100 Dangerous Cities _______") 
    
    #for state_ranking in ranked_dangerous_states:
       # print(state_ranking)
    
    
    return ranked_dangerous_states

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
    #print("_______ States with their Counts of Top 100 Safest Cities _______") 
    
    #for state_ranking in ranked_safe_states:
       # print(state_ranking)
    
    return ranked_safe_states

def state_city_counts_bar_viz(cur, conn, tlsafe, tldang):

    #make new ordered tlsafe and tldang with states having their short codes rather than full names in the tuples
    otlsafe = sorted(tlsafe)
    short_code_otlsafe = []
    for tup in otlsafe:
        cur.execute('SELECT abbreviation FROM States WHERE state_name = ?', (tup[0],))
        state = cur.fetchone()
        short_code_otlsafe.append((state[0], tup[1]))

    otldang = sorted(tldang)
    short_code_otldang = []
    for tup in otldang:
        cur.execute('SELECT abbreviation FROM States WHERE state_name = ?', (tup[0],))
        state = cur.fetchone()
        short_code_otldang.append((state[0], tup[1]))

    #get a list of all state codes alphabetized to be used for the x axis
    cur.execute('SELECT abbreviation FROM States')
    x_states_tuplist = cur.fetchall()
    x_states_list = []
    for state in x_states_tuplist:
        if state[0] == 'DC':
            continue
        x_states_list.append(state[0])

    #make a list of state codes in dangerous + safe cities tuples lists to be used in next loop
    d_short_codes = []
    for tup in short_code_otldang:
        d_short_codes.append(tup[0])

    s_short_codes = []
    for tup in short_code_otlsafe:
        s_short_codes.append(tup[0])

    #add empty tuples to our dangerous + safe cities tuple lists for the states without any cities
    for state_code in x_states_list:
        if state_code in d_short_codes:
            continue
        else:
            short_code_otldang.append((state_code, 0))

    for state_code in x_states_list:
        if state_code in s_short_codes:
            continue
        else:
            short_code_otlsafe.append((state_code, 0))

    #get rid of dc in dangerous cities tuple list
    for i in range(len(short_code_otldang)-1):
        if short_code_otldang[i][0] == 'DC':
            short_code_otldang.pop(i)

    #FINALLY arrange y_axis values for safe and dangerous cities counts
    sorted_safe_y = sorted(short_code_otlsafe)
    y_safe_values = []
    for tup in sorted_safe_y:
        y_safe_values.append(tup[1])

    sorted_dang_y = sorted(short_code_otldang)
    y_dang_values = []
    for tup in sorted_dang_y:
        y_dang_values.append(tup[1])

    sorted_x_states = sorted(x_states_list)

    # data to plot
    n_groups = len(sorted_x_states)    
    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8
    
    rects1 = plt.bar(index, y_safe_values, bar_width,
    alpha=opacity,
    color='g',
    label='Safe Cities')
    
    rects2 = plt.bar(index + bar_width, y_dang_values, bar_width,
    alpha=opacity,
    color='purple',
    label='Dangerous Cities')
    
    plt.xlabel('States')
    plt.ylabel("City Counts")
    plt.title("Safe and Dangerous City Counts by State")
    plt.xticks(index + bar_width, sorted_x_states, rotation=90, fontsize=6,)
    plt.legend()
    
    plt.tight_layout()
    plt.show()

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
def most_arrests_for_each_state(cur, conn, year):
    cur.execute('SELECT state_id FROM State_Crimes WHERE year = ?', (year,))
    all_state_abbrev = cur.fetchall()
    list_of_states_abbrev = []
    list_of_states_with_category_and_amount = []

    for tup in all_state_abbrev:
        list_of_states_abbrev.append(tup[0])

    for state_abbrev in list_of_states_abbrev:
        cur.execute('SELECT ag_assault, arson, burglary, disorderly, drug_abuse, drunkenness, dui, embezzlement, family_o, forgery, fraud, gambling, larceny, liquor, loitering, manslaughter, murder, mvt, prostitution, rape, robbery, sex_o, s_assault, stolen_p, suspicion, trafficking, vagrancy, vandalism, weapons FROM State_Crimes WHERE state_id = ? and year = ?', (state_abbrev, year))
        tup_of_all_arrests_for_each_category = cur.fetchone()
    
        categories_list = ["ag_assault","arson","burglary","disorderly","drug_abuse","drunkenness", "dui", "embezzlement", "family_o", "forgery", "fraud", "gambling", "larceny", "liquor", "loitering", "manslaughter", "murder", "mvt", "prostitution", "rape", "robbery", "sex_o", "s_assault", "stolen_p", "suspicion", "trafficking", "vagrancy", "vandalism", "weapons"]
        
        maximum = 0
        category = ""

        for i in range(len(tup_of_all_arrests_for_each_category)):
            if tup_of_all_arrests_for_each_category[i] > maximum:
                maximum = tup_of_all_arrests_for_each_category[i]
                category = categories_list[i] 

        if category == "s_assault":
            category = "Simple Assault"
        elif category == "drug_abuse":
            category = "Drug Abuse"
        elif category == "dui":
            category = category.upper()
        else:
            category = category.capitalize()

        cur.execute('SELECT state_name FROM States JOIN State_Crimes ON States.id = State_Crimes.state_id WHERE State_Crimes.state_id = ?', (state_abbrev,))
        state_name = cur.fetchone()[0]

        list_of_states_with_category_and_amount.append(("State: " + state_name, "Category: " + category, "Arrests: " + str(maximum)))

    return list_of_states_with_category_and_amount

def most_arrests_for(cur, conn, state_abbrev, year):
    cur.execute('SELECT ag_assault, arson, burglary, disorderly, drug_abuse, drunkenness, dui, embezzlement, family_o, forgery, fraud, gambling, larceny, liquor, loitering, manslaughter, murder, mvt, other, prostitution, rape, robbery, sex_o, s_assault, stolen_p, suspicion, trafficking, vagrancy, vandalism, weapons FROM State_Crimes WHERE state_id = ? and year = ?', (state_abbrev, year))
    tup_of_all_arrests_for_each_category = cur.fetchone()
    
    categories_list = ["ag_assault","arson","burglary","disorderly","drug_abuse","drunkenness", "dui", "embezzlement", "family_o", "forgery", "fraud", "gambling", "larceny", "liquor", "loitering", "manslaughter", "murder", "mvt", "other", "prostitution", "rape", "robbery", "sex_o", "s_assault", "stolen_p", "suspicion", "trafficking", "vagrancy", "vandalism", "weapons"]
    
    maximum = 0
    category = ""

    for i in range(len(tup_of_all_arrests_for_each_category)):
        if tup_of_all_arrests_for_each_category[i] > maximum:
            maximum = tup_of_all_arrests_for_each_category[i]
            category = categories_list[i] 

    return category    

#from each state, took the crime category that had the most arrests. saw how often each category appeared
#to have the most arrests for the other states / counted the appearance of categories with most arrests
#2017: 45 states have the category other as the most number of arrests, 3 states have drug abuse, 2 simple assault
#2018: 45 states have the category other as the most number of arrests, 4 states have drug abuse, 1 simple assault
def us_most_arrests_categories_pie_viz(cur, conn, year_one, year_two):
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
        if category == "s_assault":
            category_name = "Simple Assault"
        elif category == "drug_abuse":
            category_name = "Drug Abuse"
        elif category == "dui":
            category_name = category.upper()
        else:
            category_name = category.capitalize()
        labels.append(category_name)
    for count in dict_of_category_and_count.values():
        sizes.append(count)

    colors = ['lightskyblue', 'lightcoral', 'yellowgreen', 'gold', 'pink', 'red', 'blue', 'green', 'magenta']

    plt.figure()
    plt.subplot(121)
    plt.title("Percentages of US States \n That Have These Top Crime Categories in " + str(year_one))
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
        if category == "s_assault":
            category_name = "Simple Assault"
        elif category == "drug_abuse":
            category_name = "Drug Abuse"
        elif category == "dui":
            category_name = category.upper()
        else:
            category_name = category.capitalize()
        labels_two.append(category_name)
    for count in dict_category_and_count.values():
        sizes_two.append(count)

    plt.subplot(122)
    plt.title("Percentages of US States \n That Have These Top Crime Categories in " + str(year_two))
    plt.pie(sizes_two, labels=labels_two, autopct='%1.1f%%', colors=colors)
    plt.axis('equal')
    
    plt.tight_layout(w_pad=-5)
    plt.show()

#without other
def most_arrests_without_other(cur, conn, state_abbrev, year):
    cur.execute('SELECT ag_assault, arson, burglary, disorderly, drug_abuse, drunkenness, dui, embezzlement, family_o, forgery, fraud, gambling, larceny, liquor, loitering, manslaughter, murder, mvt, prostitution, rape, robbery, sex_o, s_assault, stolen_p, suspicion, trafficking, vagrancy, vandalism, weapons FROM State_Crimes WHERE state_id = ? and year = ?', (state_abbrev, year))
    tup_of_all_arrests_for_each_category = cur.fetchone()
    
    categories_list = ["ag_assault","arson","burglary","disorderly","drug_abuse","drunkenness", "dui", "embezzlement", "family_o", "forgery", "fraud", "gambling", "larceny", "liquor", "loitering", "manslaughter", "murder", "mvt", "prostitution", "rape", "robbery", "sex_o", "s_assault", "stolen_p", "suspicion", "trafficking", "vagrancy", "vandalism", "weapons"]
    
    maximum = 0
    category = ""

    for i in range(len(tup_of_all_arrests_for_each_category)):
        if tup_of_all_arrests_for_each_category[i] > maximum:
            maximum = tup_of_all_arrests_for_each_category[i]
            category = categories_list[i] 

    return category

def us_most_arrests_categories_pie_viz_without_other(cur, conn, year_one, year_two):
    cur.execute('SELECT state_id FROM State_Crimes WHERE year = ?', (year_one,))
    all_state_abbrev = cur.fetchall()
    list_of_states_abbrev = []

    list_of_most_arrest_categories = []
    dict_of_category_and_count = {}

    for tup in all_state_abbrev:
        list_of_states_abbrev.append(tup[0])

    for state_abbrev in list_of_states_abbrev:
        crime_category = most_arrests_without_other(cur, conn, state_abbrev, year_one)
        list_of_most_arrest_categories.append(crime_category)

    for category in list_of_most_arrest_categories:
        dict_of_category_and_count[category] = dict_of_category_and_count.get(category, 0) + 1

    labels = []
    sizes = []

    for category in dict_of_category_and_count.keys():
        if category == "s_assault":
            category_name = "Simple Assault"
        elif category == "drug_abuse":
            category_name = "Drug Abuse"
        elif category == "dui":
            category_name = category.upper()
        else:
            category_name = category.capitalize()
        labels.append(category_name)
    for count in dict_of_category_and_count.values():
        sizes.append(count)

    colors = ['magenta', 'lightskyblue', 'yellowgreen', 'gold', 'pink', 'lightcoral', 'red', 'blue', 'green']

    plt.figure()
    plt.subplot(121)
    plt.title("Percentages of US States That Have These Top \n Crime Categories (excludes the other category) \n in " + str(year_one))
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
        crime_category_year_two = most_arrests_without_other(cur, conn, state_abbrev, year_two)
        list_most_arrest_categories.append(crime_category_year_two)

    for category in list_most_arrest_categories:
        dict_category_and_count[category] = dict_category_and_count.get(category, 0) + 1

    labels_two = []
    sizes_two = []

    for category in dict_category_and_count.keys():
        if category == "s_assault":
            category_name = "Simple Assault"
        elif category == "drug_abuse":
            category_name = "Drug Abuse"
        elif category == "dui":
            category_name = category.upper()
        else:
            category_name = category.capitalize()
        labels_two.append(category_name)
    for count in dict_category_and_count.values():
        sizes_two.append(count)

    plt.subplot(122)
    plt.title("Percentages of US States That Have These Top \n Crime Categories (excludes the other category) \n in  " + str(year_two))
    plt.pie(sizes_two, labels=labels_two, autopct='%1.1f%%', colors=colors)
    plt.axis('equal')
    
    plt.tight_layout(w_pad=-5)
    plt.show()

#using demo_api.py and table City_Demos
#average median age for dangerous cities vs safe cities
def average_age_in_dangerous_city(cur, conn):
    #find average median age for dangerous cities
    cur.execute('SELECT med_age FROM City_Demos WHERE type = "D"')
    dangerous_city_ages = cur.fetchall()
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
    #print("The average age in a dangerous city is " + str(average_age_in_dangerous_city) + " year old.")
    return str(average_age_in_dangerous_city)

def plot_median_ages_dangerous_cites(cur, conn):
    '''
    This function creates a scatter plot of the available median ages of cities over 65k population size and listed as dangerous.
    '''
    cur.execute('SELECT med_age FROM City_Demos WHERE type = "D"')
    dangerous_city_ages = cur.fetchall()
    age_list = []
    cur.execute('SELECT Dangerous_Cities.city, States.abbreviation FROM Dangerous_Cities JOIN States on Dangerous_Cities.state_id = States.id JOIN City_Demos ON Dangerous_Cities.id = City_Demos.city_id WHERE City_Demos.type = "D"')
    dangerous_city_names = cur.fetchall()
    location_list = []

    for age_value in dangerous_city_ages:
        age = str(age_value)
        add_age = age.strip("(,)")
        age_list.append(float(add_age))

    placement_list =[]
    counter = 0
    for city_value in dangerous_city_names:
        city = str(city_value[0])
        state = str(city_value[1])
        add_city = city.strip("(,)")
        add_state = state.strip("(,)")
        location_list.append(add_city + ", " + add_state)
        counter+=1
        placement_list.append(counter)
    
    #values for making trendline
    x = placement_list
    y = age_list
    #find number of points
    n = np.size(x)
    #find mean of x and y
    m_x, m_y = np.mean(placement_list), np.mean(age_list)
    rounded_age = round(m_y, 1)
    average_label = "Average\nMedian\nAge\n"+ "(" + str(rounded_age) + ")"
    
   
   #create scatter plot
    plt.figure()
    fig,ax = plt.subplots()
    plt.subplots_adjust(bottom=0.20, right=0.85)
    plt.xticks(rotation=90, fontsize=6)
    ax.scatter(location_list, age_list, color='r')
    plt.axhline(y=rounded_age, color='b', linestyle='-', label=average_label)
    ax.set_xlabel('Dangerous Cities \n (in order of most dangerous to less)')
    ax.set_ylabel('Median Age')
    ax.set_title('Median Age for U.S. Citizens in Dangerous Cities \n with a Population over 65K')
    
    #plot trendline
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x,p(x),"g--", label='Trendline')
    
    plt.legend(bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0)

    plt.show()
    
    
def average_age_in_safe_city(cur, conn):
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
    #print("The average age in a safe city is " + str(average_age_in_safe_city) + " year old.")

    return str(average_age_in_safe_city)

def plot_median_ages_safe_cites(cur, conn):
    '''
    This function creates a scatter plot of the available median ages of cities over 65k population size and listed as safe.
    '''
    cur.execute('SELECT med_age FROM City_Demos WHERE type = "S"')
    safe_city_ages = cur.fetchall()
    age_list = []
    cur.execute('SELECT Safe_Cities.city, States.abbreviation FROM Safe_Cities JOIN States on Safe_Cities.state_id = States.id JOIN City_Demos ON Safe_Cities.id = City_Demos.city_id WHERE City_Demos.type = "S"')
    safe_city_names = cur.fetchall()
    location_list = []

    for age_value in safe_city_ages:
        age = str(age_value)
        add_age = age.strip("(,)")
        age_list.append(float(add_age))

    placement_list =[]
    counter = 0
    for city_value in safe_city_names:
        city = str(city_value[0])
        state = str(city_value[1])
        add_city = city.strip("(,)")
        add_state = state.strip("(,)")
        location_list.append(add_city + ", " + add_state)
        counter+=1
        placement_list.append(counter)
    
    #values for making trendline
    x = placement_list
    y = age_list
    #find number of points
    n = np.size(x)
    #find mean of x and y
    m_x, m_y = np.mean(placement_list), np.mean(age_list)
    rounded_age = round(m_y, 1)
    average_label = "Average\nMedian\nAge\n"+ "(" + str(rounded_age) + ")"
    
    #create scatter plot
    plt.figure()
    fig,ax = plt.subplots()
    plt.subplots_adjust(bottom=0.20, right=0.85)
    plt.xticks(rotation=90, fontsize=6)
    ax.scatter(location_list, age_list, color='g')
    plt.axhline(y=rounded_age, color='b', linestyle='-', label=average_label)
    
    ax.set_xlabel('Safest Cities \n (in order of most safe to less)')
    ax.set_ylabel('Median Age')
    ax.set_title('Median Age for U.S. Citizens in Safest Cities \n with a Population over 65K')
    
    #plot trendline
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x,p(x),"r--", label='Trendline')
    
    plt.legend(bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0)

    plt.show()
    

def arrests_increase_or_decrease(cur, conn):
    if arrests_in_year(cur, conn, 2017) < arrests_in_year(cur, conn, 2018):
        return "The total number of arrests increased from 2017 to 2018.\n\n"
    else:
        return "The total number of arrests decreased from 2017 to 2018.\n\n"


def setup_state_freq_bar_viz(cur, conn, year):
    ''' looks at the top arrest category for each state (excluding other category) and plots a
        bar graph with top popular arrest categories on the x axis, and number of states with that
        category as their #1 arrest type on the y axis.
    '''
    #a list of tuples in the format [(State: [state], Category: [cat], Arrests: [value]),]
    state_arrests_tuplist = most_arrests_for_each_state(cur,conn,year)
    #create dictionary with states as keys and top crime category as value in case we later want to look at this state data
    state_cat_dict = {}
    for tup in state_arrests_tuplist:
        state = tup[0]
        cat = tup[1]
        state_cat_dict[state[7:]] = cat[10:]
    #get a frequencies dict of top crime categories from these states, then organize for plotting
    cat_freq_dict = {}
    for key in state_cat_dict:
        cat_freq_dict[state_cat_dict[key]] = cat_freq_dict.get(state_cat_dict[key],0) + 1

    ordered_plot_values_tuplist = sorted(cat_freq_dict.items(), key=lambda x: x[1],reverse=True)
    x_values_list = []
    for tup in ordered_plot_values_tuplist:
        x_values_list.append(tup[0])
    y_values_list = []
    for tup in ordered_plot_values_tuplist:
        y_values_list.append(tup[1])
    return(x_values_list, y_values_list)
   
def setup_arrest_count_bar_viz(cur, conn, year):
    ''' looks at the top arrest category for each state (excluding other category) and plots a
        bar graph with top popular arrest categories on the x axis, and number of arrests from that
        category totaled from each state on the y axis.
    '''
    #a list of tuples in the format [(State: [state], Category: [cat], Arrests: [value]),]
    state_arrests_tuplist = most_arrests_for_each_state(cur,conn,year)
    #create dictionary with categories as keys this time, and total appended crime count as value 
    cat_count_dict = {}
    for tup in state_arrests_tuplist:
        cat = tup[1][10:]
        count = tup[2][9:]
        cat_count_dict[cat] = cat_count_dict.get(cat,0) + int(count)
    #get a frequencies dict of top crime categories from these states, then organize for plotting

    ordered_plot_values_tuplist = sorted(cat_count_dict.items(), key=lambda x: x[1],reverse=True)
    x_values_list = []
    for tup in ordered_plot_values_tuplist:
        x_values_list.append(tup[0])
    y_values_list = []
    for tup in ordered_plot_values_tuplist:
        y_values_list.append(tup[1])
    return(x_values_list, y_values_list)

def top_arrest_categories_bar_viz(cur, conn, tl2017, tl2018, title, y_axis_title):
    #get x and y values to plot for both years 2017 and 2018
    x_values_2017 = tl2017[0]
    y_values_2017 = tl2017[1]
    x_values_2018 = tl2018[0]
    y_values_2018 = tl2018[1]
    #append a 0 for the extra crime category
    y_values_2018.append(0)
    # data to plot
    n_groups = len(x_values_2017)    
    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8
    
    rects1 = plt.bar(index, y_values_2017, bar_width,
    alpha=opacity,
    color='b',
    label='2017')
    
    rects2 = plt.bar(index + bar_width, y_values_2018, bar_width,
    alpha=opacity,
    color='orange',
    label='2018')
    
    plt.xlabel('Top Crime Category')
    plt.ylabel(y_axis_title)
    plt.title(title)
    plt.xticks(index + bar_width, x_values_2017)
    plt.legend()
    
    plt.tight_layout()
    plt.show()





def main():
    cur, conn = access_database('crime.db')

    information = "The total number of arrests in 2017 in the United States is " + str(arrests_in_year(cur, conn, 2017)) + ".\nThe total number of arrests in 2018 in the United States is " + str(arrests_in_year(cur, conn, 2018)) + ".\n" + arrests_increase_or_decrease(cur, conn) + "Most Amount of Arrests Come From Which Category for Each State in 2017 (excluding the Other Category) \n" + str(most_arrests_for_each_state(cur, conn, 2017)) + "\n\n" + "Most Amount of Arrests Come From Which Category for Each State in 2018 (excluding the Other Category) \n" + str(most_arrests_for_each_state(cur, conn, 2018)) + "\n\n" + "The average median age for people in dangerous cities is " + average_age_in_dangerous_city(cur, conn) + " years old.\n\n" + "The average median age for people in safe cities is " + average_age_in_safe_city(cur, conn) + " years old.\n\n" + "Count of How Many of the Top 100 Safest Cities are in Each State \n" + str(state_with_most_safe_cities(cur, conn))+ "\n\n" + "Count of How Many of the Top 100 Most Dangerous Cities are in Each State \n" + str(state_with_most_dangerous_cities(cur, conn))+ "\n\n"

    write_file("crime_information.txt", information)
   
    #calling of 7 visualizations
    #plots the amount of dangerous cities and safe cities by state in a bar chart
    state_city_counts_bar_viz(cur, conn, state_with_most_safe_cities(cur,conn), state_with_most_dangerous_cities(cur,conn))
    #plots state frequencies of top crime categories
    tuplist_state_freq_2017 = setup_state_freq_bar_viz(cur,conn,2017)
    tuplist_state_freq_2018 = setup_state_freq_bar_viz(cur,conn,2018)
    top_arrest_categories_bar_viz(cur,conn, tuplist_state_freq_2017, tuplist_state_freq_2018, 'State Frequencies of Top Crime Categories', 'State Frequencies')
    #plots total crime counts of each state's top crime categories
    tuplist_arrest_count_2017 = setup_arrest_count_bar_viz(cur, conn, 2017)
    tuplist_arrest_count_2018 = setup_arrest_count_bar_viz(cur, conn, 2018)
    top_arrest_categories_bar_viz(cur,conn, tuplist_arrest_count_2017, tuplist_arrest_count_2018, "Arrest Counts of States' Top Crime Categories", "Arrest Counts")
    #pie charts of same data
    us_most_arrests_categories_pie_viz(cur, conn, 2017, 2018)
    us_most_arrests_categories_pie_viz_without_other(cur, conn, 2017, 2018)
    #the two scatterplots
    plot_median_ages_dangerous_cites(cur, conn)
    plot_median_ages_safe_cites(cur, conn)

main()