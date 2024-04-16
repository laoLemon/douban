# -*- coding: gbk -*-

import pandas as pd

stopwords = ['什么','电影','出来','没有','一部','镜头','观众','为了','如果','怎么','可能','演技','最后','这样','就是','喜剧','这种','开始','应该']

# 读取CSV文件
df = pd.read_csv("./csv/merged_file.csv", encoding='ANSI', header=None)
# 提取第3列数据
reviews = df.iloc[:, 2]