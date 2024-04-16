from collections import Counter
import re
import pandas as pd
import jieba

stopwords = ['什么','电影','出来','没有','一部','镜头','观众','为了','如果','怎么','可能','演技','最后','这样','就是','喜剧','这种','开始','应该','知道','逻辑','尴尬','剧情','为什么','台词','可以']

def analyze_reviews(csv_file_path, stopwords=stopwords, threshold=100):
    # 读取CSV文件
    df = pd.read_csv(csv_file_path, encoding='ANSI', header=None)
    # 提取第3列数据
    reviews = df.iloc[:, 2]

    # 加入标点符号和数字到停用词表
    stopwords.extend([str(i) for i in range(10)])

    # 定义影评特征词表
    features = []

    # 分词，并统计词频
    words_counter = Counter()
    for review in reviews:
        words = jieba.lcut(review)
        words = [word for word in words if word not in stopwords and not word.isdigit()]
        words = [re.sub(r'[^\w\s]', '', word) for word in words]  # 去除标点符号
        words = [word for word in words if word]  # 去除空字符串
        words_counter.update(words)

    # 从词频中筛选出频繁出现的词语作为特征词
    for word, count in words_counter.items():
        if count >= threshold and len(word) > 1:
            # 词语符合阈值，添加到特征词表中
            features.append(word)

    # 定义维度字典，将评分划分为五个维度
    dimensions = {1: Counter(), 2: Counter(), 3: Counter(), 4: Counter(), 5: Counter()}

    # 统计每个维度下的特征词出现次数和频率
    for i, review in enumerate(reviews):
        words = jieba.lcut(review)
        words = [word for word in words if word not in stopwords and not word.isdigit()]
        words = [re.sub(r'[^\w\s]', '', word) for word in words]  # 去除标点符号
        words = [word for word in words if word]  # 去除空字符串
        # 统计特征词出现次数
        count = Counter(words)
        # 判断评分并将特征词添加到相应维度中
        rating = df.iloc[i, 1]  # 评分在第1列
        try:
            dimensions[rating].update({word: freq for word, freq in count.items() if word in features})
        except KeyError:
            print(f"出现了未知的评分值 '{rating}'，已忽略该条影评。")

    # 定义一个字典，用于存储特征词对应的最多出现的评分
    word_ratings = {}

    # 对于每个特征词，找到它在各评分中的出现次数最多的评分
    for word in features:
        max_rating = 0
        max_count = 0
        for rating, word_counter in dimensions.items():
            if word_counter[word] > max_count:
                max_rating = rating
                max_count = word_counter[word]
        word_ratings[word] = max_rating

    # 将特征词按照其最多出现的评分进行分类
    classes = {}
    for word, rating in word_ratings.items():
        if rating not in classes:
            classes[rating] = [word]
        else:
            classes[rating].append(word)

    # 计算每个特征词在所有影评中的总出现次数
    total_word_counts = {word: sum(word_counter[word] for word_counter in dimensions.values()) for word in features}

    # 输出每个类别中的特征词及其出现次数与总次数之比（按比例从高到低排序）
    for rating, class_words in classes.items():
        print(f"类{rating}:")
        class_word_ratios = []
        for word in class_words:
            count_in_class = dimensions[rating].get(word, 0)
            total_count = total_word_counts[word]
            ratio = count_in_class / total_count
            class_word_ratios.append((word, ratio))
        class_word_ratios.sort(key=lambda x: x[1], reverse=True)
        for word, ratio in class_word_ratios:
            count_in_class = dimensions[rating].get(word, 0)
            total_count = total_word_counts[word]
            print(f"{word}: {count_in_class}/{total_count} ({ratio:.2f})")
        print()

    # 输出每个类别中的特征词表
    for rating, class_words in classes.items():
        print(f"特征类{rating}：")
        print(", ".join(class_words))

    return classes


def find_high_freq_words_by_rating(csv_file_path, target_rating, stopwords=[], threshold=100):
    # 读取CSV文件
    df = pd.read_csv(csv_file_path, encoding='ANSI', header=None)

    # 提取目标评分的评论和总的评论
    target_reviews = df[df[1] == target_rating][2]
    all_reviews = df[2]

    # 加入标点符号和数字到停用词表
    stopwords.extend([str(i) for i in range(10)])

    # 统计目标评分的评论中词语的出现次数
    target_word_counts = Counter()
    for review in target_reviews:
        words = jieba.lcut(review)
        words = [word for word in words if word not in stopwords and not word.isdigit()]
        words = [re.sub(r'[^\w\s]', '', word) for word in words]  # 去除标点符号
        words = [word for word in words if word]  # 去除空字符串
        target_word_counts.update(words)

    # 统计总的评论中词语的出现次数
    all_word_counts = Counter()
    for review in all_reviews:
        words = jieba.lcut(review)
        words = [word for word in words if word not in stopwords and not word.isdigit()]
        words = [re.sub(r'[^\w\s]', '', word) for word in words]  # 去除标点符号
        words = [word for word in words if word]  # 去除空字符串
        all_word_counts.update(words)

    # 计算每个词语在目标评分的评论和总的评论中出现次数之比
    word_ratios = {}
    for word, count in target_word_counts.items():
        total_count = all_word_counts[word]
        ratio = count / total_count
        word_ratios[word] = ratio

    # 按照词语出现次数之比进行排序
    high_freq_words = [word for word, _ in sorted(word_ratios.items(), key=lambda x: x[1], reverse=True) if target_word_counts[word] >= threshold and len(word)>1]

    return high_freq_words


# 示例
classes = analyze_reviews("./csv/merged_file.csv", stopwords=stopwords)
# 添加高频词到特征类1中
classes[1].extend(['垃圾', '玩意', '恶心', '难看', '烂片', '侮辱', '浪费', '营销', '油腻'])
classes[2].extend(['low', '法庭', '两星', '探案', '猥琐', '植入', '妻夫', '莫名其妙', '低俗', '广告', '失望', '密室', '雅美', '侦探', '系列', '油腻', '长泽', '浪费'])
classes[3].extend(['相对', '及格', '之外', '勉强', '不少', '前半段', '特色', '是否', '35', '影子'])
classes[4].extend(['钢七连', '年代', '解决', '记忆', '先辈', '祖国', '总体', '优点', '超越', '千里', '惨烈', '四星', '致敬', '生命', '预期', '杜乐莹', '家庭'])
classes[5].extend(['勇气', '五星', '低分', '苹果', '心情', '女孩', '女人', '梦想', '牛蛙', '不再', '眼泪', '乐莹', '满分', '评论', '万岁', '支持', '找到', '朋友', '破防', '强大', '标准', '震撼', '样子'])
target_rating = 4
threshold = 10
high_freq_words = find_high_freq_words_by_rating("./csv/merged_file.csv", target_rating, stopwords=[""], threshold=threshold)
print("High-frequency words for rating", target_rating, ":", high_freq_words)
