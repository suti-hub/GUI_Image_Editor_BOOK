# -*- coding: utf-8 -*-
import os
from ModelImage import ModelImage

class ControlGUI():
    
    def __init__(self, default_path):

        self.dir_path      = {'Photo':default_path}
        self.ext_keys      = {'Photo':['.png', '.jpg', '.jpeg', '.JPG', '.PNG']}
        self.target_files  = {'Photo':[]}
        self.model         = {}
        self.file_pos      = {'Photo':0}
        
        self.clip_sx       = 0
        self.clip_sy       = 0
        self.clip_ex       = 0
        self.clip_ey       = 0
        self.canvas        = {}
        
        self.output_path = os.path.join('./','output')
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
            
        # Model Class生成
        self.model['Photo'] = ModelImage(self.output_path)
                
        
    # Common(Private)
    def is_target(self, name, key_list):
        
        valid = False
        for ks in key_list:
            if ks in name:
                valid = True
        
        return valid
    
    
    def get_file(self, command, set_pos=-1):
        
        tab = self.select_tab
        num = len(self.target_files[tab])
                
        if num == 0:
            print('No files..to support')
            return None
        
        if command == 'prev':
            self.file_pos[tab] -= 1
            if self.file_pos[tab] < 0:
                self.file_pos[tab] = num -1
            
        elif command == 'next':
            self.file_pos[tab] += 1
            if self.file_pos[tab] >= num:
                self.file_pos[tab] = 0
            
        elif command == 'set':
            self.file_pos[tab] = set_pos
            
        # command == 'curent'
        cur_pos = self.file_pos[tab]
            
        file_path = os.path.join(self.dir_path[tab], self.target_files[tab][cur_pos])
        print('{}/{} {} '.format(cur_pos, num-1, file_path))

        return file_path
    
    # Common(Public)
    def InitCanvas(self, window_canvas_dict):
        
        for ks, canvas in window_canvas_dict.items():      
            self.canvas[ks] = canvas
        
        
    def SetTab(self, select_tab):
        
        self.select_tab = select_tab.replace('[','').replace(']','')
        print(f'tab-control:{self.select_tab}')
        
    
    def InitStateMachine(self):

        # コマンド：(有効/無効, 遷移先)
        stm_photo = {
            'IDLE':
            {'dir':(True,'SET'),    'set':(False,'IDLE'),   'prev':(False,'IDLE'),  'next':(False,'IDLE'),
             'edit':(False,'IDLE'), 'clip':(False,'IDLE'),  'rect':(False,'IDLE'),  'done':(False,'IDLE'),
             'undo':(False,'IDLE'), 'save':(False,'IDLE')},
            'SET':  
            {'dir':(True,'SET'),    'set':(True,'SET'),     'prev':(True,'SET'),    'next':(True,'SET'),
             'edit':(True,'EDIT'),  'clip':(True,'ECLIP'),  'rect':(False,'SET'),   'done':(False,'SET'),
             'undo':(False,'SET'),  'save':(False,'SET')},
            'EDIT':  
            {'dir':(False,'EDIT'),  'set':(True,'SET'),     'prev':(True,'SET'),    'next':(True,'SET'),
             'edit':(True,'EDIT'),  'clip':(True,'ECLIP'),  'rect':(False,'EDIT'),  'done':(False,'EDIT'),
             'undo':(True,'SET'),   'save':(True,'SET')}, 
            'ECLIP': 
            {'dir':(False,'EDIT'),  'set':(True,'SET'),     'prev':(True,'SET'),    'next':(True,'SET'),
             'edit':(True,'ECLIP'), 'clip':(True,'ECLIP'),  'rect':(True,'ECLIP'),  'done':(True,'EDIT'),
             'undo':(True,'SET'),   'save':(True,'SET')}, 
        }

        # State Machine table
        self.state_machine = {'Photo':stm_photo}

        # Current State
        self.cur_state     = {'Photo':'IDLE'}
          

    def IsTransferToState(self, command):
       
        tab = self.select_tab
        cur_state = self.cur_state[tab]
        is_valid, next_state = self.state_machine[tab][cur_state][command]
        #print('state_change:{}, {}->{} @ {}'.format(is_valid, cur_state, next_state, command))
        self.cur_state[tab] = next_state
        return is_valid  
    
    
    def ForceToState(self, next_state):
        
        tab = self.select_tab
        self.cur_state[tab] = next_state


    def GetCurrentState(self):
        
        tab = self.select_tab
        return self.cur_state[tab]
    
    
    def GetDirPath(self):
        
        tab = self.select_tab
        return self.dir_path[tab]


    def SetFileList(self, dir_path):
        
        tab = self.select_tab
        
        file_list = os.listdir(dir_path)
        target_ext = self.ext_keys[tab]
        print(tab, target_ext)
        
        target_files = []
        for file_name in file_list:
            if self.is_target(file_name, target_ext):
                target_files.append(file_name)        
        
        self.dir_path[tab]     = dir_path
        self.target_files[tab] = target_files

        return self.target_files[tab]


    def GetCurrentFile(self):
        
        file_path = self.get_file('current')
        if file_path != None:
            return os.path.basename(file_path)
        else:
            return 'None'
        
    
    def DrawRectangle(self, command, pos_y, pos_x):
                
        tab = self.select_tab
        if command   == 'clip_start':
            self.clip_sy, self.clip_sx = pos_y, pos_x
            self.clip_ey, self.clip_ex = pos_y+1, pos_x+1
            
        elif command == 'clip_keep':      
            self.clip_ey, self.clip_ex = pos_y, pos_x
            
        elif command == 'clip_end':
            self.clip_ey, self.clip_ex = pos_y, pos_x
            self.clip_sy, self.clip_sx = self.model[tab].GetValidPos(self.clip_sy, self.clip_sx)
            self.clip_ey, self.clip_ex = self.model[tab].GetValidPos(self.clip_ey, self.clip_ex)
            
        if tab == 'Photo':
            self.model['Photo'].DrawRectangle(self.canvas['Photo'],  self.clip_sy, self.clip_sx, self.clip_ey, self.clip_ex)
            
        
    def Set(self, set_pos, callbacks):
        
        tab = self.select_tab
        file_path = self.get_file('set', set_pos)
        
        if tab == 'Photo':
            if file_path != None:
                self.model['Photo'].DeleteRectangle(self.canvas['Photo'])
                self.model['Photo'].Draw(file_path, self.canvas['Photo'], 'None')
            
        return (file_path != None)
    
        
    def Edit(self, command):
                
        args = {}
        if command == 'clip_done':
            args['sx'], args['sy'] = self.clip_sx, self.clip_sy
            args['ex'], args['ey'] = self.clip_ex, self.clip_ey
        
        tab = self.select_tab
        if tab == 'Photo':                 
            file_path = self.get_file('current')
            self.model['Photo'].Draw(file_path, self.canvas['Photo'], command, args=args)
    
        
    def Save(self, args=None):
        
        tab = self.select_tab
        if tab == 'Photo':        
            file_path = self.get_file('current')
            self.model['Photo'].Save(file_path)

            
    def Undo(self, command):
        
        tab = self.select_tab
        if tab == 'Photo':
            file_path = self.get_file('current')
            self.model['Photo'].DeleteRectangle(self.canvas['Photo'])
            self.model['Photo'].Draw(file_path, self.canvas['Photo'], command)
    

    # Photo(Public)
    def DrawPhoto(self, command, set_pos=-1):
                
        file_path = self.get_file(command, set_pos)
        self.model['Photo'].Draw(file_path, self.canvas['Photo'], 'None')

