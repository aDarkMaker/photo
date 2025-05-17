from PIL import Image
from rembg import remove
from PIL.ImageFilter import GaussianBlur

def create_sold_out_image():
    # 打开原始商品图片
    item_img = Image.open('item.jpg')
      # 使用rembg移除背景，获取主体，并稍微模糊处理
    subject = remove(item_img)
    subject = subject.filter(GaussianBlur(radius=1))  # 对主体轻微模糊，使边缘更自然
    
    # 创建模糊背景
    background = item_img.copy()
    background = background.filter(GaussianBlur(radius=5))  # 降低背景模糊程度
    
    # 将主体粘贴到模糊背景上，使用半透明效果
    mask = subject.split()[3].point(lambda x: x * 0.95)  # 降低不透明度到95%
    background.paste(subject, (0, 0), mask)
    
    # 转换为灰度图
    gray_img = background.convert('LA').convert('RGBA')
      # 打开sold-out水印图片
    watermark = Image.open('sold-out.webp')
    
    # 计算合适的水印大小（基于图片宽度）
    target_width = int(item_img.width * 0.5)  # 水印宽度设为图片宽度的1/2
    ratio = target_width / watermark.width
    target_height = int(watermark.height * ratio)
    watermark = watermark.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    # 获取主体的边界框
    bbox = subject.getbbox()
    if bbox:
        # 根据主体位置调整水印位置
        subject_right = bbox[2]
        subject_bottom = bbox[3]
        
        # 计算水印位置，避免遮挡主体
        x = max(item_img.width - watermark.width - 10,  # 默认右边距10像素
               min(subject_right - watermark.width, item_img.width - watermark.width - 15))  # 确保不超出图片边界
        y = max(item_img.height - watermark.height - 10,  # 默认下边距10像素
               min(subject_bottom - watermark.height, item_img.height - watermark.height - 15))  # 确保不超出图片边界
    else:
        # 如果未检测到主体，使用默认位置（右下角）
        x = item_img.width - watermark.width - 10
        y = item_img.height - watermark.height - 10
    
    # 将水印粘贴到灰度图上
    gray_img.paste(watermark, (x, y), watermark)
    
    # 保存最终图片
    gray_img.save('sold-out.png')
    print("Have Done: sold-out.png")

if __name__ == "__main__":
    create_sold_out_image()