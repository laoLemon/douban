# Bayes.py
import pandas as pd
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

    # 评估模型性能
    report = classification_report(y_test, y_pred)
    return report

report = naive_bayes_classifier('../csv/NLP/merged_file.csv', threshold=3.1)
# print("\nClassification Report:")
#print(report)
