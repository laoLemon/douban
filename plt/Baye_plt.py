# -*- coding: utf-8 -*-
#Bayes_plt.py
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

def naive_bayes_classifier(csv_file_path, threshold):
    # 读取数据，不使用表头
    data = pd.read_csv(csv_file_path, encoding='ANSI', header=None)

    # 仅选择第六列小于阈值的数据
    data = data[data.iloc[:, 5] < threshold]

    # 分割数据集为训练集和测试集
    X = data.iloc[:, 2]  # 第一列作为特征
    y = data.iloc[:, 1]  # 第二列作为目标变量
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 使用词袋模型进行特征提取
    vectorizer = CountVectorizer()
    X_train_counts = vectorizer.fit_transform(X_train)
    X_test_counts = vectorizer.transform(X_test)

    # 构建朴素贝叶斯分类器模型
    clf = MultinomialNB()
    clf.fit(X_train_counts, y_train)

    # 在测试集上进行预测
    y_pred = clf.predict(X_test_counts)

    # 计算准确率
    accuracy = accuracy_score(y_test, y_pred)

    # 评估模型性能
    report = classification_report(y_test, y_pred)
    return accuracy, report

threshold_values = [5 - i / 10 for i in range(0, 51)]  # 从5到0的阈值
accuracies = []

for threshold in threshold_values:
    try:
        accuracy, _ = naive_bayes_classifier('../csv/NLP/merged_file.csv', threshold)
        accuracies.append(accuracy)
    except ValueError:
        # 跳过导致空数据集的阈值
        pass

# 绘制趋势图
plt.figure(figsize=(10, 6))
plt.rcParams['font.family'] = 'SimHei'
plt.plot(threshold_values[:len(accuracies)], accuracies, marker='o')
plt.title('Byes模型准确率趋势')
plt.xlabel('阈值')
plt.ylabel('准确率')
plt.gca().invert_xaxis()  # 反转 x 轴刻度
plt.grid(True)
# plt.savefig('bayes_plt.png')
plt.show()
