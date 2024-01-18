import requests
from bs4 import BeautifulSoup

#爬goodinfo，找出股票代號、名稱、資本額(股本)、股價(k線圖)(6個月)、EPS(兩季)

stock = input()
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
soup_kbar = BeautifulSoup(r_kbar.text , 'html.parser')
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

all_country_info = soup_stock.select('td[class="bg_h1"] nobr')
for group in all_country_info:
    if '產業別' in group :
        industry = group.text
    if '資本額' in group :
        capital = group.text

all_country_info_content = soup_stock.select('td[bgcolor="white"]')
country_industry = all_country_info_content[1].text
country_capital = all_country_info_content[4].text
financial_dict['industry'] = country_industry
financial_dict['capital'] = country_capital


#找到10季eps
all_season = soup_eps.select('table[id="tblFinDetail"] th nobr')
all_season_text = [nobr.text for nobr in all_season[1:]] #將all_season轉換成文字
# all_season_text[1:] #分別為哪10季eps
all_season_title = soup_eps.select('td[title="滑鼠在此點一下, 可顯示公式說明"] nobr')
# all_season_eps[6] #eps_title:每股稅後盈餘
all_season_eps = soup_eps.select('table[id="tblFinDetail"] td nobr')[67:77]
all_season_float = [float(nobr.text) for nobr in all_season_eps]  #將all_season_eps轉換成浮點數
after_tax_eps = [{i:j} for i,j in zip(all_season_text, all_season_float)] #將這10季的每一季EPS資料轉成字典儲存
financial_dict['10season_eps'] ={key:value for item in after_tax_eps for key, value in item.items()}

#找到6個月內，每日的開高低收價格，以利製作K線
date_sixmonth = soup_kbar.find('table', {'id' : "tblPriceDetail"})
financial_dict['sixmonth_kbar'] = {}

for row in date_sixmonth.find_all('tr'):
    cells = row.find_all('td')
    # print(cells)
    if len(cells) >= 5:
        if '/' in cells[0].text.strip():
            row_data = [cell.text.strip() for cell in cells[:5]]
            # print(row_data[1:5])
            financial_dict['sixmonth_kbar'][row_data[0]] = row_data[1:]

financial_dict