# 크롤링을 위해 사용자가 입력해야 되는 값
start_page = 1
refresh_unit = 200
stop_page = 1111
check_auto_save = True
file_name = 'patent_{date}_{first_page}_{last_page}.csv'
firstPage = start_page   # 값 변경하면 안 됨

# 메인
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import os
from math import ceil
import schedule

# 함수 : 딜레이
def delay(text, sec):
    print(text, end="")
    for i in range(sec): print('.', end=""); time.sleep(1)

# 함수 : 사이트에서 제목/내용 크롤링
current_page_css_selector = 'span.board_pager03 strong'
def contentCrawling(current_page_css_selector = current_page_css_selector):
    dom = BeautifulSoup(driver.page_source, 'html.parser')
    patent_list = dom.select('.search_section article')
    
    current_page = driver.find_element_by_css_selector(current_page_css_selector).text

    result = [
            {
                '제목': patent.select_one('.search_section_title h1 > a:nth-of-type(2)').text.strip(),
                '내용': patent.select_one('.search_txt').text.strip()
            }
            for patent in patent_list
    ]

    return int(current_page), result   # (크롤링한 페이지, 크롤링 결과) 반환

# 함수 : 저장할 파일 경로 찾기
def findPath(fileName):
    file_path = r'D:\DevRoot\StockHelper\dataset'
    try: 
        path = os.path.join(file_path, fileName)
    except(Exception):
        file_path = 'C:\DeepLearning_Project\StockHelper\StockHelper\dataset'
        path = os.path.join(file_path, fileName)
        
    return path

# 함수 : 파일저장
# 데이터 저장 : list -> df -> csv 저장
def saveFile(path, data):
    pd.DataFrame(data).to_csv(path, encoding='utf-8')
    # 저장 결과 반환
    if os.path.isfile(path):
        print('>>> 파일변환 완료:', datetime.today().strftime(("%Y-%m-%d %H:%M:%S")))
        print('>>> 저장위치:', path)
    else: print('>>> 파일변환 실패')
        
