# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from PIL import Image, ImageOps

# ファイルパス（表示したい画像のパスに書き換えてください）
file_path  = './TEST/image_00.jpg'
# 画像リード
pil_org    = Image.open(file_path)
# 高さ、幅
h, w       = pil_org.height, pil_org.width
# リサイズ
pil_resize = pil_org.resize((h//2, w//2))
# 回転
pil_rot    = pil_org.rotate(90)
# 左右反転
pil_flip   = ImageOps.mirror(pil_org)
# クロップ
cy, cx     = h//4, w//4
pil_crop   = pil_org.crop((cx, cy, cx+w/2, cy+h//2))
# 辞書保存
pil_imgs = {'Original':pil_org,'Rotate90':pil_rot,'Flip':pil_flip,'Crop':pil_crop}
# 辞書読み出し
for key, pil_img in pil_imgs.items():
    # 画像表示
    plt.title(key)
    plt.imshow(pil_img)
    plt.show()
    # 画像保存
    pil_img.save(file_path.replace('.jpg', f'_pil_{key}.png'))




