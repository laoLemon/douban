import jieba
from sklearn.metrics import classification_report, accuracy_score
import config  # -*- coding: gbk -*-
import features

classes = features.classes
reviews = config.reviews

df = config.df
# 定义影评分类函数
def classify_review(review):
    # 统计每个特征类别中出现的特征词数量
    class_counts = {feature_class: 0 for feature_class in classes.keys()}

    # 遍历影评中的每个词，并检查其是否在特征词表中出现，然后计算特征词的出现次数
    words = jieba.lcut(review)
    for word in words:
        for feature_class, feature_words in classes.items():
            if word in feature_words:
                class_counts[feature_class] += 1

    # 找到数量最多的特征类别作为影评分类
    max_class = max(class_counts, key=class_counts.get)

    return max_class

# 实际评分与分类的对比统计
actual_ratings = []
classified_ratings = []

# 遍历影评并进行分类
for i, review in enumerate(reviews):
    classification = classify_review(review)
    actual_rating = df.iloc[i, 1]  # 获取实际评分
    actual_ratings.append(actual_rating)
    classified_ratings.append(classification)

# 计算准确率和生成分类报告
accuracy = accuracy_score(actual_ratings, classified_ratings)
report = classification_report(actual_ratings, classified_ratings)

# 输出准确率和分类报告
print("Accuracy:", accuracy)
print("\nClassification Report:")
print(report)
