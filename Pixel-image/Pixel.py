from PIL import Image, ImageEnhance, ImagePalette
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
    
    def apply_dithering(self, image):
        """
        应用抖动效果，使图像更有复古像素画的感觉
        
        Args:
            image (Image): 输入图片
        
        Returns:
            Image: 应用抖动效果后的图片
        """
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # 转换为带有抖动效果的图像
        palette_image = image.convert('P', palette=Image.ADAPTIVE, colors=32, dither=Image.FLOYDSTEINBERG)
        return palette_image.convert('RGB')

    def apply_pixel_art_effect(self, image):
        """
        应用像素画效果增强
        
        Args:
            image (Image): 输入图片
        
        Returns:
            Image: 增强后的图片
        """
        # 增加局部对比度
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
        
        # 增加锐度以突出边缘
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(2.0)
        
        return image

    def reduce_colors(self, image, num_colors=16):
        """
        减少颜色数量，并保持像素画风格的鲜明色彩
        
        Args:
            image (Image): 输入图片
            num_colors (int): 期望的颜色数量
        
        Returns:
            Image: 处理后的图片
        """
        # 使用中位切割法进行颜色量化
        return image.quantize(colors=num_colors, method=2).convert('RGB')
    
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

    def convert_to_pixel_art(self, color_mode="color", num_colors=16, edge_enhance=2.0, contrast=1.5):
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
        
        # 首先将图片缩小，这样在放大时会产生更明显的像素效果
        small_size = (new_width // self.pixel_size, new_height // self.pixel_size)
        image = self.image.resize(small_size, Image.NEAREST)
        
        # 转换颜色模式
        if color_mode == "bw":
            image = image.convert("L")
        else:
            # 减少颜色数量
            image = self.reduce_colors(image, num_colors)
            # 应用抖动效果
            image = self.apply_dithering(image)
        
        # 放大到原始尺寸，使用最近邻插值保持像素的锐利度
        image = image.resize((new_width, new_height), Image.NEAREST)
        
        # 应用像素画效果增强
        image = self.apply_pixel_art_effect(image)
        
        return image
    
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
    
    # 创建转换器实例 - 使用较小的像素大小以获得更好的效果
    converter = PixelArtConverter(input_path, pixel_size=4)
    
    # 生成增强的彩色像素风格
    color_image = converter.convert_to_pixel_art(
        color_mode="color",
        num_colors=16,    # 使用较少的颜色以获得更明显的像素画效果
        edge_enhance=2.0, # 增强边缘效果
        contrast=1.5      # 适度增加对比度
    )
    converter.save(os.path.join(output_dir, "pixel_color.jpg"), color_image)
    
    # 生成增强的黑白像素风格
    bw_image = converter.convert_to_pixel_art(
        color_mode="bw",
        edge_enhance=2.0,
        contrast=1.8
    )
    converter.save(os.path.join(output_dir, "pixel_bw.jpg"), bw_image)
    
    print("Have Done!")

if __name__ == "__main__":
    main()