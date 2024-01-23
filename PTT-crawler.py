import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime,timedelta
from random import random
from dateutil.relativedelta import relativedelta
from urllib.parse import quote

def crawl_page_detail(detail_url, session):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    re = session.get(detail_url, headers=header)
    soup = BeautifulSoup(re.text, 'lxml')

    # 處理詳細頁面的爬取邏輯
    return soup
def ptt_crawler(financial_dict,stock):
    # 設定爬取的起始日期（半年前的日期）
    start_date = (datetime.now() - relativedelta(months=6)) # 自動計算半年前的日期(from dateutil.relativedelta import relativedelta)

    # 根據字典裡的股票代號或股票名稱爬取相對應的討論版標題
    id = financial_dict['stock_id']
    name = financial_dict['stock_name']
    date_lst = [] # 爬取完的日期
    title_lst = [] # 爬取完的標題

    # 使用 Session 保持相同的 cookies
    session = requests.Session()

    # 設定起始頁面數字
    page_number = 1
    stock = quote(name, safe='') # 將中文轉換為 URL 可接受的格式(from urllib.parse import quote)
    check = True
    while True:
        first_page_url = f"https://www.ptt.cc/bbs/Stock/search?page={page_number}&q={stock}"
        soup = crawl_page_detail(first_page_url, session)

        # 處理每一頁的內容，提取需要的資訊
        for i in soup.find_all('div', {'class': 'r-ent'}):
            date = i.find('div', {'class': 'meta'}).find('div', {'class': 'date'}).text
            title = i.find('div', {'class': 'title'})

            # 提取標題的超連結
            link = title.find('a')
            detail_url = f"https://www.ptt.cc{link['href']}"

            # 進入詳細頁面爬取更多資訊
            detail_soup = crawl_page_detail(detail_url, session)

            for meta_line in detail_soup.find_all('div', {'class': 'article-metaline'}):
                if '時間' in meta_line.find('span', {'class': 'article-meta-tag'}).text:
                    # 獲取發文的年份
                    post_year = meta_line.find('span', {'class': 'article-meta-value'}).text.split()[-1]
            end = date.split('/')

            # 判斷是否符合條件
            if int(post_year) == start_date.year:
                if int(end[0]) >= start_date.month:
                    date_lst.append(date)
                    title_lst.append(title.text.strip())  # 符合條件的標題存進list裡
            elif int(post_year) == start_date.year+1:
                date_lst.append(date)
                title_lst.append(title.text.strip())
            else:
                check = False
                break
        if check == False:
            break
        # 更新頁面數字，以繼續爬取下一頁
        page_number += 1

        # 避免爬取速度過快
        sleep(random() * 2)

    if not date_lst or not title_lst:
        print('此股票半年內無人討論')
    else:
        print(date_lst,title_lst,sep = '\n')