import jieba #切詞工具
from wordcloud import WordCloud #詞雲圖產生器
import os #確認電腦內有沒有安裝繁中詞庫
import requests
import matplotlib
from matplotlib.font_manager import fontManager
import io
import base64
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False
ifont = "msjh.ttc"

def cloud_img(financial_dict,title_lst):
    # 指定要檢查的檔案名稱
    target_file_name = 'dict.txt.big'
    # 獲取當前工作目錄中的檔案列表
    files_in_directory = os.listdir()
    # 檢查是否存在目標檔案
    if target_file_name not in files_in_directory:
        #繁中詞庫請去 https://github.com/fxsjy/jieba 找到 https://github.com/fxsjy/jieba/raw/master/extra_dict/dict.txt.big 下載存到工作目錄中
        url = 'https://github.com/fxsjy/jieba/raw/master/extra_dict/dict.txt.big'
        r = requests.get(url)
        with open('dict.txt.big', 'wb') as f:
            f.write(r.content)


    #設定繁體中文詞庫及把股票名加入建議詞庫
    jieba.set_dictionary("dict.txt.big") #將詞庫替換為繁中字庫
    jieba.suggest_freq(financial_dict['stock_name'], True) #把股票名加入建議詞庫

    #將之前抓到的title_lst導入jieba切詞
    if title_lst == []:
        print("PTT近半年無相關討論")
    else:
        cut = jieba.cut("".join(title_lst), cut_all=False)
        cut = " ".join(cut)

        print("共有",len(title_lst),"則討論",sep="") #顯示總討論的文章數

        s = ["的","是","了","個","Re","嗎","分享","你","會","啦","很",financial_dict['stock_name']]
        #生產詞雲圖，字體設定為標楷體正常
        #stopwords：可以把要去掉不要顯示的字存入一個list然後再指定給stopwords這個參數
        #font_path是顯示的字體，儲存字體路徑請見 C:\Windows\Fonts，請去該資料夾中找到想要的字體把名稱跟副檔名指定過來
        wordcloud = WordCloud(max_font_size=160,font_path = ifont ,stopwords=s,collocations=False,background_color='white',width=600,height=400).generate(cut)
            # 將圖片轉換成 base64 格式
        image_stream = io.BytesIO()
        wordcloud.to_image().save(image_stream, format='PNG')
        image_stream.seek(0)
        image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

        return image_base64