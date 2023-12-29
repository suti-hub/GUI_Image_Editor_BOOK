# -*- coding: utf-8 -*-  

import tkinter as tk

class SimpleCalculator():
    
    def __init__(self, root):
        
        list_num        = ['0','1','2','3','4','5','6','7','8','9']
        dict_operator   = {'add':'+', 'sub':'-', 'mul':'*', 'div':'/'}
        dict_button     = {}
        btn_size = 7
        
        # タイトル設定
        root.title("簡易電卓")
        
        # Widget生成
        # entry
        self.entry = tk.Entry(root, width=30)
        
        # button: 0~9
        for num in list_num:
            dict_button[num] = tk.Button(root, text=num,  width=btn_size, command=self.__click(num))
        
        # button: +,-,*./
        for key, val in dict_operator.items():
            dict_button[key] = tk.Button(root, text=val, width=btn_size, command=self.__click(val))
        
        # button: =,C
        dict_button['eql'] = tk.Button(root, text="=", width=btn_size, command=self.__calculate)
        dict_button['clr'] = tk.Button(root, text="C", width=btn_size, command=self.__clear)
                    
        # Layout設定
        # entry
        self.entry.grid(row=0, column=0, columnspan=4)
        
        # button
        dict_button['1'].grid(row=1,column=0)
        dict_button['2'].grid(row=1,column=1)
        dict_button['3'].grid(row=1,column=2)
        dict_button['4'].grid(row=2,column=0)
        dict_button['5'].grid(row=2,column=1)
        dict_button['6'].grid(row=2,column=2)
        dict_button['7'].grid(row=3,column=0)
        dict_button['8'].grid(row=3,column=1)
        dict_button['9'].grid(row=3,column=2)
        dict_button['0'].grid(row=4,column=0)       
        dict_button['add'].grid(row=1,column=3)
        dict_button['sub'].grid(row=2,column=3)
        dict_button['mul'].grid(row=3,column=3)
        dict_button['div'].grid(row=4,column=3)
        dict_button['eql'].grid(row=5,column=3)
        dict_button['clr'].grid(row=5,column=0)
        
        # 初期化
        self.result = 0.0
    
    def __calculate(self):
        try:
            self.result = eval(self.entry.get())
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(self.result))
        except:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, '')
   

    def __click(self, text):
        def __click_sub():
            current = self.entry.get()
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, current + text)
            
        return __click_sub

    def __clear(self):
        self.entry.delete(0, tk.END)
        self.result = 0.0
        

def main():
    #　Tkinter root 生成
    root = tk.Tk()
    # SimpleCalculatorクラス生成
    SimpleCalculator(root)
    # Tkinterループ処理
    root.mainloop()

if __name__ == '__main__':
    main()
