# -*- coding: utf-8 -*-

import os
from ControlGUI import ControlGUI

control = ControlGUI('')
control.InitStateMachine()

st_photo = ['IDLE','SET','EDIT','ECLIP']
        
cmd_list_photo = [
    'dir','set','prev','next','edit','clip',
    'rect','done','undo','save'
    ]

def test_state_machine(tab, state_list, cmd_list):
    
    control.SetTab(tab)
    for cur_state in state_list:
        print(f"'{cur_state}':")
        col_cnt = 0
        text_line = "{"
        for n, cmd in enumerate(cmd_list):
            control.ForceToState(cur_state)
            is_valid   = control.IsTransferToState(cmd)
            next_state = control.GetCurrentState()
            text_line += f"'{cmd}':({is_valid},'{next_state}'),\t"
            col_cnt += 1
            
            if n == len(cmd_list)-1:
                last_line = text_line[:-2] + '}'
                print(last_line)
                break
            
            if col_cnt == 4: 
                col_cnt = 0
                print(text_line)
                text_line = ' '

print('Test Start')

print('\n### Photo Test ###')   
test_state_machine('[Photo]', st_photo, cmd_list_photo)

print('\nTest End')
