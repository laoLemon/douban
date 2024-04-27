# -*- coding: utf-8 -*-
# notebook.py

import tkinter as tk
from tkinter import ttk
from main import create_main_interface
from NLP import insert_images
from ana import run_movie_classifier_app

# 创建主窗口
root = tk.Tk()
root.title("Tab Demo")

# 创建选项卡控件
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# 创建选项卡
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)

# 添加选项卡到选项卡控件
notebook.add(tab1, text="电影基本信息")
notebook.add(tab2, text="情感清洗数据")
notebook.add(tab3, text="影评信息分析")

# 在选项卡1中添加 main.py 生成的界面
create_main_interface(tab1)

insert_images(tab2)

# 在选项卡3中添加 ana.py 生成的界面
run_movie_classifier_app(tab3)

# 运行界面
root.mainloop()
