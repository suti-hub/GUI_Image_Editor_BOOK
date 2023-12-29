# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import os
import numpy as np

class ImageViewer:
    
    def __init__(self, master):
        self.master = master
        self.master.title("ImageViewer")
        # キャンバス
        self.canvas = tk.Canvas(self.master, width=400, height=300, bg='gray')
        # 画像ファイルのフォルダを選択するボタン
        self.select_button      = tk.Button(self.master, text="SetFolder",  command=self.set_folder)      
        # 画像を90度回転、上下反転、左右反転するボタン
        self.rotate_button      = tk.Button(self.master, text="Rotate90",   command=self.rotate_image)      
        self.flip_lr_button     = tk.Button(self.master, text="FlipLR",     command=self.flip_imageLR)     
        self.flip_tb_button     = tk.Button(self.master, text="FlipUD",     command=self.flip_imageUD)
        # フォルダの画像（png拡張子）をスライドショーで順に表示するボタン
        self.slideshow_button   = tk.Button(self.master, text="Next",       command=self.next_show)       
        # 画面レイアウト
        self.canvas.pack(side="left")
        self.select_button.pack(side="top")
        self.rotate_button.pack(side="top")
        self.flip_lr_button.pack(side="top")
        self.flip_tb_button.pack(side="top")
        self.slideshow_button.pack(side="bottom")
        # 変数初期化
        self.images = []
        self.index = -1
        self.current_image = None
        self.is_setting    = False
   
    # イベント処理（コールバック関数）
    def set_folder(self):
        folder_path = filedialog.askdirectory()
        self.images = self.set_file_list(folder_path)
        if len(self.images) > 0:       
            self.index = 0
            self.current_image = Image.open(self.images[self.index])
            self.draw_image()
            self.is_setting    = True
        else:
            self.is_setting    = False
            print('Please choose folder(.png or .jpg files)')
        
    def rotate_image(self):
        # 状態判定
        if self.is_setting:
            self.current_image = self.edit_image('Rotate90')
            self.draw_image()

    def flip_imageLR(self):
        # 状態判定
        if self.is_setting:  
            self.current_image = self.edit_image('FlipLR')
            self.draw_image()

    def flip_imageUD(self):
        # 状態判定
        if self.is_setting:
            self.current_image = self.edit_image('FlipUD')
            self.draw_image()

    def next_show(self):
        # 状態判定
        if self.is_setting:
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.current_image = Image.open(self.images[self.index])
            self.draw_image()

    # 内部処理
    def set_file_list(self, dir_path):
        target_files = []
        file_list = os.listdir(dir_path)
        for file_name in file_list:
            if '.png' in file_name or '.jpg' in file_name:
                file_path = os.path.join(dir_path, file_name)
                target_files.append(file_path)        
        return target_files
    
    def edit_image(self, command):
        np_img = np.array(self.current_image)
        if command == 'FlipUD':
            np_img = np.flip(np_img, axis=0)
        elif command == 'FlipLR':
            np_img = np.flip(np_img, axis=1)
        elif command == 'Rotate90':
            np_img = np.rot90(np_img, 1)
        return Image.fromarray(np_img)
            
    def draw_image(self):
        canv_w      = self.canvas.winfo_width()
        canv_h      = self.canvas.winfo_height()
        pil_img     = ImageOps.pad(self.current_image, (canv_w, canv_h))
        self.tk_img = ImageTk.PhotoImage(image=pil_img)
        self.canvas.create_image(canv_w/2, canv_h/2, image=self.tk_img)

root = tk.Tk()
ImageViewer(master=root)
root.mainloop()