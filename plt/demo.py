import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import CountVectorizer



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
    return accuracy


def svm_classifier(csv_file_path, threshold):
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

    # 训练SVM分类器
    svm_classifier = SVC(kernel='linear')  # 使用线性核的支持向量机
    svm_classifier.fit(X_train_tfidf, y_train)

    # 在测试集上评估模型性能
    y_pred = svm_classifier.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    return accuracy


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
    return accuracy


threshold_values = [i / 10 for i in range(0, 51)]  # 从0到5的阈值

accuracies_rf = []
accuracies_svm = []
accuracies_nb = []

for threshold in threshold_values:
    try:
        accuracy_rf = random_forest_classifier("../csv/NLP/merged_file.csv", threshold)
        accuracies_rf.append(accuracy_rf)

        accuracy_svm = svm_classifier("../csv/NLP/merged_file.csv", threshold)
        accuracies_svm.append(accuracy_svm)

        accuracy_nb = naive_bayes_classifier("../csv/NLP/merged_file.csv", threshold)
        accuracies_nb.append(accuracy_nb)
    except ValueError:
        # 跳过导致空数据集的阈值
        pass

# 绘制趋势图
plt.figure(figsize=(10, 6))
plt.rcParams['font.family'] = 'SimHei'
plt.plot(threshold_values[:len(accuracies_rf)], accuracies_rf, label='随机森林')
plt.plot(threshold_values[:len(accuracies_svm)], accuracies_svm, label='SVM')
plt.plot(threshold_values[:len(accuracies_nb)], accuracies_nb, label='贝叶斯')
plt.title('模型准确率趋势')
plt.xlabel('阈值')
plt.ylabel('准确率')
plt.grid(True)
plt.legend()
plt.gca().invert_xaxis()  # 反转 x 轴刻度
plt.savefig('model3.png')
plt.show()
