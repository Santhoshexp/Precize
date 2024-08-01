"""Module to execute CRUD operation in students records"""

import json
import os

STORAGE_FILE = 'sat_exam_results.json'


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

def store_records(data:dict):
    """Method to add / save the new record or update an existing record"""
    with open(STORAGE_FILE, 'w',encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    file.close()

def get_data():
    """Method to get the data from the json file"""
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, 'r',encoding='utf-8') as file:
            return json.load(file)
    else:
        raise FileNotFoundError("The Records file is missing...")

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



def insert_data(records:dict):
    """Method to insert data into the students record"""
    name = input("Enter Name: ").strip()
    if name in records:
        print("A student with this name already exists.")
        return
    addr = input("Enter Address: ").strip()
    city = input("Enter City: ").strip()
    country = input("Enter Country: ").strip()
    pincode = input("Enter Pincode: ").strip()
    score = get_sat_score("Enter SAT Score[0 -100]: ")
    pass_ = "Pass" if score > 30 else "Fail"

    records[name] = {
        "Name": name,
        "Address": addr,
        "City": city,
        "Country": country,
        "Pincode": pincode,
        "SAT Score": score,
        "Passed": pass_
    }

    store_records(records)
    print("Record inserted successfully...")

def view_all_data(records:dict):
    """Method to list all the records stored"""
    if not records:
        print("No records available to display....\nTry inserting a record instead")
    else:
        print(json.dumps(records, indent=1))

def get_rank(records:dict):
    """Method to find the rank of a particular student"""
    name = input("Enter Name of the student , whose rank is to be identified: ").strip()
    sorted_data = sorted(records.items(), key=lambda item: item[1]['SAT Score'], reverse=True)
    for rank, (key, _) in enumerate(sorted_data, start=1):
        if key == name:
            print(f"Rank of {name} -> {rank}")
            return
    print("The record for the given name is not found.\nTry a different name instead.")

def update_score(records:dict):
    """Method to update the score for a particular student"""
    name = input("Enter Student name to update score: ").strip()
    if name not in records:
        print("The record for the given name is not found.\nTry a different name instead.")
    else:
        new_score = get_sat_score("Enter new SAT Score[0 -100]: ")
        if not new_score:
            return
        records[name]['SAT Score'] = new_score
        records[name]['Passed'] = "Pass" if new_score > 30 else "Fail"
    store_records(records)
    print("Score updated successfully.")


def delete_record(records:dict):
    """Method to delete a existing student record"""
    try:
        name = input("Enter Name to delete record: ").strip()
    except KeyboardInterrupt:
        print("\nUser terminated the score updation process.\n")
        return
    if name not in records:
        print("Record for the entered student name is not found.")
        return
    del records[name]
    store_records(records)
    print("Record deleted successfully.")

def average_sat_score_calulator(records:dict):
    """Method to calculate the average sat scores"""
    if not records:
        print("No records available to compute average.")
        return
    sum_score = sum(x['SAT Score'] for x in records.values())
    average_score = sum_score / len(records)
    print(f"Average SAT Score of the class -> {average_score:.2f}")

def filter_by_result_status(records:str):
    """Method to filter the records by the students SAT results"""
    status = input("Enter Pass/Fail to filter by status: ").lower()
    if status not in ["pass", "fail"]:
        print("Invalid status. Use only 'pass' or 'fail' to filter records.")
        return
    filtered_data = {key: val for key, val in records.items() if val['Passed'].lower() == status}
    if not filtered_data:
        print(f"No records found with status '{status}'.")
        return
    print(json.dumps(filtered_data, indent=1))

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
    data = get_data()
    mode = module_selector()
    if mode:
        modules[mode](data)


if __name__ == '__main__':
    exec_flow()
