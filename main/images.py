import os
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageSequence

# ✅ 设置你要保存的文件夹路径（修改为你自己的）
SAVE_FOLDER = r"C:\Users\xia\Desktop\问题图片输出"

def open_images():
    file_paths = filedialog.askopenfilenames(
        title="选择要拼接的图片",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")]
    )
    images = []
    print("图片拼接顺序：")
    for path in file_paths:
        print(" -", path)
        img = Image.open(path)
        # 如果是 GIF，取第一帧
        if img.format == "GIF":
            img = next(ImageSequence.Iterator(img))
        img = img.convert("RGB")
        images.append(img)
    return images

def stitch_horizontal(images):
    total_width = sum(img.width for img in images)
    max_height = max(img.height for img in images)
    result = Image.new("RGB", (total_width, max_height), color=(255, 255, 255))
    x_offset = 0
    for img in images:
        result.paste(img, (x_offset, 0))
        x_offset += img.width
    return result

def main():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    images = open_images()
    if not images:
        print("没有选择图片，程序退出。")
        return

    result = stitch_horizontal(images)

    # ✅ 自动创建目标文件夹
    os.makedirs(SAVE_FOLDER, exist_ok=True)

    # 让用户输入文件名
    file_name = simpledialog.askstring("输入文件名", "请输入保存的文件名（不含扩展名）", initialvalue="拼接图")
    if not file_name:
        print("未输入文件名，取消保存。")
        return

    save_path = os.path.join(SAVE_FOLDER, file_name + ".jpg")
    result.save(save_path)
    print(f"\n✅ 拼接完成，保存为：{save_path}")

if __name__ == "__main__":
    main()
