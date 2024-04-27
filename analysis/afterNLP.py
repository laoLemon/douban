import csv
from sklearn.metrics import classification_report

def generate_classification_report(input_file, flag):
    # 初始化真实标签、预测标签和成功结果列表
    true_labels = []
    predicted_labels = []
    success_results = []

    # 打开CSV文件并读取情感分析结果
    with open(input_file, 'r', encoding='ANSI') as result_file:
        csv_reader = csv.reader(result_file)

        # 遍历每一行情感分析结果
        for row in csv_reader:
            sentiment_score = float(row[4])
            score = float(row[1])

            # 判断情感分析结果是否在flag范围内
            if abs(sentiment_score - score) <= flag:
                sentiment_score = score

            # 判断情感分析结果对应的预测标签
            if sentiment_score <= 1.5:
                predicted_label = 1
            elif sentiment_score <= 2.5:
                predicted_label = 2
            elif sentiment_score <= 3.5:
                predicted_label = 3
            elif sentiment_score <= 4.5:
                predicted_label = 4
            else:
                predicted_label = 5

            # 添加真实标签、预测标签和成功结果到列表中
            true_labels.append(score)
            predicted_labels.append(predicted_label)

            # 如果预测成功，则将结果添加到成功结果列表中
            if predicted_label == score:
                success_results.append([sentiment_score, score, row[0]])

    # 将成功结果写入新的CSV文件
    output_file = 'successful_results.csv'
    with open(output_file, 'w', newline='', encoding='ANSI') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(success_results)

    # 计算分类报告
    report = classification_report(true_labels, predicted_labels)

    return report

# 调用函数并打印分类报告
input_file = '../csv/NLP/merged_file.csv'
flag = 1
classification_report = generate_classification_report(input_file, flag)
print("Classification Report:")
print(classification_report)
print("Successfully classified instances have been saved to 'successful_results.csv'.")

