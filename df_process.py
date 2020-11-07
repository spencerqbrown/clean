
import pandas as pd
import numpy as np

def create_record(df, company_id, address, chain_name, text_directory, year_column="year", rating_column="stars"):
    # initialize dictionary
    record_dict = {"Store Company ID":company_id, 
                    "Store Address":address, 
                    "Store Chain Name":chain_name, 
                    "Mean Rating (2020)":None,
                    "Mean Rating (2019)":None, 
                    "Mean Rating (2018)":None, 
                    "Mean Rating (2017)":None, 
                    "Mean Rating (2016)":None, 
                    "Mean Rating (2015)":None, 
                    "Mean Rating (2014)":None, 
                    "Mean Rating (2013)":None, 
                    "Mean Rating (2012)":None, 
                    "Standard Deviation of Ratings (2020)":None, 
                    "Standard Deviation of Ratings (2019)":None, 
                    "Standard Deviation of Ratings (2018)":None, 
                    "Standard Deviation of Ratings (2017)":None, 
                    "Standard Deviation of Ratings (2016)":None, 
                    "Standard Deviation of Ratings (2015)":None, 
                    "Standard Deviation of Ratings (2014)":None, 
                    "Standard Deviation of Ratings (2013)":None, 
                    "Standard Deviation of Ratings (2012)":None, 
                    "Number of Ratings (2020)":None,
                    "Number of Ratings (2019)":None,
                    "Number of Ratings (2018)":None,
                    "Number of Ratings (2017)":None,
                    "Number of Ratings (2016)":None,
                    "Number of Ratings (2015)":None,
                    "Number of Ratings (2014)":None,
                    "Number of Ratings (2013)":None,
                    "Number of Ratings (2012)":None,
                    "Text Ratings (2020)":None,
                    "Text Ratings (2019)":None,
                    "Text Ratings (2018)":None,
                    "Text Ratings (2017)":None,
                    "Text Ratings (2016)":None,
                    "Text Ratings (2015)":None,
                    "Text Ratings (2014)":None,
                    "Text Ratings (2013)":None,
                    "Text Ratings (2012)":None,}
    
    for year in range(2012, 2021):
        entries = df[df[year_column]==year]
        record_dict["Mean Rating (" + str(year) + ")"] = np.mean(entries[rating_column])
        record_dict["Standard Deviation of Ratings (" + str(year) + ")"] = np.std(entries[rating_column])
        record_dict["Number of Ratings (" + str(year) + ")"] = len(entries)
        # create ratings link
        filename = chain_name + "_reviews_" + company_id + str(year) + ".csv"
        if (text_directory[-2:] != "\\"):
            text_directory = text_directory + "\\"
        link = text_directory + filename
        record_dict["Text Ratings (" + str(year) + ")"] = '=HYPERLINK("' + link + '", "Link to reviews")'
        entries.to_csv(link, index=False)
    

    return record_dict


import glob

def get_files(directory_path, extension):
    if (directory_path[-2:] != "\\"):
        directory_path = directory_path + "\\"
    search_string = directory_path + "*." + extension
    return glob.glob(search_string)


import re
from date_process import date_converter

def combine_directory(directory_path, company_name, text_directory, address_col, time_col_name, current_date, date_col_name="date", year_column=True, year_column_name="year", id_rule="col", id_col="Company ID"):
    files = get_files(directory_path, "csv")
    records = []
    for file in files:
        df = pd.read_csv(file)
        # get id
        if id_rule == "col":
            company_id = df[id_col][0]
        elif id_rule == "filename":
            file_split = file.split("\\")
            if (len(file_split[-1]) == 0):
                filename = file_split[-2]
            else:
                filename = file_split[-1]
            company_id = re.search(r"^\d{10}", filename).group(0)

        # process dates
        date_converter(df, time_col_name, file, date_col_name, current_date, year_column, year_column_name)

        # create record and append to list
        records.append(create_record(df, company_id, df[address_col][0], company_name, text_directory))

    combined_df = pd.DataFrame.from_records(records)
    final_filename = company_name + "_" + company_id + ".csv"
    combined_df.to_csv(final_filename, index=False)
        

