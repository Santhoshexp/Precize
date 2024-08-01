"""Module"""

import json
from pymongo import MongoClient


MONGO_URI = 'mongodb+srv://sandy:sandy234@cluster1.nhb6kt0.mongodb.net/'
DB_NAME = 'sat_records'
COLLECTION_NAME = 'records'

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


def module_selector():
    """Method to select the module"""
    try:
        mode = input("Enter 1 to insert data\nEnter 2 to View all data\nEnter 3 to Get rank\n\
Enter 4 to Update scores\nEnter 5 to Delete one record\nEnter 6 to Calculate average SAT score\n\
Enter 7 to Filter records by Pass/Fail Status\n").strip()
        mode = int(mode)
    except ValueError:
        print("Only Numeric values are supported.")
        return ""
    except KeyboardInterrupt:
        print("User terminated the process.")
        return ""
    if mode in range(1,8):
        return mode
    print("Enter numbers in the range 1 -7 only")
    return ""

def get_sat_score(msg:str):
    """Method to get the sat score"""
    try:
        score =input(msg).strip()
        score = float(score)
    except ValueError:
        print("Enter only numeric values.")
        return ""
    except KeyboardInterrupt:
        print("\nUser terminated the process.\n")
        return ""
    if score not in range(0 , 101):
        print("Invalid scores are entered.\nValid SAT scores are in the range 0 - 100")
        return ""
    return score



def insert_data():
    """Method to insert data into the students record"""
    name = input("Enter Name: ").strip()
    existing_record = collection.find_one({'Name': name})
    if existing_record:
        print(f"A record with the name '{name}' already exists.")
        update = input("Do you want to update the existing record? (yes/no): ").strip().lower()
        if update == 'yes':
            update_score(name)
        else:
            print("Inserting new record canceled.")
        return
    addr = input("Enter Address: ").strip()
    city = input("Enter City: ").strip()
    country = input("Enter Country: ").strip()
    pincode = input("Enter Pincode: ").strip()
    score = get_sat_score("Enter SAT Score[0 -100]: ")
    pass_ = "Pass" if score > 30 else "Fail"

    new_record = {
        "Name": name,
        "Address": addr,
        "City": city,
        "Country": country,
        "Pincode": pincode,
        "SAT Score": score,
        "Passed": pass_
    }
    collection.insert_one(new_record)
    print("Data inserted successfully...")

def view_all_data():
    """Method to list all the records stored"""
    records = collection.find()
    print(json.dumps(list(records), default=str, indent=1))


def get_rank():
    """Method to find the rank of a particular student"""
    name = input("Enter Name of the student , whose rank is to be identified: ").strip()
    records = list(collection.find().sort('SAT Score', -1))
    for index, record in enumerate(records):
        if record['Name'] == name:
            print(f"Rank of {name} -> {index +1}")
            return
    print("The record for the given name is not found.\nTry a different name instead.")


def update_score(name = None):
    """Method to update the score for a particular student"""
    if not name:
        name = input("Enter Student name to update score: ").strip()
    new_score = get_sat_score("Enter new SAT Score[0 -100]: ")
    update_result = collection.update_one(
        {'Name': name},
        {'$set': {'SAT Score': new_score, 'Passed': 'Pass' if new_score > 30 else 'Fail'}})
    if update_result.matched_count:
        print("Score updated successfully.")
    else:
        print("The record for the given name is not found.\nTry a different name instead.")

def delete_record():
    """Method to delete a existing student record"""
    try:
        name = input("Enter Name to delete record: ").strip()
    except KeyboardInterrupt:
        print("\nUser terminated the score updation process.\n")
        return
    delete_result = collection.delete_one({'Name': name})
    if delete_result.deleted_count:
        print("Record deleted successfully.")
    else:
        print("Record for the entered student name is not found.")

def average_sat_score_calulator():
    """Method to calculate the average sat scores"""
    records = list(collection.find())
    if not records:
        print("No records available to compute average.")
        return
    sum_score = sum(x['SAT Score'] for x in records)
    average_score = sum_score / len(records)
    print(f"Average SAT Score of the class -> {average_score:.2f}")


def filter_by_result_status():
    """Method to filter the records by the students SAT results"""
    status = input("Enter status to filter by (Pass/Fail): ")
    records = collection.find({'Passed': status})
    print(json.dumps(list(records), default=str, indent=4))

def exec_flow():
    """Main method to execute the CRUD process"""
    modules = {
        1: insert_data,
        2: view_all_data,
        3: get_rank,
        4: update_score,
        5: delete_record,
        6: average_sat_score_calulator,
        7: filter_by_result_status
    }
    mode = module_selector()
    if mode:
        modules[mode]()

if __name__ == "__main__":
    exec_flow()
