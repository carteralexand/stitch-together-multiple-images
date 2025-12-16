import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageSequence

def get_shop_name(filename):
    """
    从文件名中提取店铺名称（分割_后的前缀）
    示例：xxx_1.jpg -> xxx | shop001_2.png -> shop001
    """
    # 匹配 xxx_数字.后缀 的格式，提取xxx部分
    match = re.match(r'^(.+?)_\d+\.\w+$', filename)
    if match:
        return match.group(1)
    return None

def load_images_from_folder(folder_path):
    """
    从指定文件夹加载所有图片，并按店铺名称分组
    返回：字典 {店铺名: [图片路径列表]}
    """
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
    shop_images = {}
    
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 过滤非图片文件
        if not filename.lower().endswith(image_extensions):
            continue
        
        # 提取店铺名称
        shop_name = get_shop_name(filename)
        if not shop_name:
            continue  # 不符合命名规则的文件跳过
        
        # 拼接完整路径
        file_path = os.path.join(folder_path, filename)
        # 添加到对应店铺的列表中
        if shop_name not in shop_images:
            shop_images[shop_name] = []
        shop_images[shop_name].append(file_path)
    
    # 对每个店铺的图片按数字序号排序（确保xxx_1.jpg, xxx_2.jpg...顺序）
    for shop_name in shop_images:
        def extract_number(file_path):
            """提取文件名中的数字部分用于排序"""
            filename = os.path.basename(file_path)
            match = re.search(r'_(\d+)\.', filename)
            return int(match.group(1)) if match else 0
        
        shop_images[shop_name].sort(key=extract_number)
    
    return shop_images

def stitch_horizontal(images):
    """水平拼接图片（保持原逻辑）"""
    if not images:
        return None
    
    # 获取所有图片的总宽度和最大高度
    total_width = sum(img.width for img in images)
    max_height = max(img.height for img in images)
    
    # 创建新画布（白色背景）
    result = Image.new("RGB", (total_width, max_height), color=(255, 255, 255))
    
    # 逐个粘贴图片
    x_offset = 0
    for img in images:
        result.paste(img, (x_offset, 0))
        x_offset += img.width
    
    return result

def process_images(source_folder, save_folder):
    """批量处理图片拼接"""
    # 加载并分组图片
    shop_images = load_images_from_folder(source_folder)
    
    if not shop_images:
        messagebox.showinfo("提示", "未找到符合命名规则的图片（格式应为：店铺名_数字.后缀）")
        return
    
    # 创建保存文件夹
    os.makedirs(save_folder, exist_ok=True)
    
    # 处理每个店铺的图片
    processed_count = 0
    for shop_name, file_paths in shop_images.items():
        try:
            # 加载图片（处理GIF只取第一帧）
            images = []
            for path in file_paths:
                img = Image.open(path)
                if img.format == "GIF":
                    img = next(ImageSequence.Iterator(img))
                img = img.convert("RGB")
                images.append(img)
            
            # 拼接图片
            stitched_img = stitch_horizontal(images)
            if not stitched_img:
                continue
            
            # 保存拼接后的图片
            save_path = os.path.join(save_folder, f"{shop_name}.jpg")
            stitched_img.save(save_path, quality=95)  # 保存为高质量JPG
            processed_count += 1
            
            print(f"✅ 已处理：{shop_name} -> {save_path}")
            
        except Exception as e:
            print(f"❌ 处理失败 {shop_name}：{str(e)}")
            continue
    
    # 处理完成提示
    if processed_count > 0:
        messagebox.showinfo("完成", f"成功拼接 {processed_count} 个店铺的图片！\n保存路径：{save_folder}")
    else:
        messagebox.showwarning("警告", "没有成功拼接任何图片！")

def main():
    """主程序（带GUI选择文件夹）"""
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    root.iconify()   # 最小化窗口（避免任务栏闪烁）
    
    # 选择源文件夹（存放待拼接图片）
    source_folder = filedialog.askdirectory(title="选择待拼接图片的文件夹")
    if not source_folder:
        messagebox.showinfo("提示", "未选择源文件夹，程序退出")
        return
    
    # 选择保存文件夹（输出拼接后的图片）
    save_folder = filedialog.askdirectory(title="选择拼接图片的保存文件夹")
    if not save_folder:
        messagebox.showinfo("提示", "未选择保存文件夹，程序退出")
        return
    
    # 批量处理
    process_images(source_folder, save_folder)

if __name__ == "__main__":
    # 可直接修改这里的默认路径，避免每次都选择文件夹
     SAVE_FOLDER = r"C:\Users\xia\Desktop\罗森清污有关\joint1_clean"
     SOURCE_FOLDER = r"C:\Users\xia\Desktop\罗森清污有关\store1_clean"
     process_images(SOURCE_FOLDER, SAVE_FOLDER)
    
    # 带GUI交互的方式
    # main()