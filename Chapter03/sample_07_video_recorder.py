# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import cv2

class VideoRecorder:

    def __init__(self, master):
        self.master = master
        self.master.title("VideoRecorder")
        # キャンバス
        self.canvas = tk.Canvas(self.master, width=400, height=300, bg='gray')
        # 動画ファイルを選択するボタン
        self.select_button   = tk.Button(self.master, text="SetFile",  command=self.set_file)      
        # 動画を操作するボタン
        self.playback_button = tk.Button(self.master, text="Play",     command=self.play_video)
        self.record_button   = tk.Button(self.master, text="Rec",      command=self.rec_video)
        self.stop_button     = tk.Button(self.master, text="Stop",     command=self.stop_video)
        # 画面レイアウト
        self.canvas.pack(side="left")
        self.select_button.pack(side="top")
        self.stop_button.pack(side="bottom")
        self.record_button.pack(side="bottom")
        self.playback_button.pack(side="bottom")
        # 変数初期化
        self.cur_frame    = 0
        self.is_setting   = False
        self.is_playing   = False
        self.is_recording = False
        self.cap = None
        self.rec = None
    
    # イベント処理（コールバック関数）
    def set_file(self):
        ext = [('mp4ファイル','*.mp4')]
        self.file_path = filedialog.askopenfilename(filetypes=ext)
        if self.file_path:
            print('Selected:', self.file_path)
            self.set_video()
            self.is_setting = True
        else:
            print('Please choose mp4')
            self.is_setting = False
            
    def play_video(self):
        # 状態判定
        if self.is_setting and not self.is_playing:
            self.is_playing = True
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.cur_frame)
            self.loop_video()
            print('Video playback..', self.is_playing)

    def rec_video(self):
        # 状態判定
        if self.is_setting and not self.is_playing:
            # 動画記録設定
            self.rec_path = self.file_path.replace('.mp4','_gui_record.mp4')
            width         = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height        = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            video_format  = cv2.VideoWriter_fourcc(*'mp4v') 
            self.rec      = cv2.VideoWriter(self.rec_path, video_format, self.fps, (width, height))
            self.is_playing   = True
            self.is_recording = True
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.cur_frame)
            self.loop_video()
            print('Video recording..', self.is_recording)
        
    def stop_video(self):
        # 状態判定
        if self.is_setting and self.is_playing:
            self.canvas.after_cancel(self.vid)
            self.close_video()
            
    
    # 内部処理
    def set_video(self):
        # 動画再生設定
        if self.cap != None:
            self.cap.release()
        self.cap       = cv2.VideoCapture(self.file_path)
        self.frames    = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps       = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.cur_frame = 0
        # 1フレーム表示
        self.ret, self.img = self.cap.read()
        if self.ret:
            self.draw_video()
            self.cur_frame += 1
        return self.ret

    def loop_video(self):
        # フレーム取得
        self.ret, self.img = self.cap.read()
        # フレーム表示
        self.draw_video()
        # フレーム書込
        if self.is_recording:
            self.rec.write(self.img)
        self.cur_frame += 1
        # 再生継続判定
        if self.ret and self.is_playing and self.cur_frame < self.frames:
            # loop_video実行（2ms後）
            self.vid = self.canvas.after(2, self.loop_video)
        else:              
            # 終了処理
            self.cur_frame = 0
            self.close_video()

    def draw_video(self):
        canv_w = self.canvas.winfo_width()
        canv_h = self.canvas.winfo_height()
        # 画像変換＆キャンバス表示
        img_conv    = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)             
        pil_img     = Image.fromarray(img_conv)
        pil_img     = ImageOps.pad(pil_img, (canv_w, canv_h))
        self.tk_img = ImageTk.PhotoImage(image=pil_img)
        self.canvas.create_image(canv_w/2, canv_h/2, image=self.tk_img)
        
    def close_video(self):
        self.is_playing = False
        print('Video playback..', self.is_playing)
        if self.is_recording:
            self.rec.release()
            self.is_recording = False
            print('Video recording..', self.is_recording)
            print('Saved:', self.rec_path)

root = tk.Tk()
VideoRecorder(master=root)
root.mainloop()