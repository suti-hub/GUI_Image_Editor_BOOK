# -*- coding: utf-8 -*-
import cv2
import matplotlib.pyplot as plt

# File path
video_path = './TEST/video_00.mp4'
save_path  = './TEST/video_record.mp4'
# Open video
cap    = cv2.VideoCapture(video_path)
# 動画情報取得
frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps    = int(cap.get(cv2.CAP_PROP_FPS))
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 5～10秒間のフレーム設定
fno_sp, fno_ep = int(fps*5), int(fps*10)
# フレーム開始位置
cap.set(cv2.CAP_PROP_POS_FRAMES, fno_sp)
# Open Video Writer
video_format = cv2.VideoWriter_fourcc(*'mp4v') 
video  = cv2.VideoWriter(save_path, video_format, fps, (width, height))

cur_frame = fno_sp
while cur_frame < fno_ep+1:
    # フレーム取得
    ret, frame = cap.read()
    # フレーム取得できなかった場合は終了
    if not ret:
        break
    # BGR->RGB変換
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # フレーム保存
    video.write(frame)
    # フレーム表示
    title = f'{cur_frame}/{fno_ep} frames, {fps} fps'
    plt.title(title)
    plt.imshow(img)
    plt.show()
    
    cur_frame += 1

# Close Video
cap.release()
video.release()
print('Saved:', save_path)
