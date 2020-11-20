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

def get_review_counts(data_path, id_col, wait=[1,1.5], url_col=None, search_terms=None, new_url_col=None, review_col_name="review_count"):
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
    driver = webdriver.Chrome('./chromedriver')
    
    # get relevant columns as lists
    urls = df[url_col]
    ids = df[id_col]
    counts = []

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

    return out_df

def evaluate_locations(data_path, scraped_df, output_path, data_id_col, scraped_id_col, data_count_col, wait=[1,1.5], url_col=None, search_terms=None, new_url_col=None, review_col_name="review_count", diff_col="difference", prop_col="proportion"):
    count_df = get_review_counts(data_path, data_id_col, wait, url_col, search_terms, new_url_col, review_col_name)
    scraped_df = pd.read_csv(scraped_df)
    out_df = count_df.join(scraped_df, on=(data_id_col, scraped_id_col))
    out_df[diff_col] = out_df[data_count_col] - out_df[review_col_name]
    out_df[prop_col] = out_df[data_count_col] / out_df[review_col_name]
    return out_df


def raw_review_count_to_int(raw_review_count):
    return int(raw_review_count.split(" ")[0].replace(",",""))


