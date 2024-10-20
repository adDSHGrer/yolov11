import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2
import os
import random


# 数据增强函数
def get_train_transforms():
    return A.Compose([
        # 几何变换
        A.HorizontalFlip(p=0.5),  # 50%的概率进行水平翻转
        A.RandomRotate90(p=0.5),  # 50%的概率随机旋转90度
        A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.2, rotate_limit=15, p=0.5),  # 平移、缩放、旋转
        # 颜色调整
        A.RandomBrightnessContrast(p=0.5),  # 随机亮度和对比度调整
        A.HueSaturationValue(hue_shift_limit=20, sat_shift_limit=30, val_shift_limit=20, p=0.5),  # 随机色调、饱和度调整
        # 添加噪声
        A.GaussNoise(p=0.3),  # 30%的概率添加高斯噪声
        # 归一化和转换为tensor
        A.Normalize(),  # 标准化到[0, 1]
        ToTensorV2()  # 转换为Tensor
    ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))


def get_val_transforms():
    return A.Compose([
        A.Normalize(),
        ToTensorV2()
    ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))


# 示例加载图像和标签
def load_image_and_labels(image_path, label_path):
    image = cv2.imread(image_path)
    h, w, _ = image.shape
    with open(label_path, 'r') as f:
        labels = []
        bboxes = []
        for line in f.readlines():
            label_info = line.strip().split()
            class_id = int(label_info[0])
            bbox = list(map(float, label_info[1:]))
            labels.append(class_id)
            bboxes.append(bbox)
    return image, bboxes, labels


# 保存增强后的图像和标签
def save_augmented_image_and_labels(image, bboxes, class_labels, save_dir, image_name):
    os.makedirs(save_dir, exist_ok=True)
    augmented_image_path = os.path.join(save_dir, f'{image_name}.jpg')
    augmented_label_path = os.path.join(save_dir, f'{image_name}.txt')

    # 保存图像
    cv2.imwrite(augmented_image_path, image)

    # 保存标签
    with open(augmented_label_path, 'w') as f:
        for bbox, class_id in zip(bboxes, class_labels):
            bbox_str = ' '.join(map(str, bbox))
            f.write(f'{class_id} {bbox_str}\n')


# 数据增强应用函数
# 数据增强应用函数
def augment_data(train_images_dir, train_labels_dir, save_dir, transform, augment_times=5):
    image_files = os.listdir(train_images_dir)

    for image_file in image_files:
        image_path = os.path.join(train_images_dir, image_file)
        label_path = os.path.join(train_labels_dir, image_file.replace('.jpg', '.txt'))

        image, bboxes, class_labels = load_image_and_labels(image_path, label_path)

        # 对每张图片增强多次
        for i in range(augment_times):
            # 进行数据增强
            augmented = transform(image=image, bboxes=bboxes, class_labels=class_labels)
            augmented_image = augmented['image']
            augmented_bboxes = augmented['bboxes']
            augmented_class_labels = augmented['class_labels']

            # 保存增强后的图像和标签
            save_augmented_image_and_labels(augmented_image.permute(1, 2, 0).numpy(), augmented_bboxes,
                                            augmented_class_labels, save_dir, f"{image_file.split('.')[0]}_aug_{i}")


# 使用数据增强
train_images_dir = 'H:/broken'  # 替换为你的训练图像路径
train_labels_dir = 'H:/out_broken'  # 替换为你的训练标签路径
save_dir = 'H:/augmented/data'  # 替换为你想保存增强后数据的路径



train_transforms = get_train_transforms()
augment_data(train_images_dir, train_labels_dir, save_dir, train_transforms)
