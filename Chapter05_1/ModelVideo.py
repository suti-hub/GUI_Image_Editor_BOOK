# -*- coding: utf-8 -*-
import os
import numpy as np
from PIL import Image, ImageTk, ImageOps
import cv2
import threading
from ModelImage import ModelImage


class ModelVideo(ModelImage):
    
    def __init__(self, output_path, ImageType='Video'):

        super().__init__(output_path, ImageType)
 
        self.cap            = None
        self.play_status    = False
        self.cur_frame      = 0
        self.lock           = threading.Lock()
        self.video_img      = None
        self.interval_limit = 23

    
    # Video(Private)
    def edit_image_proc(self, np_img, command, args={}):        
        
        if 'flip-1' in command: # U/L
            np_img = np.flip(np_img, axis=0)
            
        elif 'flip-2' in command: # L/R
            np_img = np.flip(np_img, axis=1)

        elif 'rotate-' in command: # 1:rot90 2:rot180 3:rot270
            cmd = int(command.replace('rotate-', ''))
            np_img = np.rot90(np_img, cmd)
            
        elif command == 'clip_done':
            h, w = np_img[:,:,0].shape
            sy, sx, ch, cw = self.get_original_coords(h, w, args)
            np_img = np_img[sy:sy+ch, sx:sx+cw,:]
            self.edit_args = (sy, sx, ch, cw)         
        
        elif command == 'clip_save':
            sy, sx, ch, cw = self.edit_args
            np_img = np_img[sy:sy+ch, sx:sx+cw,:]
            
        return np_img
    

    def get_cur_time(self, sec):
        
        seconds  = int(sec)
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return h, m, s
    
    
    def draw_video(self, canvas, target_img, canvas_tag):
        
        img_conv                  = cv2.cvtColor(target_img, cv2.COLOR_BGR2RGB)
        self.img_conv             = Image.fromarray(img_conv)
        pil_img_pad               = ImageOps.pad(self.img_conv, (self.canvas_w, self.canvas_h))
        self.tk_video[canvas_tag] = ImageTk.PhotoImage(image=pil_img_pad)

        self.delete_video(canvas, canvas_tag)
        canvas.create_image(self.canvas_w/2, self.canvas_h/2, image=self.tk_video[canvas_tag], tag=canvas_tag)
    
        
    def delete_video(self, canvas, canvas_tag):
        
        if canvas.gettags(canvas_tag):
            canvas.delete(canvas_tag)

    
    def loop_video(self, loop=True):
        
        if loop and self.ret:
            self.vid = self.canvas_video.after(self.interval, self.loop_video)

        self.ret, self.video_img = self.cap.read()
        if self.ret:
            self.draw_video(self.canvas_video, self.video_img, self.canvas_tag)
            self.play_status = True
            self.cur_frame += 1
            h,m,s = self.get_cur_time(self.cur_frame/self.fps)
            self.cb_playing(self.play_status, self.frame_num, self.cur_frame, h,m,s, self.canvas_tag)

        else:
            self.cur_frame = 0
            self.play_status = False
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.cur_frame)
            h,m,s = self.get_cur_time(self.cur_frame/self.fps)
            self.cb_playing(self.play_status, self.frame_num, self.cur_frame, h,m,s, self.canvas_tag)
        
        return self.ret
    
    
    def set_interval(self, speed):
        
        with self.lock:
            self.interval = int(self.base_tick*speed)
            if self.interval < self.interval_limit:
                self.interval = self.interval_limit

    
    def save_capture(self):
        
        name, ext = os.path.splitext(self.file_name)
        file_path = '{}/{}_{:05}.png'.format(self.output_path, name, self.cur_frame)        
        self.img_conv.save(file_path)
        print("Saved: {}".format(file_path))
        
    
    def edit_video(self, frame, command_list, args):
        
        edit_np_video = frame.copy()
        for cmd in command_list:
            edit_np_video = self.edit_image_proc(edit_np_video, cmd, args=args)
            
        return edit_np_video
    
    
    def is_equel(self, cmd, last_cmd):
        
        result = False
        for k_cmd in ['rotate-', 'flip-1', 'flip-2', 'clip_']:
            if k_cmd in cmd:
                if k_cmd in last_cmd:
                    result = True
                    break
            
        return result
    
    
    def get_cmd_keyval(self, cmd):
        
        key = 'None'
        for k_cmd in ['rotate', 'flip-1', 'flip-2', 'clip']:
            if k_cmd in cmd:
                key = k_cmd
                break                
        
        val = 1
        if 'rotate-' in cmd:
            val = int(cmd.replace('rotate-',''))
            
        return key, val
    
    
    def get_cmdpack(self, cmd_dict, cmd):
        
        flip_UB_keys = ['None', 'flip-1']
        flip_LR_keys = ['None', 'flip-2']
        ROT_keys     = ['None', 'rotate-1', 'rotate-2', 'rotate-3']
        
        cmd_pack = cmd
        for ks, val in cmd_dict.items():
            if ks == 'rotate':
                idx = val % len(ROT_keys)
                cmd_pack = ROT_keys[idx]
            elif ks == 'flip-1':
                idx = val % len(flip_UB_keys)
                cmd_pack = flip_UB_keys[idx]
            elif ks == 'flip-2':
                idx = val % len(flip_LR_keys) 
                cmd_pack = flip_LR_keys[idx]
            elif ks == 'clip':
                cmd_pack = 'clip_save'
            
        return cmd_pack
    
        
    def create_command_list(self):

        cont_dict         = {}
        edit_command_list = []
        self.all_command_list.append('None')
        
        for idx, cmd in enumerate(self.all_command_list):
            
            if idx == 0:
                ks_cmd, val = self.get_cmd_keyval(cmd)
                cont_dict[ks_cmd] = val
                last_cmd = cmd
                
            else:
                
                if self.is_equel(cmd, last_cmd):                  
                    ks_cmd, val = self.get_cmd_keyval(cmd)
                    cont_dict[ks_cmd] += val
                    last_cmd = cmd
                    
                else:           
                    pack_cmd = self.get_cmdpack(cont_dict, cmd)
                    edit_command_list.append(pack_cmd)
                    cont_dict = {}
                    ks_cmd, val = self.get_cmd_keyval(cmd)
                    cont_dict[ks_cmd] = val
                    last_cmd = cmd
       
        self.edit_command_list = [cmd for cmd in edit_command_list if cmd != 'None']
    
        
    def clear_command_list(self):
    
        self.edit_command_list = []
        self.all_command_list  = []
        
    
    # Video(Public)
    def Set(self, fname, canvas, canvas_tag, callbacks):
        
        result = False
        print('Video/Set')
        if self.cap != None:
            self.cap.release()
        # 動画再生初期設定
        self.file_name  = os.path.basename(fname)
        self.cap        = cv2.VideoCapture(fname)
        self.frame_num  = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps        = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.base_tick  = 1000/self.fps
        self.cur_frame  = 0
        speed           = 1.0
        self.set_interval(speed)
        print(fname, self.frame_num, self.fps, int(self.base_tick), self.interval)
        # 内部変数初期化
        self.canvas_video        = canvas
        self.canvas_tag          = canvas_tag
        self.tk_video            = {}
        self.video_edit_imgs     = {'Video1':0, 'Video2':0}
        self.clear_command_list()
        # コールバック関数設定
        self.cb_playing          = callbacks[0]
        self.cb_playing(False, 0,0, 0,0,0, self.canvas_tag)
        self.cb_saving           = callbacks[1]
        
        self.ret, self.video_img = self.cap.read()
        if self.ret:
            self.set_image_layout(self.canvas_video, self.video_img)
            self.draw_video(self.canvas_video, self.video_img, self.canvas_tag)
            self.cur_frame += 1
            self.edit_h     = self.h
            self.edit_w     = self.w
            result          = True
            
        return result
            
            
    def GetInfo(self, command):
            
        if command == 'status': 
            info1, info2 = self.play_status, self.cur_frame
        elif command == 'property':
            info1, info2 = self.frame_num, self.fps
        elif command == 'frame':
            info1, info2 = self.frame_num, self.cur_frame
            
        return info1, info2
        
    
    def Ctrl(self, canvas, canvas_tag, command, args=None):
        
        res = True
        self.canvas_video = canvas
        self.canvas_tag   = canvas_tag
        
        if command == 'play':
            res = self.loop_video()
            print('Video/', command, self.play_status)
                    
        elif command == 'step':
            self.loop_video(loop=False)
            
        elif command == 'stop':
            print('Video/', command, self.vid)
            self.canvas_video.after_cancel(self.vid)
            self.play_status = False
        
        elif 'setpos' in command:
            num = command.replace('setpos-','')
            with self.lock:                
                self.cur_frame = int(self.frame_num*(int(num)/100))
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.cur_frame)
            print('Video/', command, self.cur_frame, num)
            
        elif 'speed' in command:
            speed = float(command.replace('speed-x',''))
            self.set_interval(1/speed)
            print('Video/', command, speed, self.interval)
            
        elif command == 'capture':
           self.save_capture()
           print('Video/', command)
           
        elif command == 'drop':
            print('Video/', command, self.sid)
            self.canvas_video.after_cancel(self.sid)
            self.save_status = False
            self.complete_video_record()
            self.clear_video_record()
            self.clear_command_list()
            self.cb_saving(self.save_status, self.save_num, self.edit_num)
            
        else:
            print('Video/None')
            
        return res


    def Edit(self, canvas, canvas_tag, command, edit_frame, args=None, update=False):
        
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, edit_frame)
        ret, frame = self.cap.read()
        if ret:           

            if command != 'Undo':
    
                if np.sum(self.video_edit_imgs[canvas_tag]) != 0:
                    edit_img = self.video_edit_imgs[canvas_tag]
                else:
                    edit_img = frame
           
                edit_img = self.edit_video(edit_img, [command], args)
                self.draw_video(canvas, edit_img, canvas_tag)
                self.video_edit_imgs[canvas_tag] = edit_img
        
                if update:
                    self.set_image_layout(canvas, edit_img)
                    self.edit_h, self.edit_w, _ = edit_img.shape
                    self.all_command_list.append(command)
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.cur_frame)
                    
            else: # Undo
                self.draw_video(canvas, frame, canvas_tag)
                self.set_image_layout(canvas, frame)
                self.video_edit_imgs[canvas_tag] = 0
                self.pil_img                     = None
                self.all_command_list            = []
                
        else:
            print('cap_read:', ret)
                    

    def Save(self, fname, frame_1, frame_2, save_args):          
        # Set frames to save
        fno_sp = min(frame_1, frame_2)
        fno_ep = max(frame_1, frame_2)
        if fno_sp == fno_ep:
            fno_ep += 1
        
        self.cap_save = cv2.VideoCapture(fname)
        self.cap_save.set(cv2.CAP_PROP_POS_FRAMES, fno_sp)
        self.edit_num = fno_ep - fno_sp
        self.save_num = 0
        print(f'fno_sp:{fno_sp} fno_ep:{fno_ep} save_num:{self.save_num}')

        # Create file_path
        name, ext = os.path.splitext(fname)
        self.file_path = '{}_frame{}_{}.{}'.format(name, fno_sp, fno_ep, save_args[0])
        # Create edit commands(Minimal)
        self.create_command_list()
        # Pre-Process for save video
        self.save_ftype = save_args[0]
        self.prepare_video_record(save_args)
            
        self.save_status = True
        # start to record video
        self.loop_video_record()
    
    
    def loop_video_record(self):
        
        if self.save_num < self.edit_num:
            ret, frame = self.cap_save.read()
            if ret:
                # Edit frame
                edit_img = self.edit_video(frame, self.edit_command_list, None)
                # Write 1frame
                self.write_video_frame(edit_img)
                # View callback
                self.cb_saving(self.save_status, self.save_num, self.edit_num)
                # update save frame
                self.save_num += 1
                
                if self.save_status:
                    # start loop_video_record
                    self.sid = self.canvas_video.after(10, self.loop_video_record)
        else:
            # Complete saving
            self.complete_video_record()
            self.clear_video_record()
            self.clear_command_list()
            self.save_status = False
            # View callback
            self.cb_saving(self.save_status, self.save_num, self.edit_num)


    def prepare_video_record(self, save_args):

        if self.save_ftype == 'mp4':
            # Open Video Writer
            video_format = cv2.VideoWriter_fourcc(*'mp4v') 
            self.video   = cv2.VideoWriter(self.file_path, video_format, self.fps, (self.edit_w, self.edit_h))


    def write_video_frame(self, img_cnv):
       
        if self.save_ftype == 'mp4':
            self.video.write(img_cnv)


    def complete_video_record(self):

        if self.save_ftype == 'mp4':
            self.video.release()
            
            if self.save_status:
                print("Saved: {}".format(self.file_path))
            else:
                # remove file if to drop
                os.remove(self.file_path)
    

    def clear_video_record(self):
        
        if self.cap_save != None:
            self.cap_save.release()
            self.cap_save = None

