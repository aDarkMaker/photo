# 像素风格图片转换器 (Pixel Art Converter)

一个简单而强大的 Python 工具，可以将普通图片转换为像素艺术风格。支持彩色和黑白两种模式，并提供多种图像增强选项。

## 功能特点

- 🎨 支持彩色和黑白两种像素风格
- 🔧 可调整像素块大小
- 🎯 智能颜色量化
- ✨ 边缘增强效果
- 🔆 对比度调整
- 💾 自动创建输出目录

## 环境要求

- Python 3.6+
- Pillow (PIL)
- NumPy

## 安装依赖

```bash
pip install Pillow numpy
```

## 使用方法

1. 将你想要转换的图片放在项目目录下，命名为 `img.jpg`，或者修改代码中的 `input_path`
2. 运行脚本：

```bash
python Pixel.py
```

3. 转换后的图片将保存在 `output` 目录下：
   - `pixel_color.jpg`: 彩色像素风格
   - `pixel_bw.jpg`: 黑白像素风格

## 代码示例

```python
# 创建转换器实例
converter = PixelArtConverter("img.jpg", pixel_size=10)

# 生成彩色像素风格
color_image = converter.convert_to_pixel_art(
    color_mode="color",
    num_colors=8,     # 减少颜色数量
    edge_enhance=1.5, # 增强边缘
    contrast=1.3      # 增加对比度
)

# 生成黑白像素风格
bw_image = converter.convert_to_pixel_art(
    color_mode="bw",
    edge_enhance=1.8, # 更强的边缘增强
    contrast=1.5      # 更高的对比度
)
```

## 参数说明

### PixelArtConverter 类

- `input_path`: 输入图片路径
- `pixel_size`: 像素块大小，默认为 1

### convert_to_pixel_art 方法

- `color_mode`: 'color' 为彩色像素，'bw' 为黑白像素
- `num_colors`: 颜色量化后的颜色数量（仅彩色模式有效）
- `edge_enhance`: 边缘增强系数（建议范围：1.0-2.0）
- `contrast`: 对比度调整系数（建议范围：1.0-2.0）

## 自定义效果

你可以通过调整以下参数来获得不同的视觉效果：

1. **像素大小**：增加 `pixel_size` 可以获得更明显的像素效果
2. **颜色数量**：减少 `num_colors` 可以获得更复古的游戏风格
3. **边缘增强**：增加 `edge_enhance` 可以使像素边缘更清晰
4. **对比度**：增加 `contrast` 可以使颜色更鲜明

## 注意事项

- 输入图片尺寸会自动调整以适应像素大小
- 建议从小尺寸图片开始尝试，以获得最佳效果
- 过大的增强系数可能会导致图片失真
