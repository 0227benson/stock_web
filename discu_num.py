import matplotlib.dates as mdates
from collections import Counter
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
from io import BytesIO
import base64
def discu_num(date_lst,name):
    current_date = datetime.now()
    dates = []
    for x in date_lst:
        x = x.strip().zfill(5)
        #先把年份帶今年轉成日期資料
        date_obj = datetime.strptime(f'{current_date.year}/{x}', '%Y/%m/%d')
        if date_obj > current_date:
                date_obj = date_obj.replace(year=current_date.year - 1)
        dates.append(date_obj)



    # 計算日期範圍
    start_date = datetime.now() - timedelta(days=180)
    end_date = datetime.now()

    # 將日期資料轉換成按週跟月，並且計數
    month_numbers = [(date.isocalendar()[0], date.month) for date in dates]
    months = Counter(month_numbers)

    # 創建一個空串列來儲存年份和週數組合
    all_months = []
    # 從今天往前遍歷到180天前的每一天
    current_date = end_date
    while current_date >= start_date:
        # 使用 isocalendar 獲取年份和週數和取得月份
        year, week, _ = current_date.isocalendar()
        m = current_date.month
        # 將組合添加到串列中，檢查重複

        if (year, m) not in all_months:
            all_months.append((year, m))

        # 向前遍歷一天
        current_date -= timedelta(days=1)

    #把每月計數依照時間週期組合填入串列
    month_counts = [months[month] for month in all_months]
    month_counts = month_counts[::-1]
    all_months = all_months[::-1]

    # 直方圖 - 月
    #plt.figure(figsize=(10, 6))
    plt.bar(range(len(all_months)), month_counts, color='blue', tick_label=[f'{m[0]}-{m[1]}' for m in all_months])
    for i in range(len(all_months)):
        plt.text(i,month_counts[i],str(month_counts[i]),fontsize=10, verticalalignment='bottom',horizontalalignment='center')
    plt.xlabel('年-月')
    plt.xticks(rotation=45)
    plt.ylabel('幾篇')
    plt.title(f'每月有幾篇討論{name}的文章')
    #plt.show()
    # 將 Matplotlib 圖表轉換為圖像
    discu = BytesIO()
    plt.savefig(discu, format='png')
    discu.seek(0)
    plt.close()
    # 將圖像轉換為 Base64 字串
    discu = "data:image/png;base64," + base64.b64encode(discu.read()).decode()
    return discu