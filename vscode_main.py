from doctest import master
import json
import os
from xxlimited import new
from collections import OrderedDict


NUM_STUDENTS = 1000
SUBJECTS = ["math", "science", "history", "english", "geography"]

# Dictionary to store all student files

aggregate_dict = {}


def load_report_card(directory, student_number):
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, f"{student_number}.json")
    path = os.path.join(base_path, file_path)

    try:
        with open(path, "r") as file:
            report_card = json.load(file)
    except FileNotFoundError:
        return {}

    return report_card


# Use a for-loop to add json files (loaded as dicts) to 'master' dictionary
# For now the key of each student is the 'id' key from the JSON file. Going to keep it for now but might be a good idea to remove eventually i.e. duplicates

for student_id in range(NUM_STUDENTS):
    student_temp_data = load_report_card("students", student_id)
# Remove id from student info; instead the 'key' for the master dict will be student_id
    del student_temp_data['id']
    aggregate_dict[student_id] = student_temp_data


# Let's play around and try and calculate the 'average student grade;' first parameter of output 'report'
# Function below takes the 'basic' aggregate dict; returns dict with new (key: value) pair --> avg_grade : **%

def add_avg_student_grade(master_dictionary):

    for student_id in master_dictionary.keys():
        grade_sum = 0
        for subject in SUBJECTS:
            grade_sum += master_dictionary[student_id][subject]
        avg_grade = grade_sum / len(SUBJECTS)
        master_dictionary[student_id]["avg_grade"] = avg_grade
    
    return master_dictionary

# Too keep the code more versatile; just add avg for each student; NOT aggregate

# Below function returns aggregate average; average of ALL the students

def get_aggregate_student_average(master_dictionary):

    grade_sum = 0
    for student_id in master_dictionary:
        grade_sum += master_dictionary[student_id]["avg_grade"]
    agg_avg = round(grade_sum / NUM_STUDENTS, 2)

    return agg_avg

# To get aggregate avg. 

student_avg_added_dict = add_avg_student_grade(aggregate_dict)
aggr_avg = get_aggregate_student_average(student_avg_added_dict)

# Hardest & Easiest Subjects
# Initialize dictionary to put avg. grade for each subject

subjects_dictionary = {}

for subject in SUBJECTS:
    subjects_dictionary[subject] = 0

# Function that returns dict containing averages for each subject
# Takes in subjects dictionary ABOVE as parameter; only returns this dictionary

def get_avg_grade_for_subjects(master_dictionary, subjects_dictionary):

    for student_id in master_dictionary.keys():
        for subject in SUBJECTS:
            subjects_dictionary[subject] += master_dictionary[student_id][subject]

# Below for loop replaces rolling sums with avg   

    for subject, rollingSum in subjects_dictionary.items():
         avg = rollingSum / NUM_STUDENTS
         avg = round(avg, 2)
         subjects_dictionary[subject] = avg
    
    return subjects_dictionary

avg_grade_dictionary= get_avg_grade_for_subjects(aggregate_dict, subjects_dictionary)

# Function to return the 'hardest' course from avg_grade_dictionary
# Loop through avg_grade_dict and find the lowest avg. 

def get_min_in_simple_dict(avg_grade_dict):

    min_key = ""
    min_value = 0

    for subject, avg in avg_grade_dict.items():
        if min_key == "":
            min_key = subject
            min_value = avg
        elif min_value > avg:
            min_key = subject
            min_value = avg
    
    return min_key

hardest_course = get_min_in_simple_dict(avg_grade_dictionary)


# Function to get easiest course; similiar to above

def get_max_in_simple_dict(avg_grade_dict):

    max_key = ""
    max_value = 0

    for subject, avg in avg_grade_dict.items():
        if max_key == "":
            max_key = subject
            max_value = avg
        elif max_value < avg:
            max_key = subject
            max_value = avg
    
    return max_key

easiest_course = get_max_in_simple_dict(avg_grade_dictionary)


# To find best & worst performing grades
# Function below will return dict containing key: value --> grade: avg%


def get_avg_each_grade(student_avg_added_dict):

    avg_each_grade_dict = {}

    for student_info in student_avg_added_dict.values():
        if student_info['grade'] not in avg_each_grade_dict.keys():
            avg_each_grade_dict[student_info['grade']] = [student_info['avg_grade'], 1]
        else:
            avg_each_grade_dict[student_info['grade']][0] += student_info['avg_grade']
            avg_each_grade_dict[student_info['grade']][1] += 1
    
    for grade in avg_each_grade_dict.keys():
        avg = avg_each_grade_dict[grade][0] / avg_each_grade_dict[grade][1]
        avg = round(avg, 2)
        avg_each_grade_dict[grade] = avg
    
    return avg_each_grade_dict

avg_per_grade_dict = get_avg_each_grade(student_avg_added_dict)

best_performing_grade = get_max_in_simple_dict(avg_per_grade_dict)
worst_performing_grade = get_min_in_simple_dict(avg_per_grade_dict)

# Last - need to find the Best & Worst performing student ID's, respectively
# Going to initialize new dictionary containing only ONE key: value --> student_id: avg%
# This way I can reuse functions above to get the min & max i.e. worst and best performing students

student_avg_dict = {}

for studentID, studentInfo in student_avg_added_dict.items():
    student_avg_dict[studentID] = student_avg_added_dict[studentID].get('avg_grade')

# Worst Student

worst_performing_student = get_min_in_simple_dict(student_avg_dict)

# Best Student

best_performing_student = get_max_in_simple_dict(student_avg_dict)

# Write performance summary to text file in the same directory as main.py

with open("Performance_Summary.txt", "w") as file:
    file.write(f"Average Student Grade: {aggr_avg}\n")
    file.write(f"Hardest Subject: {hardest_course}\n")
    file.write(f"Easiest Subject: {easiest_course}\n")
    file.write(f"Best Performing Grade: {best_performing_grade}\n")
    file.write(f"Worst Performing Grade: {worst_performing_grade}\n")
    file.write(f"Best Student ID: {best_performing_student}\n")
    file.write(f"Worst Student ID: {worst_performing_student}\n")







