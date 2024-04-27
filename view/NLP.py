import tkinter as tk
from PIL import Image, ImageTk

def insert_images(root):
    # 创建顶部图片框
    top_frame = tk.Frame(root)
    top_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    # 创建底部图片框
    bottom_frames = []
    for i in range(3):
        frame = tk.Frame(root)
        frame.grid(row=1, column=i, padx=10, pady=10)
        bottom_frames.append(frame)

    # 插入图片
    filenames = ["nlp.png", "model3.png", "random_forest_plt.png", "svm_plt.png", "bayes_plt.png"]
    for i, filename in enumerate(filenames):
        image_path = f"../csv/plt/{filename}"  # 修改路径
        image = Image.open(image_path)
        # 调整图片大小为更大的尺寸
        image = image.resize((400, 380), Image.LANCZOS)  # 修改此处
        photo = ImageTk.PhotoImage(image)

        if i < 2:  # 前两张图片放在顶部
            label = tk.Label(top_frame, image=photo)
            label.image = photo
            label.pack(side=tk.LEFT)
        else:  # 其他图片放在底部
            label = tk.Label(bottom_frames[i-2], image=photo)
            label.image = photo
            label.pack()

# 创建主窗口
#root = tk.Tk()
#root.title("Image Viewer")

# 调用插入图片函数
#insert_images(root)

# 运行主事件循环
#root.mainloop()
