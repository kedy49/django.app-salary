import matplotlib.pyplot as plt
import base64
from io import BytesIO

# グラフを画像データにするための関数（過去の記事でご紹介したもの）
def Output_Graph():
    buffer = BytesIO()
    plt.savefig(buffer, format="png", transparent=True) #transparent=Trueで背景透明化
    buffer.seek(0)
    img = buffer.getvalue()
    graph = base64.b64encode(img)
    graph = graph.decode("utf-8")
    buffer.close()
    return graph


def Plot_PieChart(p,l):
    # 日本語を表示する設定
    plt.rcParams['font.family'] = 'Ms Gothic'
    # 円グラフの色の設定。順番に適用されていき、最後まで到達したら最初に戻って同じ色が適用される。
    c = ['violet',"pink"]
    plt.switch_backend("AGG")
    plt.figure(figsize=(4,4))
    # 円グラフを描画。デフォルトは3時の方向から開始
    # autopoctで比率を表示するようにしている。小数点第一位まで表示するときはautopct='%.1f%%'。
    # counterclock=Falseで時計回りに、startangle=90で12時の方向から開始、radiusで半径を変更(2で2倍？)
    plt.pie(p, autopct='%.1f%%', labels = l, colors = c, counterclock=False, startangle=90, radius=0.8, center=(0, 0))
    plt.title('給与状況', fontsize=15)
    
    graph = Output_Graph()
    return graph