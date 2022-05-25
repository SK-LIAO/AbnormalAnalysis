# -*- coding: utf-8 -*-
"""
Created on Thu May  5 14:39:17 2022

@author: A90127
"""
import numpy as np
import tkinter as tk
from tkinter import ttk
from pyperclip import copy
from datetime import datetime, timedelta, time

import stepAnaly as sA
from app_GUI import GUI
from readme import frame_styles, step_ch, step_air
from tkcalendar import DateEntry #日曆模組

class stepPage(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)

        frame1 = tk.LabelFrame(self, frame_styles, text="分析結果")
        frame1.place(relx=0.33, rely=0.02, height=550, width=576)
        frame2 = tk.LabelFrame(self, frame_styles, text="共同參數")
        frame2.place(relx=0.1, rely=0.02, height=550, width=227)
        frame3 = tk.LabelFrame(frame2, frame_styles, text="計算前後站點比例")
        frame3.place(relx=0.02, rely=0.15, height=102, width=213)
        frame4 = tk.LabelFrame(frame2, frame_styles, text="總加工時間統計")
        frame4.place(relx=0.02, rely=0.35, height=340, width=213)
        frame5 = tk.LabelFrame(frame4, frame_styles, text="各站加工時間統計")
        frame5.place(relx=0.02, rely=0.15, height=268, width=200)
        frame6 = tk.LabelFrame(frame5, frame_styles, text="查詢滯留工卡")
        frame6.place(relx=0.02, rely=0.3, height=170, width=187)
        
        
        tv1 = ttk.Treeview(frame1,selectmode='browse')#建立資料數
        def copyEKA(event):
            menu = tk.Menu(parent,tearoff=0)
            def copyinE():
                for item  in tv1.selection():
                    item_text = tv1.item(item,"values")
                card = item_text[0]
                copy(card)
            def copyinKA():
                for item  in tv1.selection():
                    item_text = tv1.item(item,"values")
                card = item_text[1]
                copy(card)
            menu.add_command(label='複製工卡號',command=copyinE) #點擊後複製工卡號
            menu.add_command(label='複製染單號',command=copyinKA)
            menu.post(event.x_root, event.y_root)
        tv1.bind('<Button-3>', copyEKA) #右鍵單擊出現複製選單
        
        tv1.place(relheight=0.995, relwidth=0.995)
        #設定y軸滑桿
        ytreescroll = tk.Scrollbar(frame1)
        ytreescroll.configure(command=tv1.yview)
        tv1.configure(yscrollcommand=ytreescroll.set)
        ytreescroll.pack(side="right", fill="y")

        self.var6 = tk.IntVar()
        Radiobutton2_1 = tk.Radiobutton(frame2,text='斗工(水)',variable=self.var6,value=0,
                                        command=lambda: changeFactor())
        Radiobutton2_2 = tk.Radiobutton(frame2,text='雲科(氣)',variable=self.var6,value=1,
                                        command=lambda: changeFactor())
        Radiobutton2_1.grid(column=0,row=0,sticky='ew')
        Radiobutton2_2.grid(column=1,row=0,sticky='w')
        self.var6.set(0)           
        
        pm = datetime.now()-timedelta(days=30)            
        Label1 = tk.Label(frame2,text='日期(起)')
        Label1.grid(column=0,row=1,sticky='ew')
        Button1_1 = DateEntry(frame2, width=13, background='darkblue',
                    foreground='white', borderwidth=3,
                    year=pm.year, month=pm.month, day=pm.day)
        Button1_1.grid(column=1,row=1,sticky='w')
        
        Label2 = tk.Label(frame2,text='日期(迄)')
        Label2.grid(column=0,row=2,sticky='ew')
        Button2_1 = DateEntry(frame2, width=13, background='darkblue',
                    foreground='white', borderwidth=3)
        Button2_1.grid(column=1,row=2,sticky='w')
        
        Label3 = tk.Label(frame6,text='滯留天數')
        Label3.grid(column=0,row=2,sticky='ew')
        self.var1 = tk.IntVar()
        self.var1.set(14)
        self.Entry3_1 = tk.Entry(frame6,textvariable=self.var1,width=2)
        self.Entry3_1.grid(column=1,row=2,sticky='nsw')
        
        
        Label4 = tk.Label(frame5,text='類型')
        Label4.grid(column=0,row=0,sticky='ew')
        self.var2 = tk.StringVar()
        self.Combobox4_1 = ttk.Combobox(frame5,textvariable=self.var2,
                                   values = ['已結案','未結案','全部'],width=13,state="readonly")
        #狀態轉數字字典
        fidict = {}
        for i,ch in enumerate(['已結案','未結案','全部']):
            fidict[ch] = i
        self.Combobox4_1.current(0)
        self.Combobox4_1.grid(column=1,row=0,sticky='w')
        
        Label5 = tk.Label(frame4,text='指定型體')
        Label5.grid(column=0,row=0,sticky='ew')
        self.var3 = tk.StringVar()
        self.var3.set('')
        self.Entry5_1 = tk.Entry(frame4,textvariable=self.var3,width=19)
        self.Entry5_1.grid(column=1,row=0,sticky='nsw')
        
        Label6 = tk.Label(frame3,text='站點')
        Label6.grid(column=0,row=0,sticky='ew')
        self.var4 = tk.StringVar()
        if self.var6.get()==0:
            steps = step_ch
        else:
            steps = step_air        
        self.Combobox6_1 = ttk.Combobox(frame3,textvariable=self.var4,
                                   values = steps,width=13,state="readonly")
        self.Combobox6_1.current()
        self.Combobox6_1.grid(column=1,row=0,sticky='w')
        
        button1 = tk.Button(frame3,text="下站比例", command = lambda: forestep())
        button1.grid(column=0,row=1)
        button2 = tk.Button(frame3,text="上站比例", command = lambda: backstep())
        button2.grid(column=0,row=2)
        button3 = tk.Button(frame5,text="各站統計", command = lambda: each())
        button3.grid(column=0,row=1)
        button4 = tk.Button(frame4,text="全站統計", command = lambda: total())
        button4.grid(column=0,row=1)
        button5 = tk.Button(frame5,text="最久天數", command = lambda: maxday())
        button5.grid(column=0,row=2)
        self.var5 = tk.StringVar()
        self.var5.set('')
        label5_1 = tk.Label(frame5,textvariable=self.var5,fg='blue',width=4)
        label5_1.grid(column=1,row=2,sticky='ew')
        button6 = tk.Button(frame6,text="滯留工卡", command = lambda: staycard())
        button6.grid(column=0,row=5)
        
        def changeFactor():
            if self.var6.get()==0:
                steps = step_ch
            else:
                steps = step_air
            self.Combobox6_1.configure(value=steps)
        
        self.static = 0
        def forestep():
            Refresh()
            Retitle(['站點','百分比(%)'])
            startdate = datetime.combine(Button1_1.get_date(), time())
            enddate = datetime.combine(Button2_1.get_date(),time())
            ds = (enddate-startdate).days
            step = self.var4.get()
            data = sA.prodNextStep(startdate,step,controller.data,ds,True)
            for row in data:
                tv1.insert("", 'end', values=row)
                      
        def backstep():
            Refresh()
            Retitle(['站點','百分比(%)'])
            startdate = datetime.combine(Button1_1.get_date(), time())
            enddate = datetime.combine(Button2_1.get_date(),time())
            ds = (enddate-startdate).days
            step = self.var4.get()
            data = sA.prodBackStep(startdate,step,controller.data,ds,True)
            for row in data:
                tv1.insert("", 'end', values=row)
        
        def total():
            Refresh()
            Retitle(['平均時間(天)','標準差(天)'])
            startdate = datetime.combine(Button1_1.get_date(), time())
            enddate = datetime.combine(Button2_1.get_date(),time())
            ds = (enddate-startdate).days
            specific = self.var3.get()
            data = sA.avgProdDays(startdate, controller.data, ds, specific, True, self.var6.get())
            avg = round(np.average([d[1] for d in data]),1)
            std = round(np.std([d[1] for d in data]),1)
            tv1.insert('', 'end', values=[avg,std])
            
        def each():
            Refresh()
            Retitle(['生產站點','平均時間(天)','標準差(天)'])
            startdate = datetime.combine(Button1_1.get_date(), time())
            enddate = datetime.combine(Button2_1.get_date(),time())
            ds = (enddate-startdate).days            
            specific = self.var3.get()
            self.static = sA.stepStatic(startdate,controller.data,ds,fidict[self.var2.get()],
                                        specific,True,self.var6.get())
            data =[ [s.name, 
                    round(np.average([i[0]+i[1]/24/60/60 for i in s.dt]),1),
                    round(np.std([i[0]+i[1]/24/60/60 for i in s.dt]),1)] for s in self.static if len(s.inner)>0] 
            for row in data:
                tv1.insert("", 'end', values=row)
            
            
        def maxday():
            startdate = datetime.combine(Button1_1.get_date(), time())
            enddate = datetime.combine(Button2_1.get_date(),time())
            ds = (enddate-startdate).days
            specific = self.var3.get()
            ch = sA.maxProdDays(startdate,controller.data,ds,fidict[self.var2.get()],specific,True,self.var6.get())
            self.var5.set(round(ch,1))
            
        def staycard():
            Refresh()
            Retitle(['工卡號','指染單號','滯留天數','是否結案'])
            startdate = datetime.combine(Button1_1.get_date(), time())
            enddate = datetime.combine(Button2_1.get_date(),time())
            ds = (enddate-startdate).days
            stayd = self.var1.get()
            specific = self.var3.get()
            self.static = sA.prodStay(startdate,stayd,controller.data,ds,fidict[self.var2.get()],
                                      specific,True,self.var6.get())
            for row in self.static:
                tv1.insert("", 'end', values=row)
                     
        def Refresh():
            tv1.delete(*tv1.get_children())  # *=splat operator
        def Retitle(ls):
            column_list_account = ls
            tv1['columns'] = column_list_account # 資料表頭
            tv1["show"] = "headings"  # 移除第一空白行
            for column in column_list_account:
                tv1.heading(column, text=column)
                tv1.column(column, width=140)