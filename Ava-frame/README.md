# 头像框添加工具

一个简单的 Python 工具，用于给头像添加精美的头像框。支持多种图片格式，自动调整大小，确保头像完美适配头像框。

## 功能特点

- 支持多种图片格式 (PNG, JPG, JPEG, WebP)
- 自动检测头像和头像框的有效区域
- 智能调整头像大小，避免超出边框
- 自动居中对齐
- 支持多个头像框样式选择

## 使用方法

1. 准备文件：

   - 将您的头像文件命名为 `avatar.jpg` 放在程序根目录
   - 将头像框图片（支持 PNG/JPG/JPEG/WebP）放在 `frame` 文件夹中

2. 运行程序：

   ```powershell
   python add.py
   ```

3. 根据提示选择想要使用的头像框样式

   - 程序会显示所有可用的头像框
   - 输入对应的序号选择头像框

4. 处理完成后，程序会生成 `avatar_with_frame.jpg` 作为结果图片

## 参数调节

如果生成的图片效果不理想，可以在 `add.py` 中调整以下参数：

1. 头像缩放比例：

   ```python
   scale_width = frame_width / avatar_width * 0.8  # 0.8 表示留出 20% 边距
   ```

   - 增大数值(如 0.9)：头像将变大，边距减小
   - 减小数值(如 0.7)：头像将变小，边距增大

2. 图像质量：
   ```python
   result.save(output_path, 'PNG')  # 可以添加 quality 参数控制图片质量
   ```
   - 可修改为：`result.save(output_path, 'PNG', quality=95)`

## 文件结构

```
Ava-frame/
├── add.py          # 主程序
├── avatar.jpg      # 原始头像
├── frame/          # 头像框文件夹
│   └── *.png      # 头像框图片
└── README.md       # 说明文档
```

## 注意事项

1. 头像框图片需要是透明背景的 PNG 格式效果最佳
2. 建议使用分辨率相近的头像和头像框
3. 如果处理结果不理想，可以调整缩放参数
4. 支持的头像框图片格式：PNG, JPG, JPEG, WebP

## 要求

- Python 3.6+
- Pillow 库
  ```powershell
  pip install Pillow
  ```
