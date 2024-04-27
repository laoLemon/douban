# -*- coding: gbk -*-
# classify.py
import pandas as pd
import jieba
from sklearn.metrics import classification_report, accuracy_score
import analysis.features as features # 导入 features 模块
def generate_classification_report(csv_file_path, threshold):
    # 读取 CSV 文件
    df = pd.read_csv(csv_file_path, header=None, encoding='ANSI')

    # 仅选择第六列小于阈值的数据
    df = df[df.iloc[:, 5] < threshold]

    # 定义影评分类函数
    def classify_review(review):
        class_counts = {feature_class: 0 for feature_class in features.classes.keys()}
        words = jieba.lcut(review)
        for word in words:
            for feature_class, feature_words in features.classes.items():
                if word in feature_words:
                    class_counts[feature_class] += 1
        max_class = max(class_counts, key=class_counts.get)
        return max_class

    # 从数据框中提取评论和实际评分
    reviews = df.iloc[:, 2]
    actual_ratings = df.iloc[:, 1]

    # 对每个评论进行分类，并记录实际评分
    classified_ratings = []
    for review in reviews:
        classification = classify_review(review)
        classified_ratings.append(classification)

    # 计算准确率和生成分类报告
    accuracy = accuracy_score(actual_ratings, classified_ratings)
    report = classification_report(actual_ratings, classified_ratings)
    return report


# 输出准确率和分类报告
report = generate_classification_report("../csv/NLP/merged_file.csv", threshold=2)
#print("\nClassification Report:")
#print(report)