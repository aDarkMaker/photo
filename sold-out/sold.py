from PIL import Image
from rembg import remove
from PIL.ImageFilter import GaussianBlur

def create_sold_out_image():
    # 打开原始商品图片
    item_img = Image.open('item.jpg')
    
    # 使用rembg移除背景，获取主体
    subject = remove(item_img)
    
    # 创建模糊背景
    background = item_img.copy()
    background = background.filter(GaussianBlur(radius=20))
    
    # 将主体粘贴到模糊背景上
    background.paste(subject, (0, 0), subject)
    
    # 转换为灰度图
    gray_img = background.convert('LA').convert('RGBA')
    
    # 打开sold-out水印图片
    watermark = Image.open('sold-out.webp')
    
    # 计算水印位置（右下角）
    x = item_img.width - watermark.width - 20  # 右边留20像素边距
    y = item_img.height - watermark.height - 20  # 下边留20像素边距
    
    # 将水印粘贴到灰度图上
    gray_img.paste(watermark, (x, y), watermark)
    
    # 保存最终图片
    gray_img.save('sold-out.png')
    print("Have Done: sold-out.png")

if __name__ == "__main__":
    create_sold_out_image()