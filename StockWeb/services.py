import numpy as np
import pandas as pd
# from proto.primitives import ProtoType
import requests
from bs4 import BeautifulSoup
import re
import os
import time
from datetime import datetime, timedelta
import FinanceDataReader as fdr
import tensorflow as tf 
# from .__init__ import kospi
from google.cloud import language_v1
from sklearn.preprocessing import MinMaxScaler
from urllib import parse

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
    client = language_v1.LanguageServiceClient.from_service_account_json("C:/DevRoot/dataset/flowing-bazaar-334005-93614458e39e.json")

    document = language_v1.Document(
        content=news_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    
    annotations = client.analyze_sentiment(request={"document": document})

    # Print the results
    score = annotations.document_sentiment.score
    
    return score

#------------ 기사 크롤링 하기 -------------------
# 키워드로 네이버 기사 url 크롤링
def crawling_article(key_word, ds, de):
    Url = 'https://search.naver.com/search.naver?'

    params = {
        "where" : 'news',
        "sm": 'tab_pge',
        "query": key_word,  # ★인코딩하지말고 넣어라★
        "sort": '0',
        "photo": '0',
        "field": '0',
        "pd": '3',
        "ds": ds,  # 오늘부터 20일 전
        "de" : de,    # 오늘
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
            
            print(code, '신문사', start, '번째 크롤링') # ★ 확인용
    
    print('url 크롤링 완료') # ★ 확인용

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

        # 결과물 추가
        dic = {
            'Date' : date,
            'title' : title,
            'content' : news_content,
            'Senti_Score' : senti_score
        }
        news.append(dic)
        
        print(tot_sum, '번째 url 본문 크롤링 중') # ★ 확인용
        tot_sum += 1    

    return pd.DataFrame(news)

# --------------- 데이터셋 구축하기(kospi, 감성점수, 기본 정보 합치기) ------------------
def make_dataset(df_news, kospi, stock_code, ds, de):
    # 날짜별 감성점수 평균내기
    df_senti = df_news[['Date','Senti_Score']].groupby('Date').mean()

    # 종목 정보 가져오기
    stock_df = fdr.DataReader(stock_code, ds, de)
    stock_df.rename(columns={'Change':'EachStock'}, inplace=True)
    
    # 정보 합치기
    stock_dataset = pd.merge(stock_df, kospi, on='Date', how='inner')
    stock_dataset = pd.merge(stock_dataset, df_senti, on='Date', how='left')
    stock_dataset = stock_dataset.fillna(0) # 감성점수가 없는 날은 0으로 세팅

    return stock_dataset
    
# --------------- 데이터셋 정규화 -------------------
def scaling(data_set):
    # 데이터 정규화
    scaler = MinMaxScaler()  # 전체를 정규화
    # Senti_Score   Open   High   Low   Close   Volume   EachStock   KOSPI
    scale_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'EachStock', 'KOSPI', 'Senti_Score']
    data_set_scaled = scaler.fit_transform(data_set[scale_cols])
    data_set_scaled = pd.DataFrame(data_set_scaled)
    data_set_scaled.columns = scale_cols
    print(data_set_scaled)

    # 종가 정규화하는 scaler 만들기
    scaler_close = MinMaxScaler()  # close만 정규화  ->  나중에 다시 되돌릴 때 필요
    df_scaled_close = scaler_close.fit_transform(data_set[['Close']])

    return data_set_scaled, scaler_close

# -------------- 주식 이름과 코드 매칭 체크 ---------------------
def check(stock_name, stock_code):
    stockList = pd.read_csv('static/data/stockList_CSV.csv', dtype='str')

    return stockList[stockList['회사명'] == stock_name]['종목코드'].iloc[0] == stock_code

# ------------ 코스피 20일치 가져오기 -----------------
def Kospi():
    today = datetime.now()
    startday = today - timedelta(days=30)
    ds = str(startday.date())
    de = str(today.date())

    # KOSPI 정보 가져오기
    kospi = fdr.DataReader('KS11', ds, de)[['Change']] 
    kospi.rename(columns={'Change' : 'KOSPI'}, inplace=True)

    # 최근 날짜부터 20일치만 가져오기
    kospi = kospi.tail(20)

    # 코스피 값과 시작 날짜, 끝 날짜 리턴
    return kospi, kospi.index[0].date(), kospi.index[-1].date()


# ----------------- ★ 주식 종가 반환해주기 (메인 함수!!!) ★ -------------------
def predict_stock(stock_name, stock_code):
    # 주식 종목 이름 한글로 디코딩
    stock_name = parse.unquote(stock_name)

    # 주식 종목 이름과 코드가 매칭이 되는지 체크
    if check(stock_name, stock_code) == False:
        return None   # 동일하지 않으면 None 이 반환 -> 나중에 views.py 에서 체크해서 alert 설정해주기

    # 코스피, 시작날짜, 끝날짜 받아오기
    kospi, ds_datetime, de_datetime = Kospi()
    print(stock_name, stock_code)
    # 날짜 문자열로 변경
    ds = str(ds_datetime).replace('-','.')
    de = str(de_datetime).replace('-','.')
    print('코스피 완료', ds, de) # ★ 확인용

    # 검색 키워드 받아오기
    dict = {'NAVER':'네이버', 'POSCO':'포스코'}
    if stock_name in dict.keys():
        stock_name = dict[stock_name]

    start = time.time()  # 시작 시간 저장   # ★ 확인용

    # 검색 키워드로 네이버 기사 크롤링
    df_news = crawling_article(stock_name, ds, de)
    print(df_news) # ★ 확인용
    
    # 기사 데이터셋 구축하기 (KOSPI(init에서 가져오기), 감성점수, 기본 데이터 합치기)
    data_set = make_dataset(df_news, kospi, stock_code, ds, de)
    print(data_set) # ★ 확인용
    
    # 스케일링
    data_set_scaled, scaler_close = scaling(data_set)

    # 데이터셋 모델에 넣기
    feature_cols = ['Senti_Score', 'Open', 'High', 'Low', 'Volume', 'EachStock', 'KOSPI']
    model = tf.keras.models.load_model('dataset/Model/StockHelperModel.h5')
    pred = model.predict(np.array(data_set_scaled[feature_cols])[np.newaxis, :])
    print(scaler_close.inverse_transform(pred)) # ★ 확인용
    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간 # ★ 확인용
    
    # 결과
    result =  data_set['Close']
    next_day = de_datetime + timedelta(days=1)
    if datetime.strptime(str(next_day), '%Y-%m-%d').weekday() == 5 or datetime.strptime(str(next_day), '%Y-%m-%d').weekday() == 6:
        next_day + next_day + timedelta(days=(7 - datetime.strptime(str(next_day), '%Y-%m-%d').weekday()))
    result.loc[str(next_day)] = scaler_close.inverse_transform(pred)[0][0]
    print(result) # ★ 확인용

    return result, data_set

# predict_stock('카카오', '000000')

# print(kospi('2021-12-10', '2021-12-13'))