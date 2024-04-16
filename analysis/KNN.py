# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report

# 读取数据集
df = pd.read_csv("../csv/merged_file.csv", encoding='ANSI', header=None)

# 分割数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(df.iloc[:, 2],df.iloc[:, 1], test_size=0.2, random_state=42)

# 使用TF-IDF向量化文本数据
vectorizer = TfidfVectorizer(max_features=1000)  # 使用TF-IDF向量化，选择前1000个特征
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# 训练KNN分类器
knn_classifier = KNeighborsClassifier(n_neighbors=5)  # 使用K=5的KNN分类器
knn_classifier.fit(X_train_tfidf, y_train)

# 在测试集上评估模型性能
y_pred = knn_classifier.predict(X_test_tfidf)
print("Classification Report:")
print(classification_report(y_test, y_pred))
