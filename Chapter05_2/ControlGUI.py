# -*- coding: utf-8 -*-
import os
import json
from ModelPhoto import ModelPhoto
from ModelVideo import ModelVideo

class ControlGUI():
    
    def __init__(self, default_path):

        self.dir_path      = {'Photo':default_path, 'Video':default_path}
        self.ext_keys      = {'Photo':['.png', '.jpg', '.jpeg', '.JPG', '.PNG'], 'Video':['.mp4']}
        self.target_files  = {'Photo':[],  'Video':[]}
        self.model         = {}
        self.file_pos      = {'Photo':0,   'Video':0}
        self.speed_val     = 1
        
        self.clip_sx       = 0
        self.clip_sy       = 0
        self.clip_ex       = 0
        self.clip_ey       = 0
        self.canvas        = {}
        self.frame         = {}
        self.json_cfg_path = './last_setting.json'
        
        self.output_path = os.path.join('./','output')
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
            
        # Model Class生成
        self.model['Photo'] = ModelPhoto(self.output_path)
        self.model['Video'] = ModelVideo(self.output_path)
                
        
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

        # コマンド：(有効/無効, 遷移先)
        stm_video = {
            'IDLE':
            {'dir':(True,'SET'),    'set':(False,'IDLE'),   'play':(False,'IDLE'),  'stop':(False,'IDLE'),
             'step':(False,'IDLE'), 'speed':(False,'IDLE'), 'cap':(False,'IDLE'),   'edit':(False,'IDLE'),
             'clip':(False,'IDLE'), 'rect':(False,'IDLE'),  'done':(False,'IDLE'),  'dclick':(False,'IDLE'),
             'undo':(False,'IDLE'), 'bar':(False,'IDLE'),   'save':(False,'IDLE'),  'drop':(False,'IDLE')},
            'SET':
            {'dir':(True,'SET'),    'set':(True,'STOP'),    'play':(False,'SET'),   'stop':(False,'SET'),
             'step':(False,'SET'),  'speed':(False,'SET'),  'cap':(False,'SET'),    'edit':(False,'SET'),
             'clip':(False,'SET'),  'rect':(False,'SET'),   'done':(False,'SET'),   'dclick':(False,'SET'),
             'undo':(False,'SET'),  'bar':(False,'SET'),    'save':(False,'SET'),   'drop':(False,'SET')}, 
            'STOP':    
            {'dir':(True,'SET'),    'set':(True,'STOP'),    'play':(True,'PLAY'),   'stop':(False,'STOP'),
             'step':(True,'STOP'),  'speed':(True,'STOP'),  'cap':(True,'STOP'),    'edit':(True,'EDIT'),
             'clip':(True,'ECLIP'), 'rect':(False,'STOP'),  'done':(False,'STOP'),  'dclick':(True,'STOP'),
             'undo':(True,'STOP'),  'bar':(True,'STOP'),    'save':(True,'RECO'),   'drop':(False,'STOP')},   
            'PLAY':    
            {'dir':(False,'PLAY'),  'set':(False,'PLAY'),   'play':(False,'PLAY'),  'stop':(True,'STOP'),
             'step':(False,'PLAY'), 'speed':(True,'PLAY'),  'cap':(False,'PLAY'),   'edit':(False,'PLAY'),
             'clip':(False,'PLAY'), 'rect':(False,'PLAY'),  'done':(False,'PLAY'),  'dclick':(False,'PLAY'),
             'undo':(False,'PLAY'), 'bar':(True,'PLAY'),    'save':(False,'PLAY'),  'drop':(False,'PLAY')},
            'EDIT':    
            {'dir':(False,'EDIT'),  'set':(False,'EDIT'),   'play':(False,'EDIT'),  'stop':(False,'EDIT'),
             'step':(False,'EDIT'), 'speed':(False,'EDIT'), 'cap':(True,'EDIT'),    'edit':(True,'EDIT'),
             'clip':(True,'ECLIP'), 'rect':(False,'EDIT'),  'done':(False,'EDIT'),  'dclick':(False,'EDIT'),
             'undo':(True,'STOP'),  'bar':(False,'EDIT'),   'save':(True,'RECO'),   'drop':(False,'EDIT')},   
            'ECLIP':    
            {'dir':(False,'ECLIP'), 'set':(False,'ECLIP'),  'play':(False,'ECLIP'), 'stop':(False,'ECLIP'),
             'step':(False,'ECLIP'),'speed':(False,'ECLIP'),'cap':(True,'ECLIP'),   'edit':(False,'ECLIP'),
             'clip':(True,'ECLIP'), 'rect':(True,'ECLIP'),  'done':(True,'ELOCK'),  'dclick':(False,'ECLIP'),
             'undo':(True,'STOP'),  'bar':(False,'ECLIP'),  'save':(True,'RECO'),   'drop':(False,'ECLIP')},    
            'ELOCK':    
            {'dir':(False,'ELOCK'), 'set':(False,'ELOCK'),  'play':(False,'ELOCK'), 'stop':(False,'ELOCK'),
             'step':(False,'ELOCK'),'speed':(False,'ELOCK'),'cap':(True,'ELOCK'),   'edit':(False,'ELOCK'),
             'clip':(False,'ELOCK'),'rect':(False,'ELOCK'), 'done':(False,'ELOCK'), 'dclick':(False,'ELOCK'),
             'undo':(True,'STOP'),  'bar':(False,'ELOCK'),  'save':(True,'RECO'),   'drop':(False,'ELOCK')},
            'RECO':    
            {'dir':(False,'RECO'),  'set':(False,'RECO'),   'play':(False,'RECO'),  'stop':(False,'RECO'),
             'step':(False,'RECO'), 'speed':(False,'RECO'), 'cap':(False,'RECO'),   'edit':(False,'RECO'),
             'clip':(False,'RECO'), 'rect':(False,'RECO'),  'done':(False,'RECO'),  'dclick':(False,'RECO'),
             'undo':(False,'RECO'), 'bar':(False,'RECO'),   'save':(False,'RECO'),  'drop':(True,'STOP')},
        }

        # State Machine table
        self.state_machine = {'Photo':stm_photo, 'Video':stm_video}

        # Current State
        self.cur_state     = {'Photo':'IDLE', 'Video':'IDLE'}
          

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
            
        else: # 'Video'
            self.model['Video'].DrawRectangle(self.canvas['Video1'], self.clip_sy, self.clip_sx, self.clip_ey, self.clip_ex)
            self.model['Video'].DrawRectangle(self.canvas['Video2'], self.clip_sy, self.clip_sx, self.clip_ey, self.clip_ex)

    
    def Set(self, set_pos, callbacks):
        
        tab = self.select_tab
        file_path = self.get_file('set', set_pos)
        
        if tab == 'Photo':
            if file_path != None:
                self.model['Photo'].DeleteRectangle(self.canvas['Photo'])
                self.model['Photo'].Draw(file_path, self.canvas['Photo'], 'None')
            
        else: # 'Video'
            if file_path != None:
                self.model['Video'].DeleteRectangle(self.canvas['Video1'])
                self.model['Video'].DeleteRectangle(self.canvas['Video2'])
                self.video_tag = 'Video1'
                
                self.model['Video'].Set(file_path, self.canvas[self.video_tag], self.video_tag, callbacks)
                _, self.frame['Video1'] = self.model['Video'].GetInfo('status')
                _, self.frame['Video2'] = self.model['Video'].GetInfo('status')   
                print('tag, fno1, fno2',self.video_tag, self.frame['Video1'], self.frame['Video2'])
            
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
            
        else: # 'Video'
            self.play_status, self.frame[self.video_tag] = self.model['Video'].GetInfo('status')
            print('tag, fno1, fno2',self.video_tag, self.frame['Video1'], self.frame['Video2'])
            self.model['Video'].Edit(self.canvas['Video1'], 'Video1', command, self.frame['Video1'], args=args, update=False)
            self.model['Video'].Edit(self.canvas['Video2'], 'Video2', command, self.frame['Video2'], args=args, update=True)

        
    def Save(self, args=None):
        
        tab = self.select_tab
        if tab == 'Photo':        
            file_path = self.get_file('current')
            self.model['Photo'].Save(file_path)
            
        else: # 'Video'
            _, self.frame[self.video_tag] = self.model['Video'].GetInfo('status')
            file_path = self.get_file('current')
            self.model['Video'].Save(file_path, self.frame['Video1'], self.frame['Video2'], args)
            print('tag, fno1, fno2',self.video_tag, self.frame['Video1'], self.frame['Video2'])
  
    
    def ClearCanvas(self):

        self.model['Video'].Edit(self.canvas['Video1'], 'Video1', 'Undo', self.frame['Video1'])
        self.model['Video'].Edit(self.canvas['Video2'], 'Video2', 'Undo', self.frame['Video2'])
        self.model['Video'].DeleteRectangle(self.canvas['Video1'])
        self.model['Video'].DeleteRectangle(self.canvas['Video2'])

            
    def Undo(self, command):
        
        tab = self.select_tab
        if tab == 'Photo':
            file_path = self.get_file('current')
            self.model['Photo'].DeleteRectangle(self.canvas['Photo'])
            self.model['Photo'].Draw(file_path, self.canvas['Photo'], command)
            
        else: # 'Video'
            _, self.frame[self.video_tag] = self.model['Video'].GetInfo('status')
            print('tag, fno1, fno2',self.video_tag, self.frame['Video1'], self.frame['Video2'])
            self.ClearCanvas()


    # Photo(Public)
    def DrawPhoto(self, command, set_pos=-1):
                
        file_path = self.get_file(command, set_pos)
        self.model['Photo'].Draw(file_path, self.canvas['Photo'], 'None')

        
    # Video(Public)
    def InitSpeed(self, speed_text):
        
        self.speed_val = 1
        return speed_text[self.speed_val]    
    
    
    def UpSpeed(self, speed_text):     
        
        self.speed_val += 1
        if self.speed_val >= len(speed_text):
            self.speed_val = 0
        return speed_text[self.speed_val]
    
    
    def SetCanvas(self, select_canvas):

        self.video_tag  = select_canvas
        self.play_status, self.frame['Video1'] = self.model['Video'].GetInfo('status')
        self.play_status, self.frame['Video2'] = self.model['Video'].GetInfo('status')
        print('canvas->{}, play_status:{}, frame:{}'.format(select_canvas, self.play_status, self.frame[select_canvas]))          
            
    
    def GetVideo(self, command):
        return self.model['Video'].GetInfo(command)       
            
            
    def Video(self, command, set_pos=-1):
        # play/stop/setpos/speed/drop
        res = self.model['Video'].Ctrl(self.canvas[self.video_tag], self.video_tag, command)
        return res
    

    def SaveConfig(self):

        cfg = {}
        cfg['dir_photo']  = self.dir_path['Photo']
        cfg['dir_video']  = self.dir_path['Video']
        cfg['select_tab'] = f'[{self.select_tab}]'
        
        with open(self.json_cfg_path, 'w') as f:
            json.dump(cfg, f, indent=4)
            print('Save setting to', self.json_cfg_path)
    

    def LoadConfig(self):

        cfg = None
        if os.path.isfile(self.json_cfg_path):
            with open(self.json_cfg_path, 'r') as f:
                cfg = json.load(f)
                self.dir_path['Photo'] = cfg['dir_photo']
                self.dir_path['Video'] = cfg['dir_video']
                print('Load setting from ', self.json_cfg_path)
                
        return cfg
