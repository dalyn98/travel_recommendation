import argparse
import re
from selenium import webdriver
import pandas as pd
from datetime import datetime

def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('--search_base', type=str, default='https://google.com/search?q=',
                        help='search base link (default : https://google.com/search?q=)')
    parser.add_argument('--data_path', type=str, default='./수집데이터/09-20누나수집.csv',
                        help='data path, (default : ./수집데이터/09-20누나수집.csv)')
    parser.add_argument('--driver_path', type=str, default='./chromedriver')

    args = parser.parse_args()
    return args


def search_list(args):
    df = pd.read_csv(args.data_path).drop('Unnamed: 0', axis=1)
    travel_list = df['관광지명'].to_list()

    return travel_list


def result_stat(args, travel_list):
    driver = webdriver.Chrome(args.driver_path)
    result_list = []

    for i in range(len(travel_list)):
        driver.get(args.search_base + travel_list[i])
        try:
            result_id = driver.find_element_by_id('result-stats')
            text = string_slice(result_id.text)
        except:
            page_id = driver.find_element_by_class_name('fl')
            link = page_id.get_attribute('href')
            driver.get(link)
            #print(page_id.get_attribute('href'))
            result_id = driver.find_element_by_id('result-stats')
            text = string_slice(result_id.text)
        result_list.append(text)
        print(text)

    return result_list


def data2frame(args, result_list):
    df = pd.read_csv(args.data_path).drop('Unnamed: 0', axis=1).iloc[:3]
    # temp_df = df['관광지명'].to_frame()
    # temp_df['검색결과'] = result_list
    df['검색건수']=result_list

    return df


def string_slice(text):
    string = text[7:-10]
    slice_string = re.sub(',', '', string)

    return slice_string


if __name__ == '__main__':
    args = get_config()
    travel_list = search_list(args)
    result = result_stat(args, travel_list)
    df = data2frame(args, result)

    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    df.to_csv('crawling_ver0.1-'+now+'.csv')