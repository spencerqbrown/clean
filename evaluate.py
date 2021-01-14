def generate_google_link(search_terms):
    base_string = "https://www.google.com/search?q="
    if not isinstance(search_terms, list):
        search_terms = list(search_terms)

    url = base_string + search_terms[0]
    if len(search_terms) > 1:
        for term in search_terms[1:]:
            url += "+" + str(term).replace("&", "")
    
    return url


def add_url_column(df, search_terms, new_col_name):
    df[new_col_name] = df.loc[:, search_terms].apply(generate_google_link, axis=1)


import pandas as pd
from selenium import webdriver
from scroll import pauseScroll

def get_review_counts(data_path, id_col, output_path, wait=[1,1.5], url_col=None, search_terms=None, new_url_col=None, review_col_name="review_count"):
    df = pd.read_csv(data_path)

    # if necessary, build urls
    if url_col is None:
        if search_terms is None:
            raise ValueError
        if new_url_col is None:
            raise ValueError
        add_url_column(df, search_terms, new_url_col)
        url_col = new_url_col

    # start up selenium
    driver = webdriver.Chrome('./cd/chromedriver')
    
    # get relevant columns as lists
    urls = df[url_col]
    ids = df[id_col]
    counts = [None]*len(ids)

    for i in range(len(urls)):
        # get url
        url = urls[i]

        # visit url
        driver.get(url)
        pauseScroll(wait)

        # find review count if possible
        reloads = 0
        keep_going = True
        while (keep_going):
            button = driver.find_elements_by_xpath("//span[@class='hqzQac']//a[@role='button']")
            if (len(button) > 0):
                # button found
                text = button[0].text
                review_count = raw_review_count_to_int(text)
                keep_going = False
            else:
                driver.get(url)
                pauseScroll(wait)
                reloads += 1
                if reloads >= 5:
                    keep_going = False

        # if review count could not be found, use NA
        if reloads >= 5:
            review_count = None

        # set review count for location
        counts[i] = review_count

    # combine id, review counts
    id_review_dict = {id_col:ids, review_col_name:counts}
    out_df = pd.DataFrame.from_dict(id_review_dict)

    driver.quit()
    out_df.to_csv(output_path, index=False)

    return out_df

def evaluate_locations(data_path, scraped_path, output_path, counts_output_path, id_col, data_count_cols, wait=[1,1.5], url_col=None, search_terms=None, new_url_col=None, scraped_col_name="reviews_scraped", review_col_name="review_count", diff_col="difference", prop_col="proportion"):
    count_df = get_review_counts(data_path, id_col, counts_output_path, wait, url_col, search_terms, new_url_col, review_col_name)
    scraped_df = pd.read_csv(scraped_path)
    out_df = pd.merge(count_df, scraped_df, on=[id_col])

    total_review_count = out_df[data_count_cols].sum(axis=1)

    out_df[diff_col] = total_review_count - out_df[review_col_name]
    out_df[prop_col] = total_review_count / out_df[review_col_name]
    out_df[scraped_col_name] = total_review_count
    out_df.to_csv(output_path, index=False)


def raw_review_count_to_int(raw_review_count):
    return int(raw_review_count.split(" ")[0].replace(",",""))

from utilities import get_files

def evaluate_all(data_path, scraped_directory_path, output_directory_path, counts_output_path, id_col, data_count_cols, wait=[1,1.5], url_col=None, search_terms=None, new_url_col=None, scraped_col_name="reviews_scraped", review_col_name="review_count", diff_col="difference", prop_col="proportion"):
    count_df = get_review_counts(data_path, id_col, counts_output_path, wait, url_col, search_terms, new_url_col, review_col_name)

    for file in get_files(scraped_directory_path, "csv"):

        scraped_path = file
        scraped_df = pd.read_csv(scraped_path)
        out_df = pd.merge(count_df, scraped_df, on=[id_col])

        total_review_count = out_df[data_count_cols].sum(axis=1)

        out_df[diff_col] = total_review_count - out_df[review_col_name]
        out_df[prop_col] = total_review_count / out_df[review_col_name]
        out_df[scraped_col_name] = total_review_count

        out_df = out_df[[id_col, scraped_col_name, diff_col, prop_col, review_col_name]]

        filename = file.split("\\")[-1].split(".")[0]
        output_path = output_directory_path + "\\" + filename + "_evaluation.csv"
        out_df.to_csv(output_path, index=False)
        print("Saved file as " + output_path)

