# 필요 library import
from selenium import webdriver
import pandas as pd


# 검색 데이터 로드
df = pd.read_csv('tourismData.csv').drop('Unnamed: 0', axis=1)
travel_list = df['관광지명'].to_list()
travel_list


# 구글지도 별점 리뷰 정보 크롤링
driver = webdriver.Chrome('chromedriver')
place = [] #관광지명
score = [] #별점
review_cnt = [] #리뷰수

n = 0

try:
    for i in range(len(travel_list)):
        driver.get('https://www.google.com/maps/search/' + travel_list[i])
        driver.implicitly_wait(3)
        
        n += 1

        #print(travel_list[i])
        print(n,'/',len(travel_list))

        #지명
        element = driver.find_elements_by_class_name('fontHeadlineLarge')

        if len(element) == 0: #결과값이 없거나 여러 개일 경우
            elements = driver.find_elements_by_class_name('fontHeadlineSmall')
            if len(elements) > 0: #결과값이 여러 개일 경우
                for element in elements:
                    print("지명: "+element.text)
                    place.append(element.text)
                    break
            else: #결과값이 없을 경우
                print("지명: 오류")
                place.append('오류: '+travel_list[i])
                break
        else:
            elements = element[0].find_elements_by_tag_name('span')
            for element in elements: #결과값 리스트 추가
                print("지명: "+element.text)
                place.append(element.text)
                break


        # 별점
        elements = driver.find_elements_by_class_name('MW4etd')

        if len(elements) == 0: #결과값이 없거나 여러 개일 경우
            elements = driver.find_elements_by_class_name('fontDisplayLarge')
            if len(elements) > 0: #결과값이 여러 개일 경우
                for element in elements:
                    print("별점: "+element.text)
                    score.append(element.text)
                    break
            else: #결과값이 없을 경우
                print("별점: 없음")
                score.append("")
                break
        else:
            for element in elements: #결과값 리스트 추가
                print("별점: "+element.text)
                score.append(element.text)
                break

        # 리뷰수
        elements = driver.find_elements_by_class_name('UY7F9')

        if len(elements) == 0: #결과값이 없거나 여러 개일 경우
            elements = driver.find_elements_by_class_name('DkEaL')
            if len(elements) > 0: #결과값이 여러 개일 경우
                for element in elements:
                    text = element.text
                    sp = text.split(' ')
                    if len(sp) > 1:
                        cnt = sp[1].strip('개')
                        print("리뷰: "+cnt)
                        review_cnt.append(cnt)
                        break
            else: #결과값이 없을 경우
                print("리뷰: 없음")
                review_cnt.append("")
                break
        else:
            for element in elements:  #결과값 숫자 부분만 리스트 추가
                text = element.text
                cnt = text.strip('('')')
                print("리뷰: "+cnt)
                review_cnt.append(cnt)
                break    

finally: #결과 리트스 데이터프레임화
    result = pd.DataFrame((zip(place, score, review_cnt)), columns = ['관광지', '별점', '리뷰수'])
result


# 데이터 파일로 저장
result.to_csv("crawling_score.csv", mode='w')