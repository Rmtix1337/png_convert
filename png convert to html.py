import os
import sys
import re
import subprocess
from pathlib import Path

def extract_number(filename):
    # 尝试提取数字部分作为排序依据
    match = re.search(r'(\\d+)', filename)
    return int(match.group(0)) if match else float('inf')  # 没有数字的文件排在最后

def extract_letter(filename):
    # 尝试提取字母部分作为排序依据
    match = re.search(r'([a-zA-Z]+)', filename)
    return match.group(0) if match else ''

def custom_sort_key(filename):
    # 提取基本名称（不带扩展名）
    base_name = Path(filename).stem
    # 使用数字和字母共同作为排序依据
    number_part = extract_number(base_name)
    letter_part = extract_letter(base_name)
    return (letter_part, number_part)

def generate_html(image_files, output_path='index.html'):
    # 创建HTML内容
    html_content = '''<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>图片展示</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow-y: scroll; /* 确保页面可以垂直滚动 */
        }
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }
        .image-container {
            margin: 10px 0;
            transition: transform 0.2s;
        }
        .image-container:hover {
            transform: scale(1.02);
        }
        img {
            max-width: 90vw; /* 图片最大宽度为视口的90% */
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        footer {
            text-align: center;
            padding: 20px;
            color: #777;
            background-color: #ffffff;
            border-top: 1px solid #ddd;
            margin-top: 30px;
        }
    </style>
</head>
<body>
    <div class="container">
'''

    # 添加图片元素到HTML
    for image_file in image_files:
        html_content += f'        <div class="image-container"><img src="{os.path.basename(image_file)}" alt="Image"></div>\n'

    # 结束HTML
    html_content += '''    </div>
    <footer>
        <p>PNG convert 2 Gallery</p>
        <p>made by Rmtix1337 | <a href="https://github.com/Rmtix1337" target="_blank">GitHub</a></p>
    </footer>
</body>
</html>'''

    # 写入HTML文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML文件已生成在：{output_path}")

if __name__ == "__main__":
    # 检查是否拖入了文件夹路径
    if len(sys.argv) < 2:
        print("请将文件夹拖放到此程序上")
        # 先设置chcp为utf-8模式再执行pause
        subprocess.run(["cmd.exe", "/c", "chcp 65001 && pause"], shell=True, encoding='utf-8')
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    # 检查文件夹是否存在
    if not os.path.isdir(folder_path):
        print(f"文件夹不存在：{folder_path}")
        sys.exit(1)
    
    # 获取所有图片文件
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) 
                  if f.lower().endswith((('.webp', '.jpg', '.jpeg', '.png')))]
    
    # 如果没有找到图片文件，退出程序
    if not image_files:
        print("未找到任何图片文件")
        sys.exit(1)
    
    # 对图片进行排序
    image_files.sort(key=lambda x: custom_sort_key(os.path.basename(x)))
    
    # 生成HTML文件
    generate_html(image_files, os.path.join(folder_path, 'index.html'))
    
    print("HTML文件生成完成！")