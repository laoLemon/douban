import csv
from snownlp import SnowNLP

# 打开CSV文件并读取影评内容，并写入新的CSV文件
filename = "2024热辣滚烫.csv"
with open(f'../csv/clean/{filename}', 'r', encoding='ANSI') as file, open(f'../csv/NLP/{filename}', 'w',
                                                                         newline='',
                                                                         encoding='ANSI') as output_file:
    csv_reader = csv.reader(file)
    csv_writer = csv.writer(output_file)

    # 写入表头
    #csv_writer.writerow(['用户名', '影评分数', '影评内容', '日期', '情感得分', '差异'])

    # 初始化统计信息
    total_reviews = 0
    data = []

    # 遍历每一行影评内容，并进行情感分析
    for row in csv_reader:
        name = row[0]
        score = float(row[1])  # 将评分转换为浮点数
        review = row[2]
        date = row[3]

        # 使用SnowNLP进行情感分析
        s = SnowNLP(review)
        # 情感得分越接近1表示积极，越接近0表示消极，将情感得分映射到1-5的范围
        sentiment_score = s.sentiments * 4 + 1

        # 计算情感得分和评分之间的差异
        difference = abs(sentiment_score - score)

        # 添加数据到列表中
        data.append([name, score, review, date, sentiment_score, difference])

        # 更新统计信息
        total_reviews += 1

    # 将数据按照差异值从小到大排序
    sorted_data = sorted(data, key=lambda x: x[5])

    # 将排序后的数据写入CSV文件中
    csv_writer.writerows(sorted_data)

    # 打印总影评数
    print("总影评数:", total_reviews)
