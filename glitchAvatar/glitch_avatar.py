import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import random

def glitch_image(input_path, output_path, max_offset=20, band_height=10, color_glitch_prob=0.3):
    img = Image.open(input_path).convert('RGB')
    arr = np.array(img)
    h, w, c = arr.shape

    y = 0
    while y < h:
        # 随机带宽
        curr_band_height = random.randint(int(band_height*0.7), int(band_height*1.5))
        if y + curr_band_height > h:
            curr_band_height = h - y
        offset = random.randint(-max_offset, max_offset)
        band = np.copy(arr[y:y+curr_band_height])
        band = np.roll(band, offset, axis=1)
        # 彩色扰动
        if random.random() < color_glitch_prob:
            color = random.choice([(30,0,0), (0,30,0), (0,0,30), (30,30,0), (0,30,30), (30,0,30)])
            band = np.clip(band + color, 0, 255)
        # 饱和度/亮度扰动
        if random.random() < 0.15:
            band_img = Image.fromarray(band.astype(np.uint8))
            enhancer = ImageEnhance.Color(band_img)
            band_img = enhancer.enhance(random.uniform(0.3, 1.7))
            band = np.array(band_img)
        if random.random() < 0.1:
            band_img = Image.fromarray(band.astype(np.uint8))
            enhancer = ImageEnhance.Brightness(band_img)
            band_img = enhancer.enhance(random.uniform(0.5, 1.5))
            band = np.array(band_img)
        # 条带边缘模糊处理
        if curr_band_height > 4:
            band_img = Image.fromarray(band.astype(np.uint8))
            band_img = band_img.filter(ImageFilter.GaussianBlur(radius=1))
            band = np.array(band_img)
        # 与上下条带边缘混合，过渡更自然
        if y > 0:
            blend_height = min(4, curr_band_height, y)
            alpha = np.linspace(0, 1, blend_height)[:, None, None]
            arr[y:y+blend_height] = (1-alpha)*arr[y:y+blend_height] + alpha*band[:blend_height]
            arr[y+blend_height:y+curr_band_height] = band[blend_height:]
        else:
            arr[y:y+curr_band_height] = band
        y += curr_band_height

    # 彩色通道偏移
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    r = np.roll(r, random.randint(-5, 5), axis=1)
    g = np.roll(g, random.randint(-5, 5), axis=0)
    b = np.roll(b, random.randint(-5, 5), axis=1)
    arr[:,:,0], arr[:,:,1], arr[:,:,2] = r, g, b

    glitched_img = Image.fromarray(arr.astype(np.uint8))
    glitched_img.save(output_path)
    print(f"Have Done：{output_path}")

if __name__ == "__main__":
    glitch_image("avatar.jpg", "avatar_glitch.jpg")