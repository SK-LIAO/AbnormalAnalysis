# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 13:58:12 2021

@author: A90127
"""

import tkinter as tk

from app_authorPage import AuthorPage
from app_databdPage import databdPage
from app_urgentbdPage import urgentbdPage
from app_fiberbdPage import fiberbdPage
from app_stepPage import stepPage
from app_abnormalPage import abnormalPage
from app_waitPage import waitPage
from app_lossPage import lossPage


class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        main_frame = tk.Frame(self, bg="#84CEEB")
        #main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")
        #main_frame.grid_rowconfigure(0, weight=1)
        #main_frame.grid_columnconfigure(0, weight=1)
        
        self.resizable(0, 0) #禁止調整視窗大小
        self.geometry("1024x600+504+20") #調整視窗大小及位置
        self.iconbitmap('LC.ico') 
        
        self.frames = {} #準備收集所有框架
        self.data = [] #準備放置基礎數據
        self.urgent = [] #準備放置急件數據
        
        
        pages = (databdPage,urgentbdPage,fiberbdPage,
                 abnormalPage, waitPage, stepPage, lossPage,AuthorPage)
        for F in pages:
            frame = F(main_frame, self) #建立框架
            self.frames[F] = frame #將框架存入 self 裡
            frame.grid(row=0, column=0, sticky="nsew") #放置框架
        
        menubar = MenuBar(self)
        tk.Tk.config(self, menu=menubar)
        
        self.show_frame(databdPage) #將指定的框架拉到最上層
        
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise() 
    def Quit_application(self):
        self.destroy()
        
    def Is_float(self,P):
        if P in ['','-']:
            return True
        else:
            try:
                float(P)
                return True
            except:
                return False
            
    def Is_int(self,P):
        if P in ['']:
            return True
        else:
            try:
                int(P)
                return True
            except:
                return False
    
        
class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        menu_file = tk.Menu(self, tearoff=0)
        self.add_cascade(label="檔案", menu=menu_file)
        menu_file.add_command(label="匯入工卡資料", command=lambda: parent.show_frame(databdPage))
        menu_file.add_command(label="匯入急件資料", command=lambda: parent.show_frame(urgentbdPage))
        menu_file.add_command(label="匯入工胚資料", command=lambda: parent.show_frame(fiberbdPage))
        menu_file.add_separator() #分隔線
        menu_file.add_command(label="離開", command=lambda: parent.Quit_application())

        menu_analysis = tk.Menu(self, tearoff=0)
        self.add_cascade(label="分析", menu=menu_analysis)
        menu_analysis.add_command(label='生產異常', command=lambda: parent.show_frame(abnormalPage))
        menu_analysis.add_command(label='待加工', command=lambda: parent.show_frame(waitPage))
        menu_analysis.add_command(label='站點工時', command=lambda: parent.show_frame(stepPage))
        menu_analysis.add_command(label='損耗', command=lambda: parent.show_frame(lossPage))

        menu_expression = tk.Menu(self, tearoff=0)
        self.add_cascade(label="說明", menu=menu_expression)
        menu_expression.add_command(label="關於App", command=lambda: parent.show_frame(AuthorPage))

            

      
root = MyApp()
root.title("利勤資料分析App")

root.mainloop()