
import tkinter as tk
from tkinter import ttk

#　ルートウィンドウ生成
root_window = tk.Tk()
#　ルートウィンドウ サイズ指定
root_window.geometry("300x200")
#　ルートウィンドウ タイトル設定
root_window.title('Tkinter widget sample')

# 他の部品設定や配置、イベント登録
# -----------------------------------------
# イベント処理
def event_button():
    print('event_button')
    
# 部品生成
Intvar0 = tk.IntVar()
Intvar1 = tk.IntVar()
Intvar2 = tk.IntVar()

frame        = tk.Frame(root_window)
label        = tk.Label(frame, text="label")
button       = tk.Button(frame, text="Button", command=event_button)
entry        = tk.Entry(frame)
combobox     = ttk.Combobox(frame, values=["select1", "select2", "select3"])
radiobutton  = tk.Radiobutton(frame, text="Radio1", variable=Intvar0, value=0)
radiobutton2 = tk.Radiobutton(frame, text="Radio2", variable=Intvar0, value=1)
checkbutton  = tk.Checkbutton(frame, text="Check1", variable=Intvar1)
checkbutton2 = tk.Checkbutton(frame, text="Check2", variable=Intvar2)

# 初期化
entry.insert(0,'Entry text ..')
Intvar0.set(0)
Intvar1.set(1)
Intvar2.set(1)
combobox.set("select1")

# 部品配置
frame.pack()
label.grid        (row=1, column=1, padx=5, pady=5, sticky=tk.W)
entry.grid        (row=2, column=1, padx=5, pady=5, sticky=tk.W)
combobox.grid     (row=3, column=1, padx=5, pady=5, sticky=tk.W)
radiobutton.grid  (row=4, column=1, padx=5, pady=5, sticky=tk.W)
radiobutton2.grid (row=4, column=2, padx=5, pady=5, sticky=tk.W)
checkbutton.grid  (row=5, column=1, padx=5, pady=5, sticky=tk.W)
checkbutton2.grid (row=5, column=2, padx=5, pady=5, sticky=tk.W)
button.grid       (row=6, column=1, padx=5, pady=5, sticky=tk.W)
# -----------------------------------------

#　ループ処理
root_window.mainloop()

