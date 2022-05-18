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
        
        Label1_1 = tk.Label(frame1,text='日期(起)')
        Label1_1.grid(column=0,row=0,sticky='ew')
        self.Button1_1 = DateEntry(frame1, width=13, background='darkblue',
                    foreground='white', borderwidth=3)
        self.Button1_1.set_date(datetime.now()-timedelta(days=30))
        self.Button1_1.grid(column=1,row=0,sticky='w')
        Label1_2 = tk.Label(frame1,text='日期(迄)')
        Label1_2.grid(column=0,row=1,sticky='ew')
        self.Button1_2 = DateEntry(frame1, width=13, background='darkblue',
                    foreground='white', borderwidth=3)
        self.Button1_2.grid(column=1,row=1,sticky='w')
        
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
        
    def graph(self,controller):
        self.f_plot.clear()
        shoeType = True if self.var1.get()=='是' else False
        int_num = int(self.Entry1_5.get())
        std_num = float(self.Entry1_4.get())
        a = datetime.combine(self.Button1_1.get_date(),time())
        b = datetime.combine(self.Button1_2.get_date(),time())
        data = np.array([d for d in controller.data if b>dB.myStrptime(d[1])>=a])
        data = lA.normalLoss(data,shoeType)
        pts = np.array([[controller.E2mass[d[0]],(controller.E2mass[d[0]]-d[9])/controller.E2mass[d[0]]] for d in data])
        line = lA.piecewiseLoss(pts[:,0],pts[:,1],int_num,std_num)
        a, b = lA.log_regre(line[:,0],line[:,1])
        x = np.linspace(min(line[:,0]), max(line[:,0]))
        self.f_plot.scatter(pts[:,0], pts[:,1], alpha=0.3)
        self.f_plot.plot(x,a*np.log(x)+b,color='r')
        self.f_plot.set_ylabel('Rate of Loss')
        self.f_plot.set_title('Mass-Loss Estimation')
        self.f_plot.set_xlabel('Mass(kg)')
        self.f_plot.text(150,0.4,'y={:.4f}ln(x)+{:.4f}'.format(a,b),size=14,color='r')
        self.canvs.draw()
           
            