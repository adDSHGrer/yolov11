import json
import os

# 输入包含JSON文件的目录
input_dir = 'H:\out_broken'  # 替换为您的JSON文件夹路径

# 遍历目录中的所有JSON文件
for filename in os.listdir(input_dir):
    if filename.endswith('.json'):  # 只处理JSON文件
        input_json_path = os.path.join(input_dir, filename)

        # 读取JSON文件
        with open(input_json_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        # 生成输出TXT文件的路径
        output_txt_path = os.path.join(input_dir, filename.rsplit('.', 1)[0] + '.txt')

        # 将结果写入TXT文件
        with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
            # 遍历形状列表
            for shape in data['shapes']:
                label = shape['label']
                points = shape['points']
                print(output_txt_path)
                print(label)
                # 计算相对坐标
                x1, y1 = points[0]
                x2, y2 = points[1]
                image_width = data['imageWidth']
                image_height = data['imageHeight']

                relative_x1 = (x1 / image_width)
                relative_y1 = (y1 / image_height)
                relative_x2 = (x2 / image_width)
                relative_y2 = (y2 / image_height)

                # 只需要一行并按照要求格式化
                result_line = f"{label} {relative_x1:.6f} {relative_y1:.6f} {relative_x2:.6f} {relative_y2:.6f}"

                # 写入TXT文件
                txt_file.write(result_line + '\n')

        print(f"转换完成，结果已保存到 {output_txt_path}")
