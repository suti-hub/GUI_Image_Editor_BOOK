# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import time

# File path(測定対象の画像ファイルのパス)
file_path = '../Chapter03/TEST/image_00.jpg'
print('=== Pillow ===')
print('-----------------')
# 画像リード
t0 = time.perf_counter()
pil_org = Image.open(file_path)
t1 = time.perf_counter()
print(f' Read:\t{(t1-t0)*1e6:.1f} us')
# リサイズ
t0 = time.perf_counter()
pil_resize = pil_org.resize((300, 300))
t1 = time.perf_counter()
print(f' リサイズ:\t{(t1-t0)*1e6:.1f} us')
print('-----------------')
# 回転
t0 = time.perf_counter()
pil_rot = pil_org.rotate(90)
t1 = time.perf_counter()
print(f' 回転:\t{(t1-t0)*1e6:.1f} us')
# 左右反転
t0 = time.perf_counter()
pil_flip = ImageOps.mirror(pil_org)
t1 = time.perf_counter()
print(f' 左右反転:\t{(t1-t0)*1e6:.1f} us')
# クロップ
t0 = time.perf_counter()
pil_crop = pil_org.crop((500, 500, 500+500, 500+500))
t1 = time.perf_counter()
print(f' クロップ:\t{(t1-t0)*1e6:.1f} us')

print('\n=== Numpy ===')
print('-----------------')
# Numpy変換
t0 = time.perf_counter()
np_org  = np.array(pil_org)
t1 = time.perf_counter()
print(f' Numpy変換:\t{(t1-t0)*1e6:.1f} us')
# PIL変換
t0 = time.perf_counter()
pil_org  = Image.fromarray(np_org)
t1 = time.perf_counter()
print(f' PIL変換:\t{(t1-t0)*1e6:.1f} us')
print('-----------------')
# 回転
t0 = time.perf_counter()
np_rot  = np.rot90(np_org, 1)
t1 = time.perf_counter()
print(f' 回転:\t{(t1-t0)*1e6:.1f} us')
# 左右反転
t0 = time.perf_counter()
np_flip  = np.flip(np_org, axis=1)
t1 = time.perf_counter()
print(f' 左右反転:\t{(t1-t0)*1e6:.1f} us')
# クロップ
t0 = time.perf_counter()
np_crop  = np_org[500:1000,500:1000,:]
t1 = time.perf_counter()
print(f' クロップ:\t{(t1-t0)*1e6:.1f} us')






