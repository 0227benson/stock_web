import requests
from bs4 import BeautifulSoup
import re
from time import sleep
from collections import OrderedDict


#爬goodinfo，找出股票代號、名稱、資本額(股本)、股價(k線圖)(6個月)、EPS(兩季)
try:

    ##處理股票清單，若使用者輸入股票名稱，先轉成股票代碼餵給程式
    #解析網站
    url_stock_list = 'https://goodinfo.tw/tw/Lib.js/TW_STOCK_ID_NM_LIST.js'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    r_list = requests.get(url_stock_list, headers=header)
    r_list.encoding = 'UTF-8'
    soup_list = BeautifulSoup(r_list.text, 'html.parser')

    #提取JavaScript中的garrTW_LIST_STOCK_ID_NM内容，並將所有股票清單列入字典，以股票名稱為key、代號為value(爬取javascript規格，要用正規表達式)
    javascript_content = str(soup_list)
    matches = re.findall(r"var garrTW_LIST_STOCK_ID_NM = \['(.*?)'\];", javascript_content, re.DOTALL)

    #如果有匹配到結果，進行後續處理
    if matches:
        # 將garrTW_LIST_STOCK_ID_NM内容納入字典
        dict_stock_list = {item.split(' ', 1)[1]: item.split(' ', 1)[0] for item in matches[0].split("','")}


    #函式：判斷使用者輸入是否為中文
    def is_chinese_or_digit(char):
        #如果是名稱，return字典value
        if '\u4e00' <= char <= '\u9fff':
            return dict_stock_list[char]

        #如果是代號，return代號
        if '0' <= char <= '9':
            return char

    # 判斷使用者輸入為何
    stock = is_chinese_or_digit(input())

    url_stock = 'https://goodinfo.tw/tw/StockDetail.asp?STOCK_ID=' + stock #股票代號、名稱、資本額(股本)網址
    url_kbar = 'https://goodinfo.tw/tw/ShowK_Chart.asp?STOCK_ID='+ stock + '&PERIOD=180' #六個月K線網址
    url_eps = 'https://goodinfo.tw/tw/StockFinDetail.asp?RPT_CAT=XX_M_QUAR&LAST_RPT_CAT=XX_M_QUAR&STOCK_ID='+ stock + '&QRY_TIME=' #EPS網址(單季)

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    r_stock = requests.get(url_stock,headers= header)
    r_kbar = requests.get(url_kbar, headers=header)
    r_eps = requests.get(url_eps, headers=header)

    #解析以上三個網站
    r_stock.encoding = 'UTF-8'
    r_kbar.encoding = 'UTF-8'
    r_eps.encoding = 'UTF-8'

    soup_stock = BeautifulSoup(r_stock.text , 'html.parser')
    sleep(0.5)
    soup_kbar = BeautifulSoup(r_kbar.text , 'html.parser')
    sleep(0.5)
    soup_eps = BeautifulSoup(r_eps.text , 'html.parser')

    #找標頭:股票代號、名稱
    financial_dict = {}

    link = f'StockDetail.asp?STOCK_ID={stock}'
    all_head_stock = soup_stock.select(f'a[href="{link}"]')

    for element in all_head_stock:
        if element.text[0].isdigit():
            stock_id_name = element.text.split()
    financial_dict['stock_id'] = stock_id_name[0]
    financial_dict['stock_name'] = stock_id_name[1]


    #找產業類別、股本
    all_country_info_content = soup_stock.select('td[bgcolor="white"]')
    country_industry = all_country_info_content[1].text
    country_capital = all_country_info_content[4].text
    country_business = soup_stock.select('td[bgcolor="white"] p')[-1].text

    financial_dict['industry'] = country_industry
    financial_dict['capital'] = country_capital
    financial_dict['major business'] = country_business


    #找到10季eps
    all_season = soup_eps.select('table[id="tblFinDetail"] th nobr')
    all_season_text = [nobr.text for nobr in all_season[1:]] #將all_season轉換成文字
    # all_season_text[1:] #分別為哪10季eps
    all_season_title = soup_eps.select('td[title="滑鼠在此點一下, 可顯示公式說明"] nobr')
    # all_season_eps[6] #eps_title:每股稅後盈餘
    all_season_eps = soup_eps.select('table[id="tblFinDetail"] td nobr')[67:77]
    # all_season_float = [float(nobr.text) for nobr in all_season_eps]  #將all_season_eps轉換成浮點數
    all_season_float =[float(nobr.text) if nobr.text != '-' else 0 for nobr in all_season_eps]
    after_tax_eps = [{i:j} for i,j in zip(all_season_text, all_season_float)] #將這10季的每一季EPS資料轉成字典儲存
    financial_dict['10season_eps'] ={key:value for item in after_tax_eps for key, value in item.items()}

    #找到6個月內，每日的開高低收價格，以利製作K線
    date_sixmonth = soup_kbar.find('table', {'id' : "tblPriceDetail"})
    #將K線資料加入一個有序的字典
    financial_dict['sixmonth_kbar'] = OrderedDict()

    for row in date_sixmonth.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) >= 5:
            if '/' in cells[0].text.strip():
                row_data = [cell.text.strip() for cell in cells[:5]]
                financial_dict['sixmonth_kbar'][row_data[0]] = row_data[1:]
                financial_dict['sixmonth_kbar'][row_data[0]].append(float(cells[8].text.strip().replace(',', '')) if cells[8].text.strip().replace(',', '') else 0)
except :
    try:
        if '您的瀏覽量異常' in soup_stock.text or '您的瀏覽量異常' in soup_kbar.text or '您的瀏覽量異常' in soup_eps.text:
            print('查詢頻率太高，你被bannnnnn了!')
    except:
        print("錯誤：查無此股")