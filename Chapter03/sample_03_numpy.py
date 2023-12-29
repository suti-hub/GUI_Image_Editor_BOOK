# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
 
# ファイルパス（表示したい画像のパスに書き換えてください）
file_path  = './TEST/image_00.jpg'
# 画像リード
pil_org   = Image.open(file_path)
# Numpy変換
np_org    = np.array(pil_org)
# 高さ、幅
h, w, ch  = np_org.shape
# 回転
np_rot    = np.rot90(np_org, 1)
# 左右反転
np_flip   = np.flip(np_org, axis=1)
# クロップ
cy, cx    = h//4, w//4
np_crop   = np_org[cy:cy+h//2, cx:cx+w//2,:]
# 辞書保存
np_imgs = {'Original':np_org,'Rotate90':np_rot,'Flip':np_flip,'Crop':np_crop}
# 辞書読み出し
for key, np_img in np_imgs.items():
    # 画像表示
    plt.title(key)
    plt.imshow(np_img)
    plt.show()
    # Pillow変換
    pil_img = Image.fromarray(np_img)
    # 画像保存
    pil_img.save(file_path.replace('.jpg', f'_np_{key}.png'))




