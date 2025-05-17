from PIL import Image, ImageEnhance
import os
import numpy as np

class PixelArtConverter:
    def __init__(self, input_path, pixel_size=1):
        """
        初始化像素艺术转换器
        
        Args:
            input_path (str): 输入图片的路径
            pixel_size (int): 像素块的大小，默认为1
        """
        self.input_path = input_path
        self.pixel_size = pixel_size
        self.image = Image.open(input_path)
    
    def quantize_colors(self, image, num_colors=8):
        """
        对图片进行颜色量化
        
        Args:
            image (Image): 输入图片
            num_colors (int): 量化后的颜色数量
        
        Returns:
            Image: 颜色量化后的图片
        """
        return image.quantize(colors=num_colors).convert(image.mode)
    
    def enhance_edges(self, image, factor=1.5):
        """
        增强图片边缘
        
        Args:
            image (Image): 输入图片
            factor (float): 边缘增强系数
        
        Returns:
            Image: 边缘增强后的图片
        """
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(factor)
    
    def adjust_contrast(self, image, factor=1.3):
        """
        调整图片对比度
        
        Args:
            image (Image): 输入图片
            factor (float): 对比度调整系数
        
        Returns:
            Image: 对比度调整后的图片
        """
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)

    def convert_to_pixel_art(self, color_mode="color", num_colors=8, edge_enhance=1.5, contrast=1.3):
        """
        将图片转换为像素风格
        
        Args:
            color_mode (str): 'color' 为彩色像素，'bw' 为黑白像素
            num_colors (int): 量化后的颜色数量
            edge_enhance (float): 边缘增强系数
            contrast (float): 对比度调整系数
            
        Returns:
            Image: 转换后的图片
        """
        # 调整图片大小，使其能被像素大小整除
        width, height = self.image.size
        new_width = width - (width % self.pixel_size)
        new_height = height - (height % self.pixel_size)
        image = self.image.resize((new_width, new_height))
        
        # 如果是黑白模式，先转换为灰度图
        if color_mode == "bw":
            image = image.convert("L")
            pixel_image = Image.new("L", image.size)
        else:
            # 对彩色图像进行颜色量化
            image = self.quantize_colors(image, num_colors)
            pixel_image = Image.new(image.mode, image.size)
        
        # 遍历图片，按像素块处理
        for i in range(0, new_width, self.pixel_size):
            for j in range(0, new_height, self.pixel_size):
                # 获取像素块的平均颜色
                box = (i, j, i + self.pixel_size, j + self.pixel_size)
                region = image.crop(box)
                if color_mode == "bw":
                    color = int(sum(region.getdata()) / (self.pixel_size * self.pixel_size))
                else:
                    r = int(sum(p[0] for p in region.getdata()) / (self.pixel_size * self.pixel_size))
                    g = int(sum(p[1] for p in region.getdata()) / (self.pixel_size * self.pixel_size))
                    b = int(sum(p[2] for p in region.getdata()) / (self.pixel_size * self.pixel_size))
                    color = (r, g, b)
                
                # 填充像素块
                for x in range(i, i + self.pixel_size):
                    for y in range(j, j + self.pixel_size):
                        pixel_image.putpixel((x, y), color)
        
        # 应用边缘增强和对比度调整
        if edge_enhance > 1.0:
            pixel_image = self.enhance_edges(pixel_image, edge_enhance)
        if contrast != 1.0:
            pixel_image = self.adjust_contrast(pixel_image, contrast)
        
        return pixel_image
    
    def save(self, output_path, converted_image):
        """
        保存转换后的图片
        
        Args:
            output_path (str): 输出图片的路径
            converted_image (Image): 转换后的图片
        """
        converted_image.save(output_path)

def main():
    # 示例用法
    input_path = "img.jpg"  # 输入图片路径
    output_dir = "output"   # 输出目录
    
    # 创建输出目录（如果不存在）
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 创建转换器实例
    converter = PixelArtConverter(input_path, pixel_size=10)
    
    # 生成增强的彩色像素风格
    color_image = converter.convert_to_pixel_art(
        color_mode="color",
        num_colors=8,     # 减少颜色数量，使效果更明显
        edge_enhance=1.5, # 增强边缘
        contrast=1.3      # 增加对比度
    )
    converter.save(os.path.join(output_dir, "pixel_color.jpg"), color_image)
    
    # 生成增强的黑白像素风格
    bw_image = converter.convert_to_pixel_art(
        color_mode="bw",
        edge_enhance=1.8, # 黑白模式下可以使用更强的边缘增强
        contrast=1.5      # 黑白模式下增加更多对比度
    )
    converter.save(os.path.join(output_dir, "pixel_bw.jpg"), bw_image)

if __name__ == "__main__":
    main()