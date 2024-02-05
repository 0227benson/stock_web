import requests
from bs4 import BeautifulSoup

def fetch_stock_price(stock_code):
    url = f"https://tw.stock.yahoo.com/q/q?s={stock_code}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        stock_price = soup.find('b').text
        return stock_price
    else:
        print("Error fetching stock price.")
        return None
