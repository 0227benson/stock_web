import matplotlib.pyplot as plt
import base64
from io import BytesIO


def EPS(financial_dict):
    eps = financial_dict['10season_eps']
    if eps!={}:
        eps_Q=[]
        eps_v=[]
        for item in eps:
            eps_Q.append(item)
            eps_v.append(eps[item])

        fig, ax = plt.subplots()
        ax.bar(eps_Q[::-1], eps_v[::-1])
        ax.set_title(f"{financial_dict['stock_name']}每季EPS")
        ax.set_xticklabels(eps_Q[::-1], rotation=45)
        ax.set_ylabel('EPS')
        for i in reversed(range(len(eps_Q))):
            ax.text(eps_Q[i], eps_v[i], str(eps_v[i]), fontsize=10, verticalalignment='center', horizontalalignment='center')

        # 將 Matplotlib 圖表轉換為圖像
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        # 將圖像轉換為 Base64 字串
        img_str = "data:image/png;base64," + base64.b64encode(img.read()).decode()
        return img_str