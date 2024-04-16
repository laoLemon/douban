from wordcloud import WordCloud
# 读取文本
def csvwc(movie):

    comment_index = 2
    stopwords=[]
    if '2024' in movie:
        stopwords = ["乐", "和", "另", "p", "的", "赢", "不是", "另外", "最后", "唉", "还行", "与", "b", "比",
                         "的人", "热辣滚烫", "所以", "的自己", "一部", "真的"]
    if '2023' in movie:
        stopwords = ["另外", "和", "p", "就", "与", "在", "哦", "大", "嗯", "了", "以及", "还有", "并且", "其实"]
    if '2022' in movie:
        stopwords = ["不过","但是","唉","是","的","和","当然","在","总之","长津湖"]
    if '2021' in movie:
        stopwords = ["但是","哎","的","总之","the","和","唐探3","唐探","算了","当然"]
    if '2019' in movie:
        stopwords = ["流浪地球","但是","了","最后","但","和","里","不","然而","呃","看","哎","咦","而","吧","啊","好的","不是","真的","的好","嗯","对","与"]


    with open(movie, "r", encoding="ANSI", newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        with open('comment.txt', 'a') as f:
            f.truncate(0)
        for row in csvreader:
            comment_content = row[comment_index]
            with open('comment.txt', 'a') as f:
                f.write(comment_content)
        csvfile.close()

    f = open('comment.txt', 'r', encoding='ANSI')
    txt = f.read()
    f.close

    # 词云对象
    wc = WordCloud(font_path='msyh.ttc'
                   ,width = 1000,
                    height = 700,
                   background_color='white',
                   stopwords=stopwords)
    # 生成词云
    wc.generate(txt)
    # 保存词云文件
    wc.to_file('img.jpg')

import matplotlib.pyplot as plt
import csv

from pylab import mpl
# 设置显示中文字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]

def get_quarter(date):
    month = int(date.split("/")[0])
    if 1 <= month <= 3:
        return "第一季度"
    elif 4 <= month <= 6:
        return "第二季度"
    elif 7 <= month <= 9:
        return "第三季度"
    else:
        return "第四季度"

def datechart(movie):
    date_index = 3
    counts = {}

    # 读取csv文件并统计每个日期的影评数量
    with open(movie, "r", encoding="ANSI", newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            comment_content = row[date_index]
            month, day = comment_content.split("月")
            day = day.replace("日", "")
            counts[f"{month}/{day}"] = counts.get(f"{month}/{day}", 0) + 1

    # 将统计结果按日期排序
    items = sorted(counts.items(), key=lambda x: (int(x[0].split('/')[0]), int(x[0].split('/')[1])))

    # 计算每个季度的最大值日期和对应的影评数量
    max_values = {}
    for item in items:
        quarter = get_quarter(item[0])
        if quarter not in max_values or counts[item[0]] > counts[max_values[quarter]]:
            max_values[quarter] = item[0]

    # 构建新的 x 轴刻度和对应的标签
    x_ticks = []
    x_labels = []
    for quarter in sorted(max_values.keys()):
        x_ticks.append(max_values[quarter])
        x_labels.append(f"{quarter}\n{max_values[quarter]}")

    # 绘制折线图
    plt.plot([item[0] for item in items], [item[1] for item in items], 'b*--', alpha=0.5, linewidth=1, label='acc')

    # 在每个季度的最大值日期处标记出日期
    for i in range(len(x_ticks)):
        plt.text(x_ticks[i], counts[x_ticks[i]], x_ticks[i], ha='center', va='bottom')

    plt.legend()  # 显示图例
    plt.xlabel('日期')  # 设置 x 轴标签
    plt.ylabel('影评数量')  # 设置 y 轴标签
    plt.title('影评数量随时间变化图')  # 设置标题
    plt.xticks(x_ticks, x_labels, rotation=45)  # 设置 x 轴刻度并旋转标签
    plt.tight_layout()  # 调整布局，避免标签重叠

    plt.show()  # 显示图表
    return plt



if __name__ == '__main__':
    movie2024 = "2024热辣滚烫.csv"
    movie2023 = "2023满江红.csv"
    movie2022 = "2022长津湖.csv"
    movie2021 = "2021唐人街3.csv"
    movie2019 = "2019流浪地球.csv"
    #csvwc('./csv/clean/' + movie2023)
    datechart('./csv/clean/'+movie2024)

