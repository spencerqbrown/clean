import datetime
from datetime import datetime
from datetime import timedelta

def relative_to_date(time_string, current_date):
    # initialize deltas
    years_delta = 0
    weeks_delta = 0
    months_delta = 0
    days_delta = 0

    # process input string
    split_string = time_string.split(" ")[:2]

    num = split_string[0]
    if ("a" in num):
        num = 1
    else:
        num = int(num)
    
    # get deltas
    unit = split_string[1]
    if "day" in unit:
        days_delta = num
    elif "week" in unit:
        weeks_delta = num
    elif "month" in unit:
        months_delta = num
    elif "year" in unit:
        years_delta = num

    # return shifted date
    return current_date - timedelta(days=days_delta + 7*weeks_delta + 30*months_delta + 365*years_delta)

import pandas as pd

def date_converter(df, time_column_name, string_with_date, new_column_name="date", current_date=None, year_column_name="year"):
    # if no date is given, attempt to extract it
    if (current_date is None):
        current_date = extract_date_underscores(string_with_date)
    # check if a date was found
    if (current_date is None):
        raise ValueError("Could not find date in filename")
    # apply changes to df
    df[new_column_name] = df[time_column_name].apply(relative_to_date, args=(current_date,))
    df[year_column_name] = df[new_column_name].apply(lambda d: d.year)

import re

# as far as I know this function does not work at all
def extract_date(date_string):
    return_date = None
    date = re.search(r"\d{4}-\d{2}-\d{2}", date_string).group(0)
    if not date:
        return_date = datetime.strptime(date, "%Y-%m-%d")
    return return_date

def extract_date_underscores(date_string):
    return_date = None
    date = re.search(r"\d{1,2}_\d{2}_\d{2,4}", date_string).group(0)
    if date:
        date_pieces = date.split("_")
        year = date_pieces[2]
        month = date_pieces[0]
        day = date_pieces[1]
        return_date = datetime(year=int(year),
                                month=int(month),
                                day=int(day))
    return return_date