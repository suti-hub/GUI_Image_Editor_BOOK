# -*- coding: utf-8 -*-

import os
from ControlGUI import ControlGUI
import pytest
import os

def test_get_file():
    
    cur_path = os.getcwd()
    obj      = ControlGUI('')
    obj.dir_path['Photo'] = f'{cur_path}/test_dir'
    # file list取得（txtのみ）
    file_list = os.listdir(obj.dir_path['Photo'])
    file_list        = [name for name in file_list if '.txt' in name]
    # テスト条件（初期化）
    obj.select_tab   = 'Photo'
    obj.target_files = {'Photo': file_list}
    obj.file_pos     = {'Photo': 0} 
    
    print('---- [file_list]------')
    for idx, fn in enumerate(file_list):
        print(idx, fn)
    
    num = len(file_list)
    print('------ [curent command test] ------')
    # curent pos
    cur_idx = obj.file_pos['Photo']
    assert obj.get_file('current') == os.path.join(obj.dir_path['Photo'], file_list[cur_idx])
    
    print('------ [set command test] ------')
    # set file pos
    for idx in range(num):
        assert obj.get_file('set', idx) == os.path.join(obj.dir_path['Photo'], file_list[idx])
    
    print('------ [curent command test] ------')
    # curent pos
    cur_idx = obj.file_pos['Photo']
    assert obj.get_file('current') == os.path.join(obj.dir_path['Photo'], file_list[cur_idx])
    
    print('------ [next command test] ------')
    # next pos idx => idx: 0 ~ max_num-1
    for idx in range(num):
        assert obj.get_file('next') == os.path.join(obj.dir_path['Photo'], file_list[idx])  
    
    print('------ [curent command test] ------')
    # curent pos
    cur_idx = obj.file_pos['Photo']
    assert obj.get_file('current') == os.path.join(obj.dir_path['Photo'], file_list[cur_idx])

    print('------ [prev command test] ------')
    # prev pos idx
    for idx in [3,2,1,0,4]:
        assert obj.get_file('prev') == os.path.join(obj.dir_path['Photo'], file_list[idx])
    
    print('------ [curent command test] ------')
    # curent pos
    cur_idx = obj.file_pos['Photo']
    assert obj.get_file('current') == os.path.join(obj.dir_path['Photo'], file_list[cur_idx])
    
    print('------ [file_list num ==0 test] ------')
    # テスト条件（初期化）　ファイルリストなし
    obj.target_files = {'Photo': []}
    obj.file_pos = {'Photo': 0} 
    # curent pos
    cur_idx = obj.file_pos['Photo']
    assert obj.get_file('current') == None

# test実行
test_get_file()