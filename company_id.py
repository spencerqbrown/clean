import pandas as pd
from utilities import get_files
import numpy as np

def add_company_id(file_path, master_df, key_col, master_df_key_col, master_df_id_col, id_col_name, output_directory, base_filename=None):
    df  = pd.read_csv(file_path)
    key = df[key_col][0]
    subset = master_df[master_df[master_df_key_col] == key]
    company_ids = subset[master_df_id_col]
    company_id = np.array(company_ids)[0]
    df[id_col_name] = company_id
    if output_directory[-2:] != "\\":
        output_directory = output_directory + "\\"

    # get output filename
    if base_filename is None:
        file_split = file_path.split("\\")
        if (len(file_split[-1]) == 0):
            output_filename = file_split[-2]
        else:
            output_filename = file_split[-1]
    else:
        output_filename = base_filename + "_" + str(company_id) + ".csv"
    outpath = output_directory + output_filename
    print("Saving to " + outpath)
    df.to_csv(outpath, index=False)

import re

def add_company_ids(directory_path, master_df_path, key_col, master_df_key_col, master_df_id_col, id_col_name, output_directory):
    files = get_files(directory_path, "csv")
    print(len(files))
    master_df = pd.read_excel(master_df_path)
    for file in files:
        print("File: " + file)

        dir_split = directory_path.split("\\")
        if (len(dir_split[-1]) == 0):
            raw_base = dir_split[-2]
        else:
            raw_base = dir_split[-1]
        base_filename = re.sub(r"\d", "", raw_base).strip("_")

        add_company_id(file_path=file, 
                        master_df=master_df, 
                        key_col=key_col, 
                        master_df_key_col=master_df_key_col, 
                        master_df_id_col=master_df_id_col, 
                        id_col_name=id_col_name, 
                        output_directory=output_directory,
                        base_filename = base_filename)
