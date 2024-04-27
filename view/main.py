# main.py
import tkinter as tk
from tkinter import ttk
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from 数据分析 import datechart, plot_bar_chart_from_csv

def create_main_interface(parent):
    def on_closing():
        parent.destroy()

    # 创建左侧框架
    left_frame = tk.Frame(parent)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # 创建选择电影的下拉框
    movie_list = ["2019流浪地球", "2021唐人街3", "2022长津湖", "2023满江红", "2024热辣滚烫", "总数据"]

    selected_movie = tk.StringVar()
    selected_movie.set(movie_list[0])  # 默认选中第一个电影

    def show_movie_data(event):
        # 清空之前的折线图和树状图
        for widget in line_chart_frame.winfo_children():
            widget.destroy()
        for widget in pie_chart_frame.winfo_children():
            widget.destroy()
        selected = selected_movie.get()
        if selected == "总数据":
            filename = "../csv/merged_file.csv"
            try:
                image_path = "../csv/wordcloud/merged_wordcloud.jpg"
                image = Image.open(image_path)
                image = image.resize((300, 200), Image.LANCZOS)  # 调整图片大小
                photo = ImageTk.PhotoImage(image)
                wordcloud_label.configure(image=photo)
                wordcloud_label.image = photo  # 保持图片引用，防止被垃圾回收
            except FileNotFoundError:
                wordcloud_label.configure(text="找不到词云图片")
        else:
            filename = f"../csv/clean/{selected}.csv"
            try:
                image_path = f"../csv/wordcloud/stopwords/{selected}.jpg"
                image = Image.open(image_path)
                image = image.resize((300, 200), Image.LANCZOS)  # 调整图片大小
                photo = ImageTk.PhotoImage(image)
                wordcloud_label.configure(image=photo)
                wordcloud_label.image = photo  # 保持图片引用，防止被垃圾回收
            except FileNotFoundError:
                wordcloud_label.configure(text="找不到词云图片")

        # 更新表格数据
        with open(filename, "r", encoding="ANSI") as file:
            csv_reader = csv.reader(file)
            data = list(csv_reader)
            for row in treeview.get_children():
                treeview.delete(row)
            for row in data:
                treeview.insert("", tk.END, values=row)

        bar_chart = plot_bar_chart_from_csv(filename)

        # 创建并更新评论时间的折线图
        fig = plt.figure(figsize=(3, 2))
        plt.clf()  # 清除当前的图形
        datechart(filename)
        plt.title('评论时间分布')
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=line_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 创建并更新评分的树状图
        fig_bar = plt.figure(figsize=(4, 3))
        plt.clf()  # 清除当前的图形
        ax = fig_bar.add_subplot(111)  # 创建子图对象
        plot_bar_chart_from_csv(filename, ax=ax)
        plt.title('评分分布')
        plt.tight_layout()
        canvas_bar = FigureCanvasTkAgg(fig_bar, master=pie_chart_frame)
        canvas_bar.draw()
        canvas_bar.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    movie_label = tk.Label(left_frame, text="选择电影:")
    movie_label.pack(side=tk.TOP, padx=10, pady=10)
    movie_dropdown = ttk.Combobox(left_frame, textvariable=selected_movie, values=movie_list)
    movie_dropdown.pack(side=tk.TOP, padx=10, pady=5)
    movie_dropdown.bind("<<ComboboxSelected>>", show_movie_data)

    # 创建显示CSV文件内容的表格
    treeview = ttk.Treeview(left_frame, columns=("column1", "column2", "column3", "column4"), show="headings",
                            height=10)
    treeview.heading("column1", text="用户名")
    treeview.heading("column2", text="评分")
    treeview.heading("column3", text="评论")
    treeview.heading("column4", text="评论时间")
    treeview.column("column1", width=10)
    treeview.column("column2", width=5)
    treeview.column("column3", width=500)
    treeview.column("column4", width=10)
    treeview.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.BOTH, expand=True)  # 使用pack布局管理器

    # 添加滚动条
    vsb = ttk.Scrollbar(left_frame, orient="vertical", command=treeview.yview)
    vsb.pack(side='right', fill='y')  # 使用pack布局管理器
    treeview.configure(yscrollcommand=vsb.set)

    # 创建右侧框架
    right_frame = tk.Frame(parent)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # 创建显示词云的区域
    wordcloud_frame = tk.Frame(right_frame)
    wordcloud_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
    wordcloud_label = tk.Label(wordcloud_frame)
    wordcloud_label.pack(fill=tk.BOTH, expand=True)

    # 创建显示折线图的区域
    line_chart_frame = tk.Frame(right_frame)
    line_chart_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

    # 创建显示树状图的区域
    pie_chart_frame = tk.Frame(right_frame)
    pie_chart_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

    # 设置右侧框架的行和列的权重，使其在调整窗口大小时可以等比例伸缩
    right_frame.grid_rowconfigure(0, weight=1)
    right_frame.grid_rowconfigure(1, weight=1)
    right_frame.grid_rowconfigure(2, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)



if __name__ == "__main__":
    root = tk.Tk()
    app = create_main_interface(root)
    root.mainloop()