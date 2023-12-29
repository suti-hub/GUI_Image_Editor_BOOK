# -*- coding: utf-8 -*-
import cv2
import matplotlib.pyplot as plt

# File path
video_path = './TEST/video_00.mp4'
# Open video
cap    = cv2.VideoCapture(video_path)
# 動画情報取得
frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps    = int(cap.get(cv2.CAP_PROP_FPS))
# 5秒間のフレーム設定
num_frames = int(fps*5)

cur_frame = 0
while cur_frame < num_frames:
    # フレーム取得
    ret, frame = cap.read()
    # フレーム取得できなかった場合は終了
    if not ret:
        break
    # BGR->RGB変換
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # フレーム表示
    title = f'{cur_frame}/{frames} frames, {fps} fps'
    plt.title(title)
    plt.imshow(img)
    plt.show()
    
    cur_frame += 1

# Close Video
cap.release()
