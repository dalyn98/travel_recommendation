import argparse
import re
from selenium import webdriver
import pandas as pd
from datetime import datetime
from time import sleep
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess

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
    df = pd.read_csv(args.data_path).drop('Unnamed: 0', axis=1).iloc[:3]
    # temp_df = df['관광지명'].to_frame()
    # temp_df['검색결과'] = result_list
    df['검색건수']=total_list[0]
    df['지도상 관광지명'] = total_list[1]
    df['별점'] = total_list[2]
    df['리뷰개수'] = total_list[3]

    return df


def string_slice(text):
    string = text[7:-10]
    slice_string = re.sub(',', '', string)

    return slice_string

def place_search(travel,driver):
    driver.get('https://www.google.com/maps/search/' + travel)
    driver.implicitly_wait(3)


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
    elements = driver.find_elements_by_class_name('MW4etd')

    if len(elements) == 0: #결과값이 없거나 여러 개일 경우
        elements = driver.find_elements_by_class_name('fontDisplayLarge')
        if len(elements) > 0: #결과값이 여러 개일 경우
            for element in elements:
                #print("별점: "+element.text)
                review = element.text
                return review
        else: #결과값이 없을 경우
            #print("별점: 없음")
            review = '0'
            return review
    else:
        for element in elements: #결과값 리스트 추가
            #print("별점: "+element.text)
            review = element.text
            return review
def review_search(driver):
    elements = driver.find_elements_by_class_name('UY7F9')

    if len(elements) == 0: #결과값이 없거나 여러 개일 경우
        elements = driver.find_elements_by_class_name('DkEaL')
        if len(elements) > 0: #결과값이 여러 개일 경우
            for element in elements:
                text = element.text
                sp = text.split(' ')
                if len(sp) > 1:
                    cnt = sp[1].strip('개')
#                     print("리뷰: "+cnt)
#                     review_cnt.append(cnt)
                    return cnt
        else: #결과값이 없을 경우
            #print("리뷰: 없음")
            return '0'
    else:
        for element in elements:  #결과값 숫자 부분만 리스트 추가
            text = element.text
            cnt = text.strip('('')')
#             print("리뷰: "+cnt)
#             review_cnt.append(cnt)
            return cnt
if __name__ == '__main__':
    args = get_config()
    travel_list = search_list(args)
    
    subprocess.Popen(
        r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')  # 디버거 크롬 구동

    option = Options()
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    total_list = []
    try:
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
    for travel in travel_list:
        temp_list = []
        search_stat = result_stat(args,travel)
        place_stat = place_search(travel,driver=driver)
        star_stat = star_search(driver=driver)
        review_stat = review_search(driver=driver)
        
        temp_list = [search_stat,place_stat,star_stat,review_stat]
        total_list.append(temp_list)
        print(search_stat, place_stat,star_stat,review_stat)
    
    df = data2frame(args, result)
    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    df.to_csv('crawling_ver0.3-'+now+'.csv')