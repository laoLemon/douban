# -*- coding: utf-8 -*-
# ana.py
import tkinter as tk
from tkinter import ttk
from analysis.Random_forest import random_forest_classifier as random_forest__report_classifier
from analysis.Bayes import naive_bayes_classifier as naive_bayes_classifier_classifier
from analysis.SVM import svm_classifier as svm_classifier_classifier

def run_movie_classifier_app(parent):
    def show_movie_data(selected_movie, random_forest_label, bayes_label, svm_label, slider_value):
        selected = selected_movie.get()
        slider_val = float(slider_value.get())

        # 调用预测方法，并显示结果
        if selected == "总数据":
            random_forest = random_forest__report_classifier("../csv/NLP/merged_file.csv", slider_val)
            report_bayes = naive_bayes_classifier_classifier("../csv/NLP/merged_file.csv", slider_val)
            report_svm = svm_classifier_classifier("../csv/NLP/merged_file.csv", slider_val)
        else:
            filename = f"../csv/NLP/{selected}.csv"
            random_forest = random_forest__report_classifier(filename, slider_val)
            report_bayes = naive_bayes_classifier_classifier(filename, slider_val)
            report_svm = svm_classifier_classifier(filename, slider_val)

        # 在界面上显示预测结果
        random_forest_label.configure(text="Classification Report for classifier.py:\n" + random_forest)
        bayes_label.configure(text="Classification Report for Bayes.py:\n" + report_bayes)
        svm_label.configure(text="Classification Report for SVM.py:\n" + report_svm)
        print("Slider Value:", slider_val)

    def start_analysis():
        show_movie_data(selected_movie, random_forest_label, bayes_label, svm_label, slider_value)

    # 创建主框架
    main_frame = ttk.Frame(parent)
    main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # 创建选择电影的下拉框
    movie_list = ["2019流浪地球", "2021唐人街3", "2022长津湖", "2023满江红", "2024热辣滚烫", "总数据"]

    selected_movie = tk.StringVar()
    selected_movie.set(movie_list[0])  # 默认选中第一个电影

    movie_dropdown = ttk.Combobox(main_frame, textvariable=selected_movie, values=movie_list)
    movie_dropdown.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    # 创建滑块组件
    slider_label = ttk.Label(main_frame, text="Slider:")
    slider_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    slider_value = tk.DoubleVar()
    slider = tk.Scale(main_frame, from_=0, to=5, orient=tk.HORIZONTAL, resolution=0.1, variable=slider_value)
    slider.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

    # 创建按钮
    analyze_button = ttk.Button(main_frame, text="Start Analysis", command=start_analysis)
    analyze_button.grid(row=0, column=3, padx=10, pady=5)

    # 创建用于显示分类结果的框架和标签
    result_frame = ttk.Frame(parent)
    result_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    random_forest_frame = tk.Frame(result_frame, bd=2, relief=tk.GROOVE)
    random_forest_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
    random_forest_label = tk.Label(random_forest_frame, text="", width=50)
    random_forest_label.pack(side=tk.LEFT)

    bayes_frame = tk.Frame(result_frame, bd=2, relief=tk.GROOVE)
    bayes_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
    bayes_label = tk.Label(bayes_frame, text="", width=50)
    bayes_label.pack(side=tk.LEFT)

    svm_frame = tk.Frame(result_frame, bd=2, relief=tk.GROOVE)
    svm_frame.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")
    svm_label = tk.Label(svm_frame, text="", width=50)
    svm_label.pack(side=tk.LEFT)

if __name__ == "__main__":
    root = tk.Tk()
    app = run_movie_classifier_app(root)
    root.mainloop()
