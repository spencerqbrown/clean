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

def separate_companies(files_dir, master_file, id_col="key", master_id_col="Store Company ID", master_company_name_col="company_name", date=None):
    master = pd.read_csv(master_file)
    files = get_files(files_dir, "csv")
    for f in files:
        filename = f.split("\\")[-1]
        filepath = "\\".join(f.split("\\")[:-1])
        df = pd.read_csv(f)
        company_id = int(df[id_col][0])
        company_name = list(master[master[master_id_col]==company_id][master_company_name_col])[0]
        if date is None:
            date_string = ""
        else:
            date_string = "_" + date
        company_name_dir = filepath + "\\" + company_name + date_string
        if not os.path.isdir(company_name_dir):
            os.mkdir(company_name_dir)
        new_filepath = company_name_dir + "\\" + filename
        df.to_csv(new_filepath, index=False)


def extract_year_sheet(source_file, output_path, sheet_name, drop_columns=['Parent_ID', 'Parent Name', 'Parent City', 'Parent State', 'Parent Zip',
       'Headquarters ID', 'HQ Name', 'HQ City', 'HQ State', 'HQ Zip',
       'Store No', 'Store Weekly Volume', 'Type of Food Service', 'Menu Types',
       'FIPS', 'FIPS_DESC', 'CBSA', 'CBSA_DESC', 'MSA', 'MSA_DESC', 'PMSA',
       'PMSA_DESC', 'Lat', 'Lon', 'GeoLevel', 'Listing Type', 'Industry ID', 'Industry Name'], 
       rename_columns={"Company ID":"Store Company ID"}, 
       company_name_in="Company Name", 
       company_name_out="company_name"):
       sheet = pd.read_excel(source_file, sheet_name=sheet_name)
       sheet = sheet.rename(columns=rename_columns)
       sheet = sheet.drop(drop_columns, axis=1)
       process_company_names(sheet, company_name_in, company_name_out)
       sheet.to_csv(output_path, index=False)

def link_to_id(link, master_df, master_id_col="Store Company ID", master_link_col="Google Link"):
    company_id = list(master_df[master_df[master_link_col] == link][master_id_col])[0]
    return company_id

def link_to_id_all(master_df, df, master_id_col="Store Company ID", master_link_col="Google Link", link_col="Task URL1", id_col_name="Store Company ID"):
    df[id_col_name] = df[link_col].apply(link_to_id, args=[master_df, master_id_col, master_link_col])

import re

def html_to_stars(html_text):
    stars_text = re.search(r"\d star", html_text).group(0)
    num = stars_text.split(" ")[0]
    return int(num)

def stack_files(directory_path, output_path, extension="csv"):
    if extension == "csv":
        read_function = pd.read_csv
    elif extension == "xlsx":
        read_function = pd.read_excel
    else:
        raise ValueError

    all_files = get_files(directory_path, extension)
    if len(all_files) > 1:
        base_file = all_files[0]
        base = read_function(base_file)
        total_files = 1
        print("Setting base file: " + base_file, end='\r')
        for f in all_files[1:]:
            print("Adding file: " + f + ", " + str(total_files) + " stacked", end='\r')
            df = read_function(f)
            base = pd.concat([base, df])
            total_files += 1
        print(str(total_files) + " stacked")
        
        base.to_csv(output_path, index=False)
