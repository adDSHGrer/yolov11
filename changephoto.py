import os
from PIL import Image

# 需要读取的目录
input_dir = 'H:/broken'
# 转换后保存的目录
output_dir = 'H:/broken'

# 确保输出目录存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 遍历目录中的所有图片
for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):  # 添加.lower()以忽略大小写
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename.rsplit('.', 1)[0] + '.jpg')  # 将所有图片保存为JPEG

        try:
            # 打开图片
            with Image.open(input_path) as image:
                # 检查图片模式并转换
                if image.mode in ('RGBA', 'P'):  # 同时处理RGBA和P模式
                    print(f"Converting {filename} from {image.mode} to RGB")
                    image = image.convert('RGB')  # 转换为RGB模式

                # 保存为JPEG格式
                image.save(output_path, 'JPEG')
                print(f"Saved {filename} as JPEG in {output_dir}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    else:
        print(f"Skipping unsupported file format: {filename}")
