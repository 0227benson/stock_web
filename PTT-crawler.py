import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime,timedelta
from random import random


def crawl_page(page_url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    re = requests.get(page_url, headers=header)
    soup = BeautifulSoup(re.text, 'html.parser')

    # 處理頁面的爬取邏輯
    return soup
def ptt_crawler(financial_dict,stock):
    # 設定爬取的起始日期（半年前的日期）
    start_date = (datetime.now() - timedelta(days=180)).replace(hour=0, minute=0, second=0, microsecond=0)

    # 解析 PTT 目前最新的頁面，提取頁面數字
    #latest_page_url = 'https://www.ptt.cc/bbs/Stock/index.html'
    #latest_page_soup = crawl_page(latest_page_url)
    #latest_page_number = latest_page_soup.select('.btn-group-paging a')[1]['href'].split('/')[-1].split('.')[0]
    #latest_page_number = int(latest_page_number[5:])



    # 根據字典裡的股票代號或股票名稱爬取相對應的討論版標題
    id = financial_dict['stock_id']
    name = financial_dict['stock_name']
    result_lst = [] # 爬取完的日期及標題

    while True:
        # 設定起始頁面數字
        page_number = 1
        first_page_url = f"https://www.ptt.cc/bbs/Stock/search?page={page_number}&q={stock}"
        soup = crawl_page(first_page_url)

        # 處理每一頁的內容，提取需要的資訊
        for i in soup.find_all('div', {'class': 'r-ent'}):
            date = i.find('div', {'class': 'meta'}).find('div', {'class': 'date'}).text
            title = i.find('div', {'class': 'title'}).text.strip()
            dt = date + title
            result_lst.append(dt) #符合條件的標題存進list裡

        # 更新頁面數字，以繼續爬取下一頁
        page_number += 1
        end = date.split('/')
        # 設定爬取頁面的結束條件
        if int(end[0]) == int(start_date.strftime('%m')) and int(end[1]) < int(start_date.strftime('%d')):
            break

        # 避免爬取速度過快
        sleep(random() * 2)

    print(result_lst)