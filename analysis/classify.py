# -*- coding: gbk -*-
# classify.py
import pandas as pd
import jieba
from sklearn.metrics import classification_report, accuracy_score
import analysis.features as features # ���� features ģ��
def generate_classification_report(csv_file_path, threshold):
    # ��ȡ CSV �ļ�
    df = pd.read_csv(csv_file_path, header=None, encoding='ANSI')

    # ��ѡ�������С����ֵ������
    df = df[df.iloc[:, 5] < threshold]

    # ����Ӱ�����ຯ��
    def classify_review(review):
        class_counts = {feature_class: 0 for feature_class in features.classes.keys()}
        words = jieba.lcut(review)
        for word in words:
            for feature_class, feature_words in features.classes.items():
                if word in feature_words:
                    class_counts[feature_class] += 1
        max_class = max(class_counts, key=class_counts.get)
        return max_class

    # �����ݿ�����ȡ���ۺ�ʵ������
    reviews = df.iloc[:, 2]
    actual_ratings = df.iloc[:, 1]

    # ��ÿ�����۽��з��࣬����¼ʵ������
    classified_ratings = []
    for review in reviews:
        classification = classify_review(review)
        classified_ratings.append(classification)

    # ����׼ȷ�ʺ����ɷ��౨��
    accuracy = accuracy_score(actual_ratings, classified_ratings)
    report = classification_report(actual_ratings, classified_ratings)
    return report


# ���׼ȷ�ʺͷ��౨��
report = generate_classification_report("../csv/NLP/merged_file.csv", threshold=2)
#print("\nClassification Report:")
#print(report)