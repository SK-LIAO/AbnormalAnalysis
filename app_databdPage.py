# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 08:10:00 2022

@author: A90127
"""

import tkinter as tk
from tkinter import filedialog,ttk

import dataBuild as dB

from app_GUI import GUI
from readme import frame_styles


class databdPage(GUI):  # 繼承GUI
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        self.name = 'dataPage'

        frame1 = tk.LabelFrame(self, frame_styles, text="工卡進度資料預覽")
        frame1.place(relx=0.1, rely=0.02, height=450, width=800)

        frame2 = tk.LabelFrame(self, frame_styles, text="匯入")
        frame2.place(relx=0.1, rely=0.77, height=75, width=800)

        button1 = tk.Button(frame2, text="選擇檔案", command=lambda: Load_path(self))
        button1.grid(column=0,row=0)
        button2 = tk.Button(frame2, text="匯入資料", command=lambda: Load_data(self))
        button2.grid(column=0,row=1)
        Label1 = tk.Label(frame2,text='',width=100)
        Label1.grid(column=1,row=0)
        var = tk.StringVar()
        var.set('')
        Label2 = tk.Label(frame2,textvariable=var,width=100)
        Label2['fg'] = '#0000FF'
        Label2.grid(column=1,row=1)

        tv1 = ttk.Treeview(frame1,show='headings',selectmode='none')
        tv1.place(relheight=0.995, relwidth=0.995)
        #設定y軸滑桿
        ytreescroll = tk.Scrollbar(frame1)
        ytreescroll.configure(command=tv1.yview)
        tv1.configure(yscrollcommand=ytreescroll.set)
        ytreescroll.pack(side="right", fill="y")
        #設定x軸滑桿
        xtreescroll = tk.Scrollbar(frame1,orient=tk.HORIZONTAL)
        xtreescroll.configure(command=tv1.xview)
        tv1.configure(xscrollcommand=xtreescroll.set)
        xtreescroll.pack(side="bottom", fill="x")
        def Load_path(self):
            filename = filedialog.askopenfilename()
            Label1['text'] = filename
            self.path = filename
    
        def Load_data(self):
            Refresh_data()
            controller.data, controller.head,  = dB.dataBuild(self.path)
            column_list_account = list(controller.head)
            tv1['columns'] = column_list_account 
            for column in column_list_account:
                tv1.heading(column, text=column)
                tv1.column(column, width=140)
            for row in controller.data[:50]:
                tv1.insert("", 'end', values=list(row))
            var.set('檔案已經匯入')        
        
        #刪除Treeview的數據
        def Refresh_data():
            tv1.delete(*tv1.get_children())  # *=splat operator
            
