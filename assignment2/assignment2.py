import csv
import traceback
import os
from datetime import datetime
import custom_module


def read_employees():
    data = {}
    rows = []
    try:
        with open("../csv/employees.csv", newline='') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i == 0:
                    data["fields"] = row
                else:
                    rows.append(row)
        data["rows"] = rows
        return data

    except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = []
        for trace in trace_back:
            stack_trace.append(
                f'File: {trace[0]}, Line: {trace[1]}, Func: {trace[2]}, Message: {trace[3]}')
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")
        exit(1)


def column_index(column_name):
    return employees["fields"].index(column_name)


employees = read_employees()
employee_id_column = column_index("employee_id")


def first_name(id):
    id = str(id)
    for row in employees["rows"]:
        if row[employee_id_column] == id:
            return row[column_index("first_name")]


def employee_find(id):
    id = str(id)
    matches = []
    for row in employees["rows"]:
        if row[employee_id_column] == id:
            matches.append(row)
    return matches


def employee_find_2(id):
    id = str(id)
    matches = list(
        filter(lambda row: row[employee_id_column] == id, employees["rows"]))
    return matches


def sort_by_last_name():
    last_name_col = column_index("last_name")
    employees["rows"].sort(key=lambda row: row[last_name_col])
    return employees["rows"]


sort_by_last_name()


def employee_dict(row):
    return {k: v for k, v in zip(employees["fields"], row) if k != "employee_id"}


def all_employees_dict():
    return {row[employee_id_column]: employee_dict(row) for row in employees["rows"]}


def get_this_value():
    return os.getenv("THISVALUE")


def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)


def read_minutes():
    def read_file(path):
        data = {}
        rows = []
        with open(path, newline='') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i == 0:
                    data["fields"] = row
                else:
                    rows.append(tuple(row))
        data["rows"] = rows
        return data

    minutes1 = read_file("../csv/minutes1.csv")
    minutes2 = read_file("../csv/minutes2.csv")
    return minutes1, minutes2


minutes1, minutes2 = read_minutes()


def create_minutes_set():
    global minutes_set
    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])
    minutes_set = set1 | set2
    return minutes_set


minutes_set = create_minutes_set()


def create_minutes_list():
    global minutes_list
    minutes_list = list(minutes_set)
    minutes_list = list(
        map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), minutes_list))
    return minutes_list


minutes_list = create_minutes_list()


def write_sorted_list():
    minutes_list.sort(key=lambda x: x[1])
    sorted_data = list(
        map(lambda x: (x[0], x[1].strftime("%B %d, %Y")), minutes_list))
    with open("./minutes.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(minutes1["fields"])
        writer.writerows(sorted_data)
    return sorted_data


write_sorted_list()
