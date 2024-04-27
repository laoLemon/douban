# Random_forest_plt.py
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def random_forest_classifier(csv_file_path, threshold):
    # 读取数据集
    df = pd.read_csv(csv_file_path, encoding='ANSI', header=None)

    # 仅选择第六列小于阈值的数据
    df = df[df.iloc[:, 5] < threshold]

    # 分割数据集为训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(df.iloc[:, 2], df.iloc[:, 1], test_size=0.2, random_state=42)

    # 使用TF-IDF向量化文本数据
    vectorizer = TfidfVectorizer(max_features=1000)  # 使用TF-IDF向量化，选择前1000个特征
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # 训练随机森林分类器
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)  # 使用100棵树的随机森林
    rf_classifier.fit(X_train_tfidf, y_train)

    # 在测试集上评估模型性能
    y_pred = rf_classifier.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    return accuracy, report

threshold_values = [i / 10 for i in range(0, 51)]  # 从0到5的阈值
accuracies = []

for threshold in threshold_values:
    try:
        accuracy, _ = random_forest_classifier("../csv/NLP/merged_file.csv", threshold)
        accuracies.append(accuracy)
    except ValueError:
        # 跳过导致空数据集的阈值
        pass

# 绘制趋势图
plt.figure(figsize=(10, 6))
plt.rcParams['font.family'] = 'SimHei'
plt.plot(threshold_values[:len(accuracies)], accuracies, marker='o')
plt.title('随机森林模型准确率趋势')
plt.xlabel('阈值')
plt.ylabel('准确率')
plt.grid(True)
plt.gca().invert_xaxis()  # 反转 x 轴刻度
# plt.savefig('random_forest_plt.png')
plt.show()

