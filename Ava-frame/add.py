from PIL import Image
import os

def find_face_area(img):
    """
    简单地检测图片中人脸区域的范围
    通过分析图片的不透明区域来估计有效内容的范围
    
    Parameters:
        img: PIL Image对象
    Returns:
        (left, top, right, bottom): 有效内容的边界框
    """
    # 获取alpha通道或转换为灰度图
    if img.mode == 'RGBA':
        alpha = img.split()[3]
    else:
        alpha = img.convert('L')
    
    # 获取图像大小
    width, height = img.size
    
    # 找到非透明/非白色区域的边界
    bbox = alpha.getbbox()
    if not bbox:
        return (0, 0, width, height)
    return bbox

def list_frames(frame_dir):
    """列出可用的头像框"""
    frames = []
    for file in os.listdir(frame_dir):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            frames.append(file)
    return frames

def add_frame(avatar_path, frame_path, output_path=None):
    """
    给头像添加头像框，确保头像不会超出头像框
    
    Parameters:
        avatar_path (str): 头像图片路径
        frame_path (str): 头像框图片路径
        output_path (str): 输出图片路径，默认为None（在原头像名称后添加_with_frame）
    """
    try:
        # 打开头像和头像框
        avatar = Image.open(avatar_path).convert('RGBA')
        frame = Image.open(frame_path).convert('RGBA')
        
        # 获取头像框的有效区域
        frame_area = find_face_area(frame)
        frame_width = frame_area[2] - frame_area[0]
        frame_height = frame_area[3] - frame_area[1]
        
        # 获取头像的有效区域
        avatar_area = find_face_area(avatar)
        avatar_width = avatar_area[2] - avatar_area[0]
        avatar_height = avatar_area[3] - avatar_area[1]
        
        # 计算缩放比例，确保头像适应头像框
        scale_width = frame_width / avatar_width * 0.8  # 留出20%的边距
        scale_height = frame_height / avatar_height * 0.8
        scale = min(scale_width, scale_height)
        
        # 调整头像大小
        new_width = int(avatar.width * scale)
        new_height = int(avatar.height * scale)
        avatar = avatar.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 创建一个新的透明背景，大小与头像框相同
        result = Image.new('RGBA', frame.size, (0, 0, 0, 0))
        
        # 计算头像在结果图片中的位置（居中）
        paste_x = (frame.width - new_width) // 2
        paste_y = (frame.height - new_height) // 2
        
        # 粘贴头像
        result.paste(avatar, (paste_x, paste_y))
        
        # 粘贴头像框
        result = Image.alpha_composite(result, frame)
        
        # 如果没有指定输出路径，生成默认输出路径
        if output_path is None:
            filename, ext = os.path.splitext(avatar_path)
            output_path = f"{filename}_with_frame{ext}"
        
        # 保存结果
        result.save(output_path, 'PNG')
        print(f"成功保存处理后的图片到: {output_path}")
        return True
        
    except Exception as e:
        print(f"处理图片时出错: {str(e)}")
        return False

if __name__ == "__main__":
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    frame_dir = os.path.join(current_dir, "frame")
    avatar_path = os.path.join(current_dir, "avatar.jpg")
    
    # 列出所有可用的头像框
    frames = list_frames(frame_dir)
    if not frames:
        print("错误：在frame文件夹中没有找到任何头像框")
        exit(1)
        
    print("\n可用的头像框:")
    for i, frame in enumerate(frames, 1):
        print(f"{i}. {frame}")
    
    # 获取用户选择
    while True:
        try:
            choice = input("\n请选择头像框序号（1-{}）: ".format(len(frames)))
            choice = int(choice)
            if 1 <= choice <= len(frames):
                break
            print("无效的选择，请重试")
        except ValueError:
            print("请输入有效的数字")
    
    # 使用选择的头像框
    frame_path = os.path.join(frame_dir, frames[choice - 1])
    add_frame(avatar_path, frame_path)