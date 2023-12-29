# -*- coding: utf-8 -*-
import sys
import tkinter as tk
from tkinter import ttk, filedialog
from ControlGUI import ControlGUI
import os


class ViewGUI():
    
    def __init__(self, window_root, default_path):
        
        # Controller Class生成
        self.control = ControlGUI(default_path)
        
        # 初期化
        self.dir_path         = None
        self.label_rotate     = [' 90°','180°','270°']
        self.label_flip       = ['U/D','L/R']
        
        # メインウィンドウ
        self.window_root = window_root
        # メインウィンドウサイズ指定
        self.window_root.geometry("800x650") # W x H
        # メインウィンドウタイトル
        self.window_root.title('GUI Image Editor v1.1.1')
        
        # サブウィンドウ
        self.window_sub_ctrl1     = tk.Frame(self.window_root, height=300, width=300)
        self.window_sub_ctrl2     = tk.Frame(self.window_root, height=500, width=400)
        
        # Nootebook, Tab生成
        self.window_sub_frame     = tk.Frame(self.window_root, height=590, width=540)
        self.notebook             = ttk.Notebook(self.window_sub_frame)
        self.tab1                 = tk.Frame(self.notebook, height=560, width=500)
        self.notebook.add(self.tab1, text='[Photo]')
        self.notebook.select(self.tab1)
        self.select_tab           = '[Photo]'
        
        
        # Photo[tab1]
        self.window_sub_ctrl3     = tk.Frame(self.tab1,  height=120, width=400)
        self.window_photo_canvas  = tk.Canvas(self.tab1, height=450, width=400, bg='black')
        
        # オブジェクト
        # StringVar(ストリング)生成
        self.str_dir        = tk.StringVar()
        # IntVar生成 
        self.radio_intvar = []
        for n in range(3):
            self.radio_intvar.append(tk.IntVar())
        self.bar_position   = tk.IntVar()
    
        
        # GUIウィジェット・イベント登録
        # ラベル
        label_s2_blk1       = tk.Label(self.window_sub_ctrl2, text='')
        label_s3_blk1       = tk.Label(self.window_sub_ctrl3, text='')
        label_s3_blk2       = tk.Label(self.window_sub_ctrl3, text='')
        label_target        = tk.Label(self.window_sub_ctrl1, text='[Files]')
        label_rotate        = tk.Label(self.window_sub_ctrl2, text='[Rotate]')
        label_flip          = tk.Label(self.window_sub_ctrl2, text='[Flip]')
        label_clip          = tk.Label(self.window_sub_ctrl2, text='[Clip]')
        label_run           = tk.Label(self.window_sub_ctrl2, text='[Final Edit]')
        label_msg           = tk.Label(self.window_root,      text='[Message]')
        self.label_msgtxt   = tk.Label(self.window_root,      text='')
        
        # フォルダ選択ボタン生成
        self.button_setdir  = tk.Button(self.window_sub_ctrl1,    text = 'Set Folder', width=10, command=self.event_set_folder) 
        #　テキストエントリ生成
        self.entry_dir      = tk.Entry(self.window_sub_ctrl1,     text = 'entry_dir',  state='readonly',  textvariable=self.str_dir, width=39)
        self.str_dir.set(self.dir_path)
        # コンボBOX生成
        self.combo_file     = ttk.Combobox(self.window_sub_ctrl1, text = 'combo_file', value=[], state='readonly', width=36, postcommand=self.event_updatefile)
        self.combo_file.set('..[select file]')
        self.combo_file.bind('<<ComboboxSelected>>', self.event_selectfile)
        
        #　切替ボタン生成
        button_next         = tk.Button(self.window_sub_ctrl3, text = '>>Next',  width=10,command=self.event_next)
        button_prev         = tk.Button(self.window_sub_ctrl3, text = 'Prev<<',  width=10,command=self.event_prev)
        
        # クリップボタン生成
        button_clip_start   = tk.Button(self.window_sub_ctrl2, text = 'Try',     width=5, command=self.event_clip_try)
        button_clip_done    = tk.Button(self.window_sub_ctrl2, text = 'Done',    width=5, command=self.event_clip_done)
        
        # Save/Undo/Drop/SettingSaveボタン生成
        button_save         = tk.Button(self.window_sub_ctrl2, text = 'Save',    width=5, command=self.event_save)
        button_undo         = tk.Button(self.window_sub_ctrl2, text = 'Undo',    width=5, command=self.event_undo)     
        
        # ボタン生成
        self.btn_rotate = []
        for idx, text in enumerate(self.label_rotate): # 1:rot90 2:rot180 3:rot270
            self.btn_rotate.append(tk.Button(self.window_sub_ctrl2, text=text, width=5, command=self.event_rotate(idx)))
            
        self.btn_flip = []
        for idx, text in enumerate(self.label_flip):   # 1:Flip U/L 2:Flip L/R
            self.btn_flip.append(tk.Button(self.window_sub_ctrl2,  text=text,  width=5, command=self.event_flip(idx)))
        
        # マウスイベント登録
        self.window_photo_canvas.bind   ('<ButtonPress-1>',   self.event_clip_start)
        self.window_photo_canvas.bind   ('<Button1-Motion>',  self.event_clip_keep)
        self.window_photo_canvas.bind   ('<ButtonRelease-1>', self.event_clip_end)   
        
        ## ウィジェット配置
        # サブウィンドウ
        self.window_sub_ctrl1.place     (relx=0.68, rely=0.05)
        self.window_sub_ctrl2.place     (relx=0.68, rely=0.25)
        self.window_sub_ctrl3.place     (relx=0.30, rely=0.90)
        self.window_sub_frame.place     (relx=0.01, rely=0.01)
        self.notebook.place             (relx=0.001, rely=0.001)
        # Photo[tab1]
        self.window_photo_canvas.place  (relx=0.09,  rely=0.05)
        
        # window_sub_ctrl1
        self.button_setdir.grid  (row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.entry_dir.grid      (row=2, column=1, padx=5, pady=5, sticky=tk.W)
        label_target.grid        (row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.combo_file.grid     (row=4, column=1, padx=5, pady=5, sticky=tk.W)
        
        # window_sub_ctrl2
        label_rotate.grid        (row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.btn_rotate[0].grid  (row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.btn_rotate[1].grid  (row=3, column=2, padx=5, pady=5, sticky=tk.W)
        self.btn_rotate[2].grid  (row=3, column=3, padx=5, pady=5, sticky=tk.W)
        
        label_flip.grid          (row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.btn_flip[0].grid    (row=5, column=1, padx=5, pady=5, sticky=tk.W)
        self.btn_flip[1].grid    (row=5, column=2, padx=5, pady=5, sticky=tk.W)

        label_clip.grid          (row=6, column=1, padx=5, pady=5, sticky=tk.W)
        button_clip_start.grid   (row=7, column=1, padx=5, pady=5, sticky=tk.W)
        button_clip_done.grid    (row=7, column=2, padx=5, pady=5, sticky=tk.W)
        label_run.grid           (row=8, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
        button_undo.grid         (row=9, column=1, padx=5, pady=5, sticky=tk.W)
        button_save.grid         (row=9, column=2, padx=5, pady=5, sticky=tk.W)
        
        # window_sub_ctrl3
        label_s3_blk1.grid       (row=1, column=1, columnspan=2, padx=5, pady=5, sticky=tk.EW)
        button_prev.grid         (row=1, column=1, padx=5, pady=5, sticky=tk.E)
        label_s3_blk2.grid       (row=1, column=4, columnspan=2, padx=5, pady=5, sticky=tk.EW)
        button_next.grid         (row=1, column=3, padx=5, pady=5, sticky=tk.W)

        # Init
        canvas_dict = {'Photo':self.window_photo_canvas}
        self.control.InitCanvas(canvas_dict)
        self.control.SetTab(self.select_tab)
        self.control.InitStateMachine()

    
    # Private
    def set_message(self, text):
        self.label_msgtxt['text'] = text
        
        
    def clear_message(self): 
        self.label_msgtxt['text'] = ''


    # Event Callback
    # Common
    def event_set_folder(self):
        
        if self.control.IsTransferToState('dir'):
            print(sys._getframe().f_code.co_name)
            
            dir_path = self.control.GetDirPath()
            self.dir_path = filedialog.askdirectory(initialdir=dir_path, mustexist=True)
            self.str_dir.set(self.dir_path)
            self.combo_file['value'] = self.control.SetFileList(self.dir_path)
            
            file_name = self.control.GetCurrentFile()
            self.combo_file.set(file_name)
            print(self.dir_path)
            if file_name == 'None':
                self.control.ForceToState('IDLE')
                self.set_message('No files..to support, try to change folder')
            else:
                self.event_selectfile(None)
                self.clear_message()

        
    def event_updatefile(self):
        
        if self.control.IsTransferToState('dir'):
            print(sys._getframe().f_code.co_name)
            self.combo_file['value'] = self.control.SetFileList(self.dir_path)
            file_name = self.control.GetCurrentFile()
            self.combo_file.set(file_name)
            if file_name == 'None':
                self.control.ForceToState('IDLE')
                self.set_message('No files..to support, try to change folder')

        
    def event_selectfile(self, event):
        
        if self.control.IsTransferToState('set'):
            print(sys._getframe().f_code.co_name)
                        
            set_pos = self.combo_file.current()
            result  = self.control.Set(set_pos, None)
            if not result:
                self.control.ForceToState('IDLE')
                
            self.clear_message()

        
    def event_rotate(self, idx):

        def check_event():
            if self.control.IsTransferToState('edit'):
                cmd = 'rotate-' + str(idx+1)
                self.control.Edit(cmd)
                print('{} {} {}'.format(sys._getframe().f_code.co_name, idx, cmd))
                return check_event
            
        return check_event
        
    
    def event_flip(self, idx):
        
        def check_event():
            if self.control.IsTransferToState('edit'):
                cmd = 'flip-' + str(idx+1)
                self.control.Edit(cmd)
                print('{} {} {}'.format(sys._getframe().f_code.co_name, idx, cmd))
                return check_event
            
        return check_event
        
        
    def event_clip_try(self):
        
        if self.control.IsTransferToState('clip'):
            print(sys._getframe().f_code.co_name)
        
        
    def event_clip_done(self):
        
        if self.control.IsTransferToState('done'):
            print(sys._getframe().f_code.co_name)
            self.control.Edit('clip_done')
    
    
    def event_clip_start(self, event):
        
        if self.control.IsTransferToState('rect'):
            print(sys._getframe().f_code.co_name, event.x, event.y)
            self.control.DrawRectangle('clip_start', event.y, event.x)
    
        
    def event_clip_keep(self, event):
        
        if self.control.IsTransferToState('rect'):
            self.control.DrawRectangle('clip_keep', event.y, event.x)

        
    def event_clip_end(self, event):
        
        if self.control.IsTransferToState('rect'):
            print(sys._getframe().f_code.co_name, event.x, event.y)
            self.control.DrawRectangle('clip_end', event.y, event.x)
        
        
    def event_save(self):
        
        if self.control.IsTransferToState('save'):
            print(sys._getframe().f_code.co_name)
            self.control.Save()

    
    def event_undo(self):
        
        if self.control.IsTransferToState('undo'):
            print(sys._getframe().f_code.co_name)
            self.control.Undo('None')
            self.clear_message()
 
    
    # Photo        
    def event_prev(self):
        
        if self.control.IsTransferToState('prev'):
            print(sys._getframe().f_code.co_name)
            self.control.DrawPhoto('prev')
            file_name = self.control.GetCurrentFile()
            self.combo_file.set(file_name)
        
        
    def event_next(self):
        
        if self.control.IsTransferToState('next'):
            print(sys._getframe().f_code.co_name)
            self.control.DrawPhoto('next')
            file_name = self.control.GetCurrentFile()
            self.combo_file.set(file_name)

    
    def event_ftype(self):
        
        arg0 = self.ftype[self.radio_intvar[0].get()]
        if arg0 == 'mp4':
            self.window_sub_ctrl6.place_forget()
        else:
            self.window_sub_ctrl6.place(relx=0.68, rely=0.78)


def main():
    
    #　Tk MainWindow 生成
    main_window = tk.Tk()
    
    # Viewクラス生成
    current_dir = os.getcwd()
    print(current_dir)
    ViewGUI(main_window, current_dir)
    
    #　フレームループ処理
    main_window.mainloop()
    

if __name__ == '__main__':
    
    main()

   