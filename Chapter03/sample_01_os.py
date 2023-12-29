# -*- coding: utf-8 -*-
import os

def check_path_print(check_path):
    
    if os.path.exists(check_path):
        print('指定したパスは存在します：', check_path)
    else:
        print('指定したパスは存在しません：', check_path)  

check_ext = '.png'
root_path = './TEST'
sub_dir1  = 'dir1'
sub_dir2  = 'dir2'
sub_dir3  = 'dir2/dir3'

# ディレクトリのパス確認
dir_path = os.path.join(root_path, sub_dir1)
check_path_print(dir_path)
# ディレクトリ作成
os.mkdir(dir_path)
print('mkdir:', dir_path)
check_path_print(dir_path)
# ディレクトリのパス確認
dir_path = os.path.join(root_path, sub_dir2)
check_path_print(dir_path)
# ディレクトリのパス確認
dir_path = os.path.join(root_path, sub_dir3)
check_path_print(dir_path)
# ディレクトリ作成
os.makedirs(dir_path)
print('makedirs:', dir_path)
check_path_print(dir_path)

# ファイルの作成
for i in range(3):

    file_path_txt = os.path.join(dir_path, f'test0{i}.txt')
    with open(file_path_txt, 'w') as f:
        f.write(f'This is test0{i}.txt')
    print('Created:', os.path.basename(file_path_txt))
        
    file_path_png = os.path.join(dir_path, f'img0{i}.png')
    with open(file_path_png, 'w') as f:
        f.write(f'This is img0{i}.png')
    print('Created:', os.path.basename(file_path_png))

# ディレクトリ内のpngファイルの表示
file_list = os.listdir(dir_path)
for filename in file_list:
    
    name, ext = os.path.splitext(filename)
    if check_ext == ext:
        print(f'name:{name}, ext:{ext}')

