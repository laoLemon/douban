import tkinter as tk
from tkinter import ttk
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from 数据分析 import datechart
# 创建主窗口
root = tk.Tk()
root.title("影评数据分析")
root.geometry("800x600")  # 设置窗口大小

# 创建左侧框架
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 创建选择电影的下拉框
movie_list = ["2019流浪地球", "2021唐人街3", "2022长津湖", "2023满江红", "2024热辣滚烫", "总数据"]

selected_movie = tk.StringVar()
selected_movie.set(movie_list[0])  # 默认选中第一个电影

def show_movie_data(event):
    selected = selected_movie.get()
    if selected == "总数据":
        filename = "../csv/merged_file.csv"
        # 创建一张空白图片
        blank_image = Image.new("RGB", (10, 10), "white")
        photo = ImageTk.PhotoImage(blank_image)
        wordcloud_label.configure(image=photo)
        wordcloud_label.image = photo  # 保持图片引用，防止被垃圾回收
    else:
        filename = f"../csv/clean/{selected}.csv"
    with open(filename, "r", encoding="ANSI") as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
        # 清除之前的内容
        for row in treeview.get_children():
            treeview.delete(row)
        # 插入新数据
        for row in data:
            treeview.insert("", tk.END, values=row)

    # 加载词云图片
    if selected != "总数据":
        try:
            image_path = f"../csv/wordcloud/stopwords/{selected}.jpg"
            image = Image.open(image_path)
            image = image.resize((500, 300), Image.LANCZOS)  # 调整图片大小
            photo = ImageTk.PhotoImage(image)
            wordcloud_label.configure(image=photo)
            wordcloud_label.image = photo  # 保持图片引用，防止被垃圾回收
        except FileNotFoundError:
            wordcloud_label.configure(text="找不到词云图片")
    else:
        wordcloud_label.configure(text="")

movie_label = tk.Label(left_frame, text="选择电影:")
movie_label.pack(side=tk.TOP, padx=10, pady=10)
movie_dropdown = ttk.Combobox(left_frame, textvariable=selected_movie, values=movie_list)
movie_dropdown.pack(side=tk.TOP, padx=10, pady=5)
movie_dropdown.bind("<<ComboboxSelected>>", show_movie_data)

# 创建显示CSV文件内容的表格
treeview = ttk.Treeview(left_frame, columns=("column1", "column2", "column3", "column4"), show="headings", height=10)
treeview.heading("column1", text="用户名")
treeview.heading("column2", text="评分")
treeview.heading("column3", text="评论")
treeview.heading("column4", text="评论时间")
treeview.column("column1", width=10)
treeview.column("column2", width=5)
treeview.column("column3", width=500)
treeview.column("column4", width=10)
treeview.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.BOTH, expand=True)

# 添加滚动条
vsb = ttk.Scrollbar(left_frame, orient="vertical", command=treeview.yview)
vsb.pack(side='right', fill='y')
treeview.configure(yscrollcommand=vsb.set)

# 创建右侧框架
right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# 创建显示词云的区域
wordcloud_frame = tk.Frame(right_frame)
wordcloud_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

wordcloud_label = tk.Label(wordcloud_frame)
wordcloud_label.pack(fill=tk.BOTH, expand=True)

# 创建显示评论时间的图表
fig1 = plt.Figure(figsize=(5, 4), dpi=100)
ax1 = fig1.add_subplot(111)
ax1.set_xlabel('时间')
ax1.set_ylabel('评论数量')
ax1.set_title('评论时间变化')
chart1 = FigureCanvasTkAgg(fig1, right_frame)
chart1.get_tk_widget().grid(row=1, column=0, padx=10, pady=5, sticky="nsew")


# 创建显示评分分布的图表
fig2 = plt.Figure(figsize=(5, 4), dpi=100)
ax2 = fig2.add_subplot(111)
ax2.set_xlabel('评分')
ax2.set_ylabel('数量')
ax2.set_title('评分分布')
chart2 = FigureCanvasTkAgg(fig2, right_frame)
chart2.get_tk_widget().grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

# 设置右侧框架的行和列的权重，使其在调整窗口大小时可以等比例伸缩
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_rowconfigure(1, weight=1)
right_frame.grid_rowconfigure(2, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

# 运行界面
root.mainloop()