def job(start_page, refresh_unit, stop_page, check_auto_save, file_name):
    print('프로그램 시작')
    start = time.time()  # 프로그램 작동 시작 시간
    result = []
    check_page_list = []   # 실제 페이지 이동 결과 (페이지 이동의 중복/누락 확인용)
    check_save_point = False   # 파일 저장하는 시점 확인

    # 1. webdriver를 이용해 kipris 접속
    driver_path = r'D:\DevRoot\download\chromedriver.exe'
    global driver
    try: 
        driver = webdriver.Chrome(driver_path)
    except(Exception):
        driver_path = r'C:\DevRoot\download\chromedriver.exe'
        driver = webdriver.Chrome(driver_path)
    finally:
        driver.implicitly_wait(10)   # 웹 페이지 로딩 완료 최대 대기 시간 (한번만 설정하면 driver를 사용하는 모든 코드에 적용)

    if refresh_unit <= 0: refresh_unit = 100000000
    loop_len = (stop_page - start_page + 1) // refresh_unit + 1
    for refreshed_num in range(1, loop_len):
        print('인터넷 접속중')
        driver.get("http://kpat.kipris.or.kr/kpat/searchLogina.do?next=MainSearch")

        # 크롤링 시작페이지 재설정
        if refreshed_num != 1: start_page = refresh_unit * (refreshed_num - 1) + 1

        # 2. 검색 옵션 설정
        # 2.1. 행정상태 변경
        # defalut 해제 <- '전체' 클릭
        driver.find_element_by_css_selector('form#leftside .release_list > span:nth-of-type(1) > input').click()
        # 원하는 checkbox만 선택 <- '등록' 클릭
        driver.find_element_by_css_selector('form#leftside .release_list > span:nth-last-of-type(1) > input').click()

        # 2.2. 기간을 검색어로 입력
        today = datetime.today().strftime("%Y%m%d")
        decade = str(int(today) - int('00001000'))
        driver.find_element_by_css_selector('.keyword').send_keys(f'GD=[{decade}~{today}]')
        driver.find_element_by_css_selector('.input_btn img').click()

        # 2.3. 90개씩 보기 선택
        pageSel = 90   # 페이지당 게시물 개수 (30, 60, 90 중 택1)
        select = Select(driver.find_element_by_id('opt28'))
        select.select_by_value(str(pageSel))
        driver.find_element_by_css_selector('#pageSel img').click()

        # 3. 데이터 추출
        delay('크롤링 준비중', 3); print('완료')
        page_num = 'span.board_pager03 a:nth-last-of-type({0})'   # target_page 구할 때 이용

        # 3.1. 첫 페이지 크롤링
        current_page, data = contentCrawling()
        if current_page == stop_page: break   # 실행종료
        if current_page != start_page:   # 첫 페이지 찾기
            delay('시작 페이지로 이동', 0)
            while current_page < start_page:
                if current_page // 10 < start_page // 10:
                    driver.find_element_by_css_selector(page_num.format(1)).click()
                    delay('', 2)
                    current_page = int(driver.find_element_by_css_selector(current_page_css_selector).text)
                    continue
                for i in range(10, 0, -1):
                    driver.find_element_by_css_selector(page_num.format(i)).click()
                    delay('', 2)
                    current_page = int(driver.find_element_by_css_selector(current_page_css_selector).text)
                    if current_page == start_page: print('완료'); break
        current_page, data = contentCrawling()
        delay('', 2)
        result.extend(data)
        print(f'{current_page} 위치 -> {current_page} 페이지 크롤링 완료 / 누적 {len(result)} 건')
        check_page_list.append(current_page)

        # 3.2. 페이지 이동하며 크롤링
        while True:
            # 실행 종료
            if current_page >= stop_page: break
            if current_page == refresh_unit * refreshed_num: break

            for i in range(10, 0, -1):
                if current_page >= stop_page: break
                if current_page == refresh_unit * refreshed_num: check_save_point = True; break

                # 3.2.1. 크롤링할 페이지(target_page)가 현재 페이지의 다음 페이지인 지 확인
                target_page = driver.find_element_by_css_selector(page_num.format(i))
                if i != 1 and int(target_page.text) <= current_page: delay('', 1); continue 

                print(f'현재 {current_page}', end=" -> ")
                dataLen1 = current_page * pageSel   # 현재 페이지의 크롤링 데이터 개수
                # 3.2.2. 크롤링할 페이지(target_page)인 다음 페이지로 이동
                try:
                    print(f'{target_page.text} click', end=" -> ")
                except Exception:
                    driver.refresh()   # 새로고침
                    dealy('', 5)
                    dom = BeautifulSoup(driver.page_source, 'html.parser')
                    patent_list = dom.select('.search_section article')
                finally:
                    target_page.click()  # 크롤링할 페이지로 이동
                    delay('', 2)
                while True:
                    try: # (클릭해서 이동한) 현재 페이지(click_page)는 target_page
                        click_page = driver.find_element_by_css_selector(current_page_css_selector).text
                    except Exception:
                        driver.refresh()   # 새로고침
                        dom = BeautifulSoup(driver.page_source, 'html.parser')
                        patent_list = dom.select('.search_section article')
                        click_page = int(driver.find_element_by_css_selector(current_page_css_selector).text)

                    if current_page != click_page: break  # 페이지 이동 시 loop 탈출
                # 3.2.3. 크롤링
                try:
                    current_page, data = contentCrawling()
                except Exception:
                    driver.refresh()   # 새로고침
                    current_page, data = contentCrawling()
                finally:
                    result.extend(data)
                # 3.2.4. 중간결과 반환
                dataLen2 = current_page * pageSel   # 현재 페이지의 크롤링 데이터 개수
                print(f'{current_page} 크롤링 완료 / 누적 {len(result)} 건')
                check_page_list.append(current_page)

        # 4.1. 파일 저장
        if check_save_point and check_auto_save:
            print('=' * 60)
            fileName = file_name.format(date=today, first_page=start_page, last_page=current_page)
            saveFile(path=findPath(fileName), data=result)

            # 4.2. 저장 결과
            print('예상 데이터 개수 :', (current_page - start_page + 1) * pageSel)
            print('긁어온 데이터개수 :', len(result))
            normal_page_list = [i for i in range(start_page, current_page + 1)]   # 정상적으로 크롤링했을 때
            num = len(normal_page_list)
            for i in range(start_page, current_page + 1):
                if i in check_page_list:
                    check_page_list.pop(check_page_list.index(i))
                    normal_page_list.pop(normal_page_list.index(i))
            print('중복된 페이지 :', check_page_list if check_page_list else '없음')
            print('누락된 페이지 :', normal_page_list if normal_page_list else '없음')
            print('=' * 60)
            check_page_list = []
            normal_page_list = []
            check_save_point = False
            result = []


    print('=' * 60)
    if not check_auto_save: start_page = firstPage
    fileName = file_name.format(date=today, first_page=start_page, last_page=stop_page)
    saveFile(path=findPath(fileName), data=result)
    print('예상 데이터 개수 :', (stop_page - start_page + 1) * pageSel)
    print('긁어온 데이터개수 :', len(result))
    normal_page_list = [i for i in range(start_page, current_page + 1)]   # 정상적으로 크롤링했을 때
    num = len(normal_page_list)
    for i in range(start_page, current_page + 1):
        if i in check_page_list:
            check_page_list.pop(check_page_list.index(i))
            normal_page_list.pop(normal_page_list.index(i))
    print('중복된 페이지 :', check_page_list if check_page_list else '없음')
    print('누락된 페이지 :', normal_page_list if normal_page_list else '없음')
    print('소요시간 :', int(time.time() - start) / 60, '분')  # 현재시각 - 시작시간 = 실행 시간
    print('프로그램 종료')
    
# [참고] schedule 모듈 : https://blog.daum.net/geoscience/1626
# [참고] cmd pyinstaller 모듈 : https://dvlp-jun.tistory.com/26 
# 매일 특정시간에 동작
schedule.every().day.at("01:00").do(job(start_page, refresh_unit, stop_page, check_auto_save, file_name))
while True:
    schedule.run_pending()
    time.sleep(1)