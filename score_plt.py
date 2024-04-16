# -- coding:utf-8 --
import csv
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from statistics import median, mode

# 打开CSV文件并读取影评内容
reviews = []
with open('./csv/sentiment_analysis_results.csv', 'r', encoding='ANSI') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        review = {
            'review': row['影评内容'],
            'sentiment_score': float(row['情感得分']),
            'score': float(row['影评分数']),
            'difference': float(row['差异'])
        }
        reviews.append(review)

# 初始化统计信息
scores = defaultdict(list)
sentiment_means = {}
sentiment_medians = {}
sentiment_modes = {}

# 对每个评分收集情感得分
for review in reviews:
    score = review['score']
    sentiment_score = review['sentiment_score']
    scores[score].append(sentiment_score)

# 计算每个评分的情感得分的平均值、中位数和众数
for score, sentiment_scores in scores.items():
    sentiment_means[score] = np.mean(sentiment_scores)
    sentiment_medians[score] = median(sentiment_scores)
    sentiment_modes[score] = mode(sentiment_scores)

# 输出统计信息
print("评分分组情况：")
for score, sentiment_scores in scores.items():
    print(f"评分 {score}: 共 {len(sentiment_scores)} 条评论")

print("\n每个评分的情感得分统计信息：")
for score in sorted(sentiment_means.keys()):
    print(f"评分 {score}:")
    print(f"\t平均值: {sentiment_means[score]}")
    print(f"\t中位数: {sentiment_medians[score]}")
    print(f"\t众数: {sentiment_modes[score]}")

# 绘制图表
x = sorted(sentiment_means.keys())  # 对评分进行排序
y_mean = [sentiment_means[score] for score in x]
y_median = [sentiment_medians[score] for score in x]
y_mode = [sentiment_modes[score] for score in x]

plt.figure(figsize=(10, 6))
plt.plot(x, y_mean, label='Mean Sentiment Score', marker='o')
plt.plot(x, y_median, label='Median Sentiment Score', marker='s')
plt.plot(x, y_mode, label='Mode Sentiment Score', marker='^')
plt.xlabel('Rating')
plt.ylabel('Sentiment Score')
plt.title('Relationship between Rating and Sentiment Score')
plt.xticks(np.arange(1, 6, step=1))
plt.legend()
plt.grid(True)
plt.show()
