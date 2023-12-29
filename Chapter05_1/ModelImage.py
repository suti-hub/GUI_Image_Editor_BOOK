# -*- coding: utf-8 -*-
import numpy as np

class ModelImage():
    
    def __init__(self, output_path, ImageType):
         
        self.ImageType   = ImageType
        self.canvas_w    = 0
        self.canvas_h    = 0
        self.output_path = output_path
       
    # Common(Private)
    def set_image_layout(self, canvas, image):
        
        self.canvas_w  = canvas.winfo_width()
        self.canvas_h  = canvas.winfo_height()
        self.rate_wh   = self.canvas_w/self.canvas_h
        
        h, w, ch       = image.shape
        rate_wh        = w / h
        self.h, self.w = h, w
        if rate_wh < self.rate_wh:
            self.resize_h = self.canvas_h
            self.resize_w = int(w * (self.canvas_h/h))
            self.pad_x = (self.canvas_w - self.resize_w) // 2
            self.pad_y = 0
            
        else:
            self.resize_w = self.canvas_w
            self.resize_h = int(h * (self.canvas_w/w))
            self.pad_y = (self.canvas_h - self.resize_h) // 2
            self.pad_x = 0
        
        
    def get_correct_values(self, rate, sy, sx, ey, ex):

        mod_sx = int(min(sx, ex)*rate)
        mod_sy = int(min(sy, ey)*rate)
        mod_ex = int(max(sx, ex)*rate)
        mod_ey = int(max(sy, ey)*rate)
        ch, cw = mod_ey - mod_sy, mod_ex - mod_sx

        return mod_sy, mod_sx, ch, cw

    
    def get_original_coords(self, h, w, args):
        
        sy, sx, ey, ex = args['sy'], args['sx'], args['ey'], args['ex']
        rate_wh = w / h
        
        if rate_wh < self.rate_wh:
            rate  = h/self.canvas_h
            x_spc = self.pad_x*rate
            sy, sx, ch, cw = self.get_correct_values(rate, sy, sx, ey, ex)
            sx = sx - x_spc
            sx = int(max(sx, 0))
            sx = int(min(sx, w))
            
        else:
            rate  = w/self.canvas_w
            y_spc = self.pad_y*rate
            sy, sx, ch, cw = self.get_correct_values(rate, sy, sx, ey, ex)        
            sy = sy - y_spc
            sy = int(max(sy, 0))
            sy = int(min(sy, h))

        return sy, sx, ch, cw
    
    
    def edit_image_proc(self, np_img, command, args={}):        
        
        if 'flip-1' in command: # U/L
            np_img = np.flip(np_img, axis=0)
            
        elif 'flip-2' in command: # L/R
            np_img = np.flip(np_img, axis=1)

        elif 'rotate-' in command: # 1:rot90 2:rot180 3:rot270
            cmd    = int(command.replace('rotate-', ''))
            np_img = np.rot90(np_img, cmd)
            
        elif command == 'clip_done':
            h, w   = np_img[:,:,0].shape
            sy, sx, ch, cw = self.get_original_coords(h, w, args)
            np_img = np_img[sy:sy+ch, sx:sx+cw,:]
            
        return np_img
    

    # Common(Public) 
    def GetValidPos(self, pos_y, pos_x):
        
        rate_wh = self.resize_w / self.resize_h
        
        if rate_wh < self.rate_wh:
            valid_pos_y = pos_y
            valid_pos_x = max(pos_x, self.pad_x)
            valid_pos_x = min(valid_pos_x, self.canvas_w - self.pad_x)
            
        else:
            valid_pos_x = pos_x
            valid_pos_y = max((pos_y, self.pad_y))
            valid_pos_y = min(valid_pos_y, self.canvas_h - self.pad_y)

        return valid_pos_y, valid_pos_x
  
   
    def DrawRectangle(self, canvas, clip_sy, clip_sx, clip_ey, clip_ex, tag='clip_rect', color='red'):
        
        if canvas.gettags(tag):
            canvas.delete(tag)
            
        canvas.create_rectangle(clip_sx, clip_sy, clip_ex, clip_ey, outline=color, tag=tag)
        
    
    def DeleteRectangle(self, canvas, tag='clip_rect'):
        
        if canvas.gettags(tag):
            canvas.delete(tag)
            
    