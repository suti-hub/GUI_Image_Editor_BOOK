# -*- coding: utf-8 -*-
import os
import numpy as np
from datetime import datetime
from PIL import Image, ImageTk, ImageOps
from ModelImage import ModelImage

class ModelPhoto(ModelImage):
    
    def __init__(self, output_path, ImageType='Photo'):

        super().__init__(output_path, ImageType)

        self.edit_img       = None
        self.original_img   = None


    # Common(Private)       
    def edit_image_command(self, orginal_image, edit_image, command, args={}):
        
        if edit_image != None:
            img = edit_image
        else:
            img = orginal_image.copy()
        
        np_img = np.array(img)
        np_img = self.edit_image_proc(np_img, command, args=args)
        
        return Image.fromarray(np_img)
       
            
    # Photo(Public)     
    def Draw(self, file_path, canvas, command, args={}):
        
        if canvas.gettags('Photo'):
            canvas.delete('Photo')
            
        if self.edit_img != None and command != 'None':
            img               = self.edit_img
            
        else:
            img               = Image.open(file_path)
            self.original_img = img
            self.edit_img     = None
            self.set_image_layout(canvas, np.array(self.original_img))
        
        if command != 'None':
            img               = self.edit_image_command(self.original_img, self.edit_img, command, args=args)
            self.edit_img     = img
            self.set_image_layout(canvas, np.array(self.edit_img))

        pil_img     = ImageOps.pad(img, (self.canvas_w, self.canvas_h))
        self.tk_img = ImageTk.PhotoImage(image=pil_img)
        canvas.create_image(self.canvas_w/2, self.canvas_h/2, image=self.tk_img, tag='Photo')
    
    
    def Save(self, file_path):
        
        if self.edit_img != None:
            name, ext   = os.path.splitext(file_path)
            dt          = datetime.now()
            file_name   = os.path.basename(name) + '_' + dt.strftime('%H%M%S') + '.png'
            file_path   = os.path.join(self.output_path, file_name)

            self.edit_img.save(file_path)
            print("Saved: {}".format(file_path))
            
    