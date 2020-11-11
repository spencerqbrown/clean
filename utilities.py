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
