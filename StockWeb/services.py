import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os
import time
from datetime import datetime, timedelta
from google.cloud import language_v1

#---------- 기사 정제하기----------------
# 텍스트 데이터 정제
def data_refine(data):
    # 제거할 단어들 불러오기
    with open('static/data/except_words.txt', 'r', encoding='utf-8') as f:
        except_words = list(map(lambda line: line.replace('\n', ''), f.readlines()))

    # 제거 패턴 (금칙어)
    for ex_word in except_words:
        data = re.sub(ex_word, '', str(data))
        
    # <br/> 태그 제거
    data = data.replace('<br/>', '')
        
    # 특수문자 제거 (알파벳, 숫자, 한글만 남기기) 
    data = re.sub(r"[^a-zA-Z0-9가-힣.]", " ", str(data))
    
    return data.strip()

# --------------- 감성점수 계산하기 ------------------------
def sentiment_scoring(news_content):
    """Run a sentiment analysis request on text within a passed filename."""
    client = language_v1.LanguageServiceClient.from_service_account_json("C:/Users/young/Desktop/StockHelper/flowing-bazaar-334005-93614458e39e.json")

    document = language_v1.Document(
        content=news_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    
    annotations = client.analyze_sentiment(request={"document": document})

    # Print the results
    score = annotations.document_sentiment.score
    
    return score

#------------ 기사 크롤링 하기 -------------------
# 키워드로 네이버 기사 url 크롤링
def crawling_article(key_word):
    Url = 'https://search.naver.com/search.naver?'

    # 오늘부터 20일 전까지의 기사를 크롤링
    today = datetime.now()
    startday = today - timedelta(days=20)

    params = {
        "where" : 'news',
        "sm": 'tab_pge',
        "query": key_word,  # ★인코딩하지말고 넣어라★
        "sort": '0',
        "photo": '0',
        "field": '0',
        "pd": '3',
        "ds": str(startday.date()).replace('-','.'),  # 오늘부터 20일 전
        "de" : str(today.date()).replace('-','.'),    # 오늘
        "cluster_rank": '10',
        "mynews" : '1',
        "office_type": '0',
        "office_section_code": '0',
        "news_office_checked" : '1032',
        "nso" : r'so:r,p:from20210101to20211130,a:all',
        "start" : '5000'
    }

    # 경향신문, 국민일보, 동아일보, 한겨례, 조선일보
    news_code = ['1032', '1005', '1020', '1028', '1023']

    # 크롤링 할 url 저장
    urls = []
    
    page = 1
        
    for code in news_code:
        params['news_office_checked'] = code
        raw = requests.get(Url, headers={'User-Agent': 'Mozilla/5.0'}, params=params)

        dom = BeautifulSoup(raw.text, "html.parser")

        try:
            a_tags = dom.select('#main_pack > div.api_sc_page_wrap > div > div > a')
            last_page = int(a_tags[-1].text.strip())
        except:
            continue

        for start in range(1, last_page * 10, 10):
            params['start'] = start
            raw = requests.get(Url, headers={'User-Agent': 'Mozilla/5.0'}, params=params)

            dom = BeautifulSoup(raw.text, "html.parser")

            lists = dom.select("#main_pack > section.sc_new.sp_nnews._prs_nws > div > div.group_news > ul > li")

            for l in lists:
                urls.append(l.select("div.news_wrap > div.news_area > div.news_info > div.info_group > a")[-1]['href'])

    # 크롤링한 날짜, 제목, 본문 저장
    news = []

    tot_sum = 0 
    for url in urls:
        raw = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

        dom = BeautifulSoup(raw.text, "html.parser")

        try:
            title = dom.select_one('#articleTitle').text.strip()
            date = dom.select_one('#main_content > div.article_header > div.article_info > div > span.t11').text.strip()[:10]
        except Exception:
            continue
        
        # <script> <style> 제거 (전처리)
        for s in dom(['script', 'style', 'img']):
            s.decompose()

        # 뉴스본문 리턴
        news_content = dom.find('div', attrs = {'id': 'articleBodyContents'})
        # 뉴스본문에 대한 전처리
        # 각 line 별로 strip(), 태그 제거
        lines = [
            line.strip()
            for line in news_content.get_text().splitlines()
        ]
        news_content = ''.join(lines)

        date = datetime.strptime(date, '%Y.%m.%d')
        if date.weekday() == 5:
            before_one_day = date - timedelta(days=1)
            date = str(before_one_day)[:10].replace('-','.')
        elif date.weekday() == 6:
            before_two_day = date - timedelta(days=2)
            date = str(before_two_day)[:10].replace('-','.')

        # 기사 정제하기
        news_content = data_refine(news_content)

        # 감성점수 계산하기
        senti_score = sentiment_scoring(news_content)

        dic = {
            'Date' : date,
            'title' : title,
            'content' : news_content,
            'Senti_Score' : senti_score
        }
        news.append(dic)

    return pd.DataFrame(news)


# 주식 종목 이름,코드 넘겨주기
def predict_stock(stock_name, stock_code):
    # 검색 키워드 받아오기
    dict = {'NAVER':'네이버', 'POSCO':'포스코'}
    if stock_name in dict.keys():
        stock_name = dict[stock_name]

    start = time.time()  # 시작 시간 저장
    # 검색 키워드로 네이버 기사 크롤링
    df_news = crawling_article(stock_name)
    print(df_news)


    # 기사 감성점수 계산하기
    


    # 기사 데이터셋 구축하기 (KOSPI(init에서 가져오기), 감성점수, 기본 데이터 합치기)


    # 데이터셋 모델에 넣기

    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간

predict_stock('POSCO', '000000')