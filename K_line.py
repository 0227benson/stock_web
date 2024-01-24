import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly.io as pio


def k_line(financial_dict):
    #設定多重子圖規格
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                   vertical_spacing=0.1, subplot_titles=(f'{financial_dict["stock_id"]} {financial_dict["stock_name"]} 近六個月股價日K線圖', 'Volume'),
                   row_width=[0.2, 0.7], specs=[[{"secondary_y": False}], [{"secondary_y": False}]])

    #給定繪製k線圖所需資訊，繪製k線並將上漲、下跌顏色設定成符合國內常用的漲紅跌綠
    candlesticks = go.Candlestick(
        x=[key for key in reversed(financial_dict['sixmonth_kbar'])],
        open=[financial_dict['sixmonth_kbar'][key][0] for key in reversed(financial_dict['sixmonth_kbar'])],
        high=[financial_dict['sixmonth_kbar'][key][1] for key in reversed(financial_dict['sixmonth_kbar'])],
        low=[financial_dict['sixmonth_kbar'][key][2] for key in reversed(financial_dict['sixmonth_kbar'])],
        close=[financial_dict['sixmonth_kbar'][key][3] for key in reversed(financial_dict['sixmonth_kbar'])],
        increasing=dict(line=dict(color='red'), fillcolor='red'),
        decreasing=dict(line=dict(color='green'), fillcolor='green'))

    #給定繪製成交量圖所需資訊，繪製成交量長條圖
    volume_bars = go.Bar(
        x=[key for key in reversed(financial_dict['sixmonth_kbar'])],
        y=[financial_dict['sixmonth_kbar'][key][4] for key in reversed(financial_dict['sixmonth_kbar'])],
        showlegend=False,
        marker={
            "color": "rgba(128,128,128,0.5)",
        }
    )

    # 將走勢圖添加到第一行
    fig.add_trace(candlesticks, row=1, col=1)
    fig.update_yaxes(title_text="Price $", secondary_y=False, showgrid=True, row=1, col=1)

    # 將Volume圖添加到第二行
    fig.add_trace(volume_bars, row=2, col=1)
    fig.update_yaxes(title_text="Volume $", secondary_y=False, showgrid=False, row=2, col=1)

    # 添加均線
    for period in [5, 10, 20]:
        ma_values = [financial_dict['sixmonth_kbar'][key][3] for key in reversed(financial_dict['sixmonth_kbar'])]
        ma_trace = go.Scatter(x=list(reversed(financial_dict['sixmonth_kbar'].keys())),
                            y=pd.Series(ma_values).rolling(window=period).mean(),
                            mode='lines',
                            name=f'{period}-day MA',
                            line=dict(width=1),
                            connectgaps=True)
        fig.add_trace(ma_trace, row=1, col=1)

    fig.update_layout(
        height=800,
        xaxis={"rangeslider": {"visible": False}}
    )

    #fig.show()
    html_string = pio.to_html(fig, full_html=False)
    return html_string