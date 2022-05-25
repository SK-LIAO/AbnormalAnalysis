# -*- coding: utf-8 -*-
"""
Created on Thu May  5 14:48:34 2022

@author: A90127
"""

import numpy as np
import tkinter as tk

from tkinter import ttk

from datetime import datetime, timedelta, time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pyperclip import copy

import lossAnaly as lA
import dataBuild as dB
from app_GUI import GUI
from readme import frame_styles
from tkcalendar import DateEntry #日曆模組

class lossPage(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        
        frame1 = tk.LabelFrame(self, frame_styles, text="參數設定")
        frame1.place(relx=0.1, rely=0.02, height=550, width=202)
        frame2 = tk.LabelFrame(self, frame_styles, text="損耗函數")
        frame2.place(relx=0.3, rely=0.02, height=550, width=600)
        frame3 = tk.LabelFrame(frame1, frame_styles, text="工卡搜索")
        frame3.place(relx=0.01, rely=0.35, height=340, width=192)
        
        self.var2 = tk.IntVar()
        Radiobutton2_1 = tk.Radiobutton(frame1,text='斗工(水)',variable=self.var2,value=0)
        Radiobutton2_2 = tk.Radiobutton(frame1,text='雲科(氣)',variable=self.var2,value=1)
        Radiobutton2_1.grid(column=0,row=0,sticky='ew')
        Radiobutton2_2.grid(column=1,row=0,sticky='w')
        self.var2.set(0)
        
        Label1_1 = tk.Label(frame1,text='日期(起)')
        Label1_1.grid(column=0,row=1,sticky='ew')
        self.Button1_1 = DateEntry(frame1, width=13, background='darkblue',
                    foreground='white', borderwidth=3)
        self.Button1_1.set_date(datetime.now()-timedelta(days=30))
        self.Button1_1.grid(column=1,row=1,sticky='w')
        Label1_2 = tk.Label(frame1,text='日期(迄)')
        Label1_2.grid(column=0,row=2,sticky='ew')
        self.Button1_2 = DateEntry(frame1, width=13, background='darkblue',
                    foreground='white', borderwidth=3)
        self.Button1_2.grid(column=1,row=2,sticky='w')
        
        Label1_3 = tk.Label(frame1,text='鞋型布')
        Label1_3.grid(column=0,row=3,sticky='ew')
        self.var1 = tk.StringVar()
        self.Combobox1_1 = ttk.Combobox(frame1,textvariable=self.var1,
                                   values = ['否','是'],width=13,state="readonly")
        self.Combobox1_1.current(1)
        self.Combobox1_1.grid(column=1,row=3,sticky='ew')
        
        Label1_4 = tk.Label(frame1,text='標準差數')
        Label1_4.grid(column=0,row=4,sticky='ew')
        self.Entry1_4 = tk.Entry(frame1,width=13,
                              validate='key',validatecommand=(parent.register(controller.Is_float), '%P'))
        self.Entry1_4.grid(column=1,row=4,sticky='ew')
        self.Entry1_4.insert(0, '2')
        
        Label1_5 = tk.Label(frame1,text='切割區間數')
        Label1_5.grid(column=0,row=5,sticky='ew')
        self.Entry1_5 = tk.Entry(frame1,width=13,text='30',
                              validate='key',validatecommand=(parent.register(controller.Is_int), '%P'))
        self.Entry1_5.grid(column=1,row=5,sticky='ew')
        self.Entry1_5.insert(0, '30')
        Button1 = tk.Button(frame1,text="損耗統計", command = lambda:self.graph(controller))
        Button1.grid(column=0,row=6,sticky='ew')
        
        f = Figure(figsize=(5, 4), dpi=100)
        self.f_plot = f.add_subplot(111)
        self.canvs = FigureCanvasTkAgg(f, frame2)
        self.canvs.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        Label2_1 = tk.Label(frame3,text='重量範圍')
        self.Entry2_1 = tk.Entry(frame3,width=8,text='0',
                            validate='key',validatecommand=(parent.register(controller.Is_int), '%P'))
        self.Entry2_1.insert(0, '0')
        Label2_2 = tk.Label(frame3,text='~')
        self.Entry2_2 = tk.Entry(frame3,width=8,text='10',
                            validate='key',validatecommand=(parent.register(controller.Is_int), '%P'))
        self.Entry2_2.insert(0, '30')
        Label2_3 = tk.Label(frame3,text='損耗範圍')
        self.Entry2_3 = tk.Entry(frame3,width=8,text='0.5',
                            validate='key',validatecommand=(parent.register(controller.Is_float), '%P'))
        self.Entry2_3.insert(0, '0.5')
        Label2_4 = tk.Label(frame3,text='~')
        self.Entry2_4 = tk.Entry(frame3,width=8,text='0.9',
                            validate='key',validatecommand=(parent.register(controller.Is_float), '%P'))
        self.Entry2_4.insert(0, '0.6')
        Label2_1.grid(row=0,column=0,sticky='ew')
        Label2_2.grid(row=1,column=1,sticky='ew')
        Label2_3.grid(row=2,column=0,sticky='ew')
        Label2_4.grid(row=3,column=1,sticky='ew')
        self.Entry2_1.grid(row=1,column=0,sticky='ew')
        self.Entry2_2.grid(row=1,column=2,sticky='ew')
        self.Entry2_3.grid(row=3,column=0,sticky='ew')
        self.Entry2_4.grid(row=3,column=2,sticky='ew')
        Button2_1 = tk.Button(frame3,text='搜索',fg='#00F',command=lambda: ECheck(self, controller))
        Button2_1.grid(row=4,column=0,sticky='ew')
        
    def graph(self,controller):
        self.f_plot.clear()
        shoeType = True if self.var1.get()=='是' else False
        int_num = int(self.Entry1_5.get())
        std_num = float(self.Entry1_4.get())
        a = datetime.combine(self.Button1_1.get_date(),time())
        b = datetime.combine(self.Button1_2.get_date(),time())
        data = np.array([d for d in controller.data if b>dB.myStrptime(d[1])>=a])
        self.data = lA.normalLoss(data,shoeType,self.var2.get())
        #統計損耗
        pts = np.array([[controller.E2mass[d[0]],(controller.E2mass[d[0]]-d[-1])/controller.E2mass[d[0]]] for d in self.data])
        '''
        for d in self.data:
            if (controller.E2mass[d[0]]-d[-1])/controller.E2mass[d[0]]<0:
                print(d[0],(controller.E2mass[d[0]]-d[-1])/controller.E2mass[d[0]])
        '''
        line = lA.piecewiseLoss(pts[:,0],pts[:,1],int_num,std_num)
        #對數回歸
        a1, b1 = lA.log_regre(line[:,0],line[:,1])
        #倒數迴歸
        a2, b2 = lA.reciprocal_regre(line[:,0],line[:,1])
        x = np.linspace(min(line[:,0]), max(line[:,0]))
        
        self.f_plot.scatter(pts[:,0], pts[:,1], alpha=0.3)
        #對數回歸線
        self.f_plot.plot(x,a1*np.log(x)+b1,color='r')
        #倒數迴歸線
        self.f_plot.plot(x,a2/np.sqrt(x)+b2,color='g')
        self.f_plot.set_ylabel('Rate of Loss')
        self.f_plot.set_title('Mass-Loss Estimation')
        self.f_plot.set_xlabel('Mass(kg)')
        #對數回歸線方程式
        self.f_plot.text(0.35,0.6,'y={:.4f}ln(x)+{:.4f}'.format(a1,b1),size=14,color='r',transform=self.f_plot.transAxes)
        #倒數迴歸線方程式
        self.f_plot.text(0.35,0.7,'y={:.4f}/x^0.5+{:.4f}'.format(a2,b2),size=14,color='g',transform=self.f_plot.transAxes)
        self.canvs.draw()
           
class ECheck(tk.Toplevel):
    def __init__(self, parent,controller):
        tk.Toplevel.__init__(self, parent, bg="#BEB2A7")
        
        self.title('搜索')
        self.resizable(0, 0) #prevents the app from being resized
        self.geometry("470x300+100+20") #fixes the applications size
        self.iconbitmap('LC.ico')

        frame = tk.LabelFrame(self,frame_styles,text='結果')
        frame.place(relx=0.02,rely=0.02,height=280,width=450)
        
        column_list_account = ['工卡號','指染單號','重量(kg)','損耗(%)']
        tv = ttk.Treeview(frame,columns=column_list_account,show="headings",selectmode='browse')
        for column in column_list_account:
            tv.heading(column, text=column) 
            tv.column(column, width=100)
        def copyEKA(event):
            menu = tk.Menu(parent,tearoff=0)
            def copyinE():
                for item  in tv.selection():
                    item_text = tv.item(item,"values")
                card = item_text[0]
                copy(card)
            def copyinKA():
                for item  in tv.selection():
                    item_text = tv.item(item,"values")
                card = item_text[1]
                copy(card)
            menu.add_command(label='複製工卡號',command=copyinE) #點擊後複製工卡號
            menu.add_command(label='複製指染單號',command=copyinKA)
            menu.post(event.x_root, event.y_root)
        tv.bind('<Button-3>', copyEKA) #右鍵單擊出現複製選單
        
        ytreescroll = tk.Scrollbar(frame)
        ytreescroll.configure(command=tv.yview)
        tv.configure(yscrollcommand=ytreescroll.set)
        ytreescroll.pack(side="right", fill="y")
        
        def condition(d):
            m = controller.E2mass[d[0]]
            e = (m-d[-1])/m
            bl1 = int(parent.Entry2_1.get())<=m
            bl2 = int(parent.Entry2_2.get())>=m
            bl3 = float(parent.Entry2_3.get())<=e
            bl4 = float(parent.Entry2_4.get())>=e
            return all([bl1,bl2,bl3,bl4])
        for d in parent.data:
            if condition(d):
                m = controller.E2mass[d[0]]
                e = (m-d[-1])/m
                tv.insert('','end',values=[d[0],d[2],m,round(100*e,2)]) 
        tv.place(relheight=0.995, relwidth=0.995)
