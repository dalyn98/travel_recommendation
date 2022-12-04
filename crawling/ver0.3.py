# %%
import argparse
import re
from selenium import webdriver
import pandas as pd
from datetime import datetime
from time import sleep
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
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


def result_stat(args, travel):
    place = [] #관광지명
    score = [] #별점
    review_cnt = [] #리뷰수
    result_list = []

    driver.get(args.search_base + travel)
    sleep(5)
    try:
        result_id = driver.find_element_by_id('result-stats')
        result_stats = string_slice(result_id.text)
        return result_stats
    except:
        text = '0'
        return text




def data2frame(args, total_list):
    df = pd.read_csv(args.data_path).drop('Unnamed: 0', axis=1)
    # temp_df = df['관광지명'].to_frame()
    # temp_df['검색결과'] = result_list
    df['검색건수']=total_list['검색건수']
    df['지도상 관광지명'] = total_list['지도상 관광지명']
    df['별점'] = total_list['별점']
    df['리뷰개수'] = total_list['리뷰개수']


    return df


def string_slice(text):
    string = text[7:-10]
    slice_string = re.sub(',', '', string)

    return slice_string

def place_search(travel,driver):
    driver.get('https://www.google.com/maps/search/' + travel)


    #지명
    element = driver.find_elements_by_class_name('fontHeadlineLarge')

    if len(element) == 0: #결과값이 없거나 여러 개일 경우
        elements = driver.find_elements_by_class_name('fontHeadlineSmall')
        if len(elements) > 0: #결과값이 여러 개일 경우
            for element in elements:
                #print("지명: "+element.text)
                place = element.text
                return place
        else: #결과값이 없을 경우
            print("지명: 오류")
            place = f'오류: {travel}'
            return place
    else:
        elements = element[0].find_elements_by_tag_name('span')
        for element in elements: #결과값 리스트 추가
            #print("지명: "+element.text)
            place = element.text
            return place
def star_search(driver):
    xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[1]/span/span[1]'
    class_name = 'MW4etd'
    try:
        elements = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,class_name)))
        elements = driver.find_elements_by_class_name(class_name)
        temp = []
        for element in elements:
            temp.extend(element.text)
        if temp == []:
            elements = []
    except:
        elements = []
    
    if elements == []:
        try:
            elements = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath)))
        except:
            return 'None'
        elements = driver.find_elements_by_xpath(xpath)
    if len(elements) == 0: #결과값이 없거나 여러 개일 경우
        elements = driver.find_elements_by_class_name('fontDisplayLarge')
        if elements ==[]:
            elements = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,xpath)))
            elements = driver.find_elements_by_xpath(xpath)
        if len(elements) > 0: #결과값이 여러 개일 경우
            for element in elements:
                if (element.text != None) or (element.text != ''):
                #print("별점: "+element.text)
                    review = element.text
                    print(review)
                    return review
        else: #결과값이 없을 경우
            #print("별점: 없음")
            review = '0'
            return review
    else:
        for element in elements: #결과값 리스트 추가
            #print("별점: "+element.text)
            if (element.text != None) or (element.text != ''):
                review = element.text
                print(review)
                return review
def review_search(driver):
    xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[2]/span[1]/span'
    class_name = 'UY7F9'
    try:
        elements = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,class_name)))
        elements = driver.find_elements_by_class_name(class_name)
        temp = []
        for element in elements:
            temp.extend(element.text)
        if temp == []:
            elements = []
    except:
        elements = []
    if elements ==[]:
        try:
            elements = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,xpath)))
        except:
            return 'None'
        elements = driver.find_elements_by_xpath(xpath)
    if len(elements) == 0: #결과값이 없거나 여러 개일 경우
        elements = driver.find_elements_by_class_name('DkEaL')
        if elements ==[]:
            elements = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,xpath)))
            elements = driver.find_elements_by_xpath(xpath)
        if len(elements) > 0: #결과값이 여러 개일 경우
            for element in elements:
                if (element.text != None) or (element.text != ''):
                    text = element.text
                    text = re.sub(r'[^0-9]', '', text)
    #                 sp = text.split(' ')
    #                 if len(sp) > 1:
    #                     cnt = sp[1].strip('개')
    #                     print("리뷰: "+cnt)
    #                     review_cnt.append(cnt)
                    return text
        else: #결과값이 없을 경우
            #print("리뷰: 없음")
            return '0'
    else:
        for element in elements:  #결과값 숫자 부분만 리스트 추가
            if (element.text != None) or (element.text != ''):
                text = element.text
                text = re.sub(r'[^0-9]', '', text)
    #             print("리뷰: "+cnt)
    #             review_cnt.append(cnt)
                return text
if __name__ == '__main__':
    args = get_config()
    travel_list = search_list(args)
    
    subprocess.Popen(
        r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')  # 디버거 크롬 구동

    option = Options()
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    total_list = {'검색건수' : [],
             '지도상 관광지명' : [],
             '별점' : [],
             '리뷰개수' : []}
    try:
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
    for travel in travel_list:
        time.sleep(2)
        temp_list = []
        search_stat = result_stat(args,travel)
        driver.implicitly_wait(2)
        place_stat = place_search(travel,driver=driver)
        driver.implicitly_wait(2)
        star_stat = star_search(driver=driver)
        driver.implicitly_wait(2)
        review_stat = review_search(driver=driver)
        driver.implicitly_wait(2)
        total_list['지도상 관광지명'].append(place_stat)
        total_list['검색건수'].append(search_stat)
        total_list['별점'].append(star_stat)
        total_list['리뷰개수'].append(review_stat)
        print(travel,search_stat, place_stat,star_stat,review_stat)
    with open('temp_dict.txt','w',encoding='UTF-8') as f:
        for code,name in total_list.items():
            f.write(f'{code} : {name}\n')
    df = data2frame(args, total_list)
    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    df.to_csv('crawling_ver0.3-'+now+'.csv')

# %%
