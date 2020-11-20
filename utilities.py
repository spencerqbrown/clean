import pandas as pd

def process_company_names(df, company_name_col, new_col_name):
    df[new_col_name] = df[company_name_col].apply(name_process)

def name_process(name_string):
    new_name = name_string.replace(" ","_").replace("'","").replace(".","").lower()
    return new_name

import glob

def get_files(directory_path, extension):
    if (directory_path[-2:] != "\\"):
        directory_path = directory_path + "\\"
    search_string = directory_path + "*." + extension
    return glob.glob(search_string)

def process_phone(phone_number):
    phone_string = str(phone_number)
    area = phone_string[:3]
    mid = phone_string[3:6]
    end = phone_string[6:10]
    proccessed_number = "(" + area + ")" + " " + mid + "-" + end
    return proccessed_number

def process_phone_numbers(df, phone_col, new_phone_col):
    df[new_phone_col] = df[phone_col].apply(process_phone)


import os

def replicate_folders(from_directory, to_directory):
    for folder in os.listdir(from_directory):
        os.mkdir(to_directory + "\\" + folder)

