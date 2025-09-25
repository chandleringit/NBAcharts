"""
Filename:    scawler_salary.py
Author:      Shin Yuan Huang
Created:     2025-09-14 
Description: NBA news from https://www.nba.com/
"""
#%% import
import urllib.request as req
import bs4 as bs
import pandas as pd
import time
from datetime import datetime, timezone
import random
import os

from data_ingestion.mysql import upload_data_to_mysql_upsert, nba_news_headline_table
from data_ingestion.nba_common import parse_time_string



#%%

def nba_news_headline(): 

    url_base = 'https://www.nba.com/'

    # 取得網頁內容
    r = req.Request(url_base)
    r.add_header('user-agent',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/1')

    # 開啟網址並讀取html內容
    resp = req.urlopen(r)
    content = resp.read()
    html = bs.BeautifulSoup(content,'html.parser')

    Headline_list = html.find_all('a', {"class": "Anchor_anchor__cSc3P", "data-type": "headline"})

    title, link, label, article_time = [], [], [], []

    for i in Headline_list:

        title_text = i.text.strip()
        url_get = i.get('href')
        if 'https' not in url_get:
            full_url = f"{url_base}{url_get}"
            # print(full_url)

            # 進入full_url取得文章分類
            r = req.Request(full_url)
            r.add_header('user-agent',
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36')
            resp = req.urlopen(r)
            content = resp.read()
            html = bs.BeautifulSoup(content,'html.parser')
            element_label = html.find('h3', class_='ArticleHeader_ahCattext__ukmoa')
            element_time = html.find('time', class_='ArticleHeader_ahDate__J3fwr')
            if element_label:
                label_text = element_label.text.strip()
                time_text = parse_time_string(element_time.text.strip()) if element_time else None

            else:
                label_text = None  # 或給預設值
                time_text = None    

            title.append(title_text)
            link.append(full_url)
            label.append(label_text)
            article_time.append(time_text)

        else:
            full_url = url_get

            title.append(title_text)
            link.append(full_url)
            label.append(None)
            article_time.append(None)

        # print(full_url)



        # time.sleep(random.uniform(3, 5))  # 輕微延遲，避免封鎖

    all_rows = []
    for i in range(len(title)):
        all_rows.append({
            'news_at': datetime.now(timezone.utc).date(),
            'title': title[i],
            'article_time': article_time[i],
            'label': label[i],
            'link': link[i],
            'uploaded_at': datetime.now(timezone.utc)
        })
    df = pd.DataFrame(all_rows)

    dirname = "output"
    if not os.path.exists(dirname):
            os.mkdir(dirname)
    # save
    df.to_csv(f'output/nba_news_headline.csv', index=False, encoding="utf-8-sig")
    # with open('salary.json', 'w', encoding='utf-8') as f:
    #     json.dump(row, f, indent=4, ensure_ascii=False)

    # to mySQL
    # upload_data_to_mysql(table_name = 'nba_players_salary', df=df, mode = 'replace')
    # data = df.to_dict(orient='records') # 將 DataFrame 轉換為字典列表
    upload_data_to_mysql_upsert(nba_news_headline_table, all_rows)

    print(f"nba_news_headline has been uploaded to mysql.")




#%%

nba_news_headline()