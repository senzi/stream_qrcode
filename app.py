import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import pyqrcode
from datetime import datetime
from PIL import Image, ImageDraw

# 二维码配置参数
version = 10  # 固定版本确保尺寸一致
error = 'H'  # 高级别错误纠正
scale = 8    # 缩放比例
duration = 50

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中获取API密钥
api_key = os.getenv('MOONSHOT_API_KEY')

# 检查 API 密钥是否成功加载
if api_key is None:
    raise ValueError("API key not found. Please set MOONSHOT_API_KEY in your .env file.")

# 配置 OpenAI 客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.moonshot.cn/v1",
)

# 获取用户输入的内容
user_input = input("请输入你的问题：")

response = client.chat.completions.create(
    model="moonshot-v1-8k",
    messages=[
        {
            "role": "system",
            "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。",
        },
        {"role": "user", "content": user_input},
    ],
    temperature=0.7,
    stream=True,
)

# 创建一个基于当前时间戳的目录
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
directory = f"./{timestamp}_chunks"
os.makedirs(directory, exist_ok=True)

# 创建一个列表存储二维码图像路径
qr_code_paths = []


collected_messages = []
# 遍历每个chunk并生成独立的JSON
for idx, chunk in enumerate(response):
    choice = chunk.choices[0]  # 假设每个chunk只有一个choice
    content = choice.delta.content if choice.delta.content is not None else ''
    finish_reason = choice.finish_reason if choice.finish_reason is not None else ''

    chunk_message = chunk.choices[0].delta
    if not chunk_message.content:
        continue
    collected_messages.append(chunk_message)
    
    reconstructed_chunk = {
        'Chunk': idx + 1,  # 自然生成的Chunk序号
        'Content': content,
        'Finish': finish_reason
    }
    
    # 将单个chunk转换为JSON格式
    chunk_json = json.dumps(reconstructed_chunk, ensure_ascii=False, indent=2)
    
    # 生成二维码这里进行编码转换
    qr = pyqrcode.create(chunk_json.encode('utf-8').decode('latin-1'), version=version, error=error)
    
    # 保存二维码图像
    qr_code_path = os.path.join(directory, f"Chunk{idx + 1}.png")
    qr.png(qr_code_path, scale=5)
    qr_code_paths.append(qr_code_path)
    
    print(f"Saved QR code for Chunk {idx + 1} to {qr_code_path}")


# 假设 qr_code_paths 和 directory 已经定义
images_with_progress = []

# 获取所有二维码图像的最大尺寸
max_width, max_height = 0, 0
for qr_code_path in qr_code_paths:
    image = Image.open(qr_code_path)
    max_width = max(max_width, image.width)
    max_height = max(max_height, image.height)

# 遍历每个二维码文件并添加进度条
for idx, qr_code_path in enumerate(qr_code_paths):
    # 打开每个二维码图像并转换为 RGBA 模式
    image = Image.open(qr_code_path).convert("RGBA")

    # 创建一个新图像，尺寸为最大尺寸，背景透明
    new_image = Image.new("RGBA", (max_width, max_height), (255, 255, 255, 0))
    new_image.paste(image, (0, 0))

    # 创建一个绘图对象
    draw = ImageDraw.Draw(new_image)

    # 计算进度条参数
    bar_width = new_image.width
    bar_height = 10
    progress = (idx + 1) / len(qr_code_paths)
    filled_width = int(bar_width * progress)

    # 绘制进度条背景
    draw.rectangle([0, new_image.height - bar_height, bar_width, new_image.height], fill="lightgray")

    # 绘制进度条前景
    draw.rectangle([0, new_image.height - bar_height, filled_width, new_image.height], fill="green")

    # 添加图像到列表
    images_with_progress.append(new_image)

    # 保存临时图像以验证进度条是否正确绘制
    temp_image_path = os.path.join(directory, f"Chunk_with_progress_{idx + 1}.png")
    new_image.save(temp_image_path)
    print(f"Saved temporary image with progress bar to {temp_image_path}")

# 将图像保存为 GIF 动画
output_gif_path = os.path.join(directory, "response.gif")
images_with_progress[0].save(output_gif_path, save_all=True, append_images=images_with_progress[1:], duration=duration, loop=0)

print(f"GIF with progress bar saved to {output_gif_path}")

# 假设 collected_messages 已经定义
full_conversation = ''.join([m.content for m in collected_messages])

# 保存全文对话到 response.txt
output_txt_path = os.path.join(directory, "response.txt")
with open(output_txt_path, 'w', encoding='utf-8') as f:
    f.write(f"Full conversation received: {full_conversation}")

print(f"Full conversation saved to {output_txt_path}")
print(f"Full conversation received: {''.join([m.content for m in collected_messages])}")