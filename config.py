# -*- coding: gbk -*-

import pandas as pd

stopwords = ['ʲô','��Ӱ','����','û��','һ��','��ͷ','����','Ϊ��','���','��ô','����','�ݼ�','���','����','����','ϲ��','����','��ʼ','Ӧ��']

# ��ȡCSV�ļ�
df = pd.read_csv("./csv/merged_file.csv", encoding='ANSI', header=None)
# ��ȡ��3������
reviews = df.iloc[:, 2]