# -- coding:utf-8 --
import csv
from snownlp import SnowNLP

# 打开CSV文件并读取影评内容，并写入新的CSV文件
with open('../csv/merged_file.csv', 'r', encoding='ANSI') as file, open('../csv/sentiment_analysis_results.csv', 'w',
                                                                         newline='',
                                                                         encoding='ANSI') as output_file:
    csv_reader = csv.reader(file)
    csv_writer = csv.writer(output_file)

    # 写入表头
    csv_writer.writerow(['影评内容', '情感得分', '影评分数', '差异'])

    # 初始化统计信息
    total_reviews = 0

    # 遍历每一行影评内容，并进行情感分析
    for row in csv_reader:
        review = row[2]
        score = float(row[1])  # 将评分转换为浮点数
        # 使用SnowNLP进行情感分析
        s = SnowNLP(review)
        # 情感得分越接近1表示积极，越接近0表示消极，将情感得分映射到1-5的范围
        sentiment_score = s.sentiments * 4 + 1

        # 计算情感得分和评分之间的差异
        difference = abs(sentiment_score - score)

        # 写入结果到CSV文件中
        csv_writer.writerow([review, sentiment_score, score, difference])

        # 更新统计信息
        total_reviews += 1

    # 打印总影评数
    print("总影评数:", total_reviews)
