import os
import sqlite3
import inspect 
from pprint import pprint
import csv

def main():
    global db_path
    script_dir = get_script_dir()
    db_path = os.path.join(script_dir, 'social_network.db')

    # Get the names and ages of all old people
    old_people_list = get_old_people()

    # Print the names and ages of all old people
    print_name_and_age(old_people_list)

    # Save the names and ages of all old people to a CSV file
    old_people_csv = os.path.join(script_dir, 'old_people.csv')
    save_name_and_age_to_csv(old_people_list, old_people_csv)

def get_old_people():
    
    con = sqlite3.connect('social_network.db')
    cur = con.cursor()
    
    # Query the database for all information for all people.
    cur.execute('SELECT name, age FROM people where age > 50')
    
    # Fetch all query results.
    # The fetchall() method returns a list, where each list item
    # is a tuple containing data from one row in the people table.
    all_people = cur.fetchall()
    
    # Pretty print (pprint) outputs data in an easier to read format.
    pprint(all_people)
    con.commit()
    con.close()

def print_name_and_age(name_and_age_list):
    con = sqlite3.connect('social_network.db')
    cur = con.cursor()
    
    # Execute query select name and age from people table
    cur.execute('SELECT name, age FROM people')

    # Fetch all query results.
    # The fetchall() method returns a list, where each list item
    # is a tuple containing data from one row in the people table.    
    query_result = cur.fetchall()

    # iterate through the query result and print a sentence for each person
    for person in query_result:
        print("{} is {} years old.".format(person[0], person[1]))
    con.commit 
    con.close()

def save_name_and_age_to_csv(name_and_age_list, csv_path):
    """Saves name and age of all people in provided list

    Args:
        name_and_age_list (list): (name, age) of people
        csv_path (str): Path of CSV file
    """
    con = sqlite3.connect('social_network.db')
    cur = con.cursor()
    
    # execute query to select name and age of all old people
    cur.execute('SELECT name, age FROM people WHERE age > 50')
    
    query_result = cur.fetchall()
    
    # get directory path of script and join with filename
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, 'old_people.csv')

    # write data to CSV file
    with open(file_path, mode='w', newline='') as csv_file:
        # create CSV writer object
        writer = csv.writer(csv_file)
        
        # write header row to CSV file
        writer.writerow(['Name', 'Age'])
        
        # iterate through query result and write data to CSV file
        for person in query_result:
            writer.writerow(person)
    
    con.close()   
    
def get_script_dir():
    """Determines the path of the directory in which this script resides

    Returns:
        str: Full path of the directory in which this script resides
    """
    script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
    return os.path.dirname(script_path)

if __name__ == '__main__':
   main()