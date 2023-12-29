# GUI_Image_Editor_BOOK
電子書籍「PythonでGUIを作りたい　仕様検討から実装まではじめての動画・静止画編集ソフト」  
ソースコード一式

---

### 1. 概要

#### Chapter01

1章　Python環境パッケージバージョン確認のサンプルコード


#### Chapter02

2章　簡易電卓アプリのサンプルコード、写真・動画のサンプル（TEST用）


#### Chapter03

3章　各種ライブラリのサンプルコード一式


#### Chapter04

4章　静止画編集ソフトのコード一式、テストコードのサンプル


#### Chapter05_1

5章　動画編集ソフトのコード一式（変更前）、テストコードのサンプル


#### Chapter05_2

5章　動画編集ソフトのコード一式（変更後）


### 2. フォルダ構成

```
GUI_Image_Editor_BOOK
    │  
    ├─Chapter01
    │      test_package_version.py
    │      
    ├─Chapter02
    │      sample_calculator.py
    │      
    ├─Chapter03
    │  │  sample_00_tkinter.py
    │  │  sample_01_os.py
    │  │  sample_02_pillow.py
    │  │  sample_03_numpy.py
    │  │  sample_04_opencv_playback.py
    │  │  sample_05_opencv_record.py
    │  │  sample_06_image_viewer.py
    │  │  sample_07_video_recorder.py
    │  │  
    │  └─TEST
    │          image_00.jpg
    │          image_00.png
    │          video_00.mp4
    │          
    ├─Chapter04
    │      ViewGUI.py
    │      ControlGUI.py
    │      ModelImage.py
    │      numpy_pillow_time.py
    │      pytest_get_file.py
    │      test_state_machine_01.py
    │      
    ├─Chapter05_1
    │      ViewGUI.py
    │      ControlGUI.py
    │      ModelImage.py
    │      ModelPhoto.py
    │      ModelVideo.py
    │      test_state_machine_02.py
    │      
    └─Chapter05_2
            ViewGUI.py
            ControlGUI.py
            ModelImage.py
            ModelPhoto.py
            ModelVideo.py
        
```

### 3. 評価環境

- OS：Windows 10  
- プログラム言語：Python 3.8.10  
- パッケージ管理：pip 23.1.2  
- プログラム実行・デバッグ環境：Spyder 4.1.5

---

### 4. 実行方法

#### Spyder
1. Open  [Pythonファイル]

2. Run

#### Command line
1. cd [目的のフォルダ]

2. python [Pythonファイル]

---
