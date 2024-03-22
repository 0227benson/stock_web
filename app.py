from flask import Flask, render_template, request
import matplotlib
from goodinfo import goodinfo
from K_line import k_line
from stock_EPS import EPS
from PTT import crawler
from cloud import cloud_img
from discu_num import discu_num
matplotlib.use('Agg')  # 使用 Agg 后端
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('html/web.html')

@app.route("/upload", methods=["POST"])
def uploaded_file():
    stock_code = request.form.get('stockCode')
    financial_dict, display_info = goodinfo(stock_code)
    k_line_html = k_line(financial_dict)
    eps_img = EPS(financial_dict)
    title_lst,name,date_lst= crawler(financial_dict)
    wordcloud_obj = cloud_img(financial_dict, title_lst)
    discu_number = discu_num(date_lst,name)

        

    return render_template('html/web_result.html', display_info=display_info ,k_line_html=k_line_html, result=financial_dict ,eps_img=eps_img ,wordcloud_obj=wordcloud_obj ,discu_number=discu_number)

if __name__ == '__main__':
    app.secret_key = "\xa0\r\xed;\xadQ\xe9 \xd2[k\xdcK\x89\x1f\xba"
    app.run(host='0.0.0.0', port=8889, debug=True)
