# -*- coding: utf-8 -*-
"""
Created on Thu May  5 14:48:51 2022

@author: A90127
"""

import numpy as np
import tkinter as tk
import matplotlib as mpl
from tkinter import ttk
from pyperclip import copy
from datetime import datetime, timedelta, time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import dataBuild as dB
import waitAnaly as wA
from app_GUI import GUI
from readme import frame_styles, step_en, step_ch
from tkcalendar import DateEntry #日曆模組

class waitPage(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        
        frame1 = tk.LabelFrame(self, frame_styles, text="分析結果")
        frame1.place(relx=0.3, rely=0.02, height=550, width=600)
        frame2 = tk.LabelFrame(self, frame_styles, text="站點待生產")
        frame2.place(relx=0.1, rely=0.02, height=550, width=202)
        frame3 = tk.LabelFrame(frame2, frame_styles, text="站點走勢圖")
        frame3.place(relx=0.01, rely=0.27, height=382, width=192)   
        
        
        self.tv = ttk.Treeview(frame1,selectmode='browse')#建立資料數
        tv = self.tv
        column_list_account = ['待生產站點','待生產量(kg)','工卡數']
        tv['columns'] = column_list_account # 資料表頭
        tv["show"] = "headings"  # 移除第一空白行
        for column in column_list_account:
            tv.heading(column, text=column)
            tv.column(column, width=140)
        def checkdata(event,*args):
            a = datetime.combine(Button1_1.get_date(),time())
            t1 = self.timedict[self.var1.get()]
            self.searchtime = a.replace(hour=t1)
            waitCheck(self, controller)
        tv.bind('<Double-1>', checkdata) #雙擊檢視詳細資料
        tv.place(relheight=0.995, relwidth=0.995)
        
        Label1 = tk.Label(frame2,text='日期')
        Label1.grid(column=0,row=0,sticky='ew')
        Button1_1 = DateEntry(frame2, width=13, background='darkblue',
                    foreground='white', borderwidth=3)
        Button1_1.grid(column=1,row=0,sticky='w')
        
        Label2 = tk.Label(frame2,text='時間')
        Label2.grid(column=0,row=1,sticky='ew')
        self.timedict = {}
        times = ['00:00','01:00','02:00','03:00','04:00','05:00',
                 '06:00','07:00','08:00','09:00','10:00','11:00',
                 '12:00','13:00','14:00','15:00','16:00','17:00',
                 '18:00','19:00','20:00','21:00','22:00','23:00']
        for i in range(24):
            self.timedict[times[i]]=i
        self.var1 = tk.StringVar()
        self.Combobox2_1 = ttk.Combobox(frame2,textvariable=self.var1,
                                   values = times,
                                   width=13,state="readonly")
        self.Combobox2_1.current(8)
        self.Combobox2_1.grid(column=1,row=1,sticky='w')

     
        Label3 = tk.Label(frame2,text='指定型體')
        Label3.grid(column=0,row=2,sticky='ew')
        self.var4 = tk.StringVar()
        self.var4.set('')
        self.Entry5_1 = tk.Entry(frame2,textvariable=self.var4,width=19)
        self.Entry5_1.grid(column=1,row=2,sticky='nsw')
        
        button1 = tk.Button(frame2,text="各站統計", command = lambda: each())
        button1.grid(column=0,row=3)
        
        Label3 = tk.Label(frame3,text='日期(迄)')
        Label3.grid(column=0,row=0,sticky='ew')
        Button3_1 = DateEntry(frame3, width=13, background='darkblue',
                    foreground='white', borderwidth=3)
        Button3_1.grid(column=1,row=0,sticky='w')
        
        Label4 = tk.Label(frame3,text='時間(迄)')
        Label4.grid(column=0,row=1,sticky='ew')
        self.var2 = tk.StringVar()
        self.Combobox3_1 = ttk.Combobox(frame3,textvariable=self.var2,
                                   values = times,
                                   width=13,state="readonly")
        self.Combobox3_1.current(9)
        self.Combobox3_1.grid(column=1,row=1,sticky='w')
        
        
        button2 = tk.Button(frame3,text="繪製圖表", command = lambda: graph() )
        button2.grid(column=0,row=2)
        
        
        def graph():
            a = datetime.combine(Button1_1.get_date(),time())
            t1 = self.timedict[self.var1.get()]
            timestart = a.replace(hour=t1)
            b = datetime.combine(Button3_1.get_date(),time())
            t2 = self.timedict[self.var2.get()]
            timeend = b.replace(hour=t2)
            specific = self.var4.get()
            dt = timeend - timestart
            n_hrs = int(dt.days*24 + dt.seconds/60/60)
            self.timelist = [timestart+timedelta(hours=i) for i in range(n_hrs)]
            self.allstatic = wA.staticGraph(timestart,timeend,controller.data,specific)
            waitGraph(self,controller)
        
        
        def each():
            Refresh()
            #日期
            da = datetime.combine(Button1_1.get_date(),time())
            #時間(整數)
            ti = self.timedict[self.var1.get()]
            specific = self.var4.get()
            self.static = wA.stepStatic(da.replace(hour=ti),controller.data,specific,'',ra=True)
            data =[ [s.name,round(sum([i[2] for i in s.inner]),1), len(s.inner)] 
                   for s in self.static] 
            for row in data:
                tv.insert("", 'end', values=row)
                
        def Refresh():
            # Deletes the data in the current treeview and reinserts it.
            tv.delete(*tv.get_children())  # *=splat operator


class waitCheck(tk.Toplevel):
    def __init__(self, parent,controller):
        tk.Toplevel.__init__(self, parent, bg="#BEB2A7")
        
        self.title('詳細資料')
        self.resizable(0, 0) #prevents the app from being resized
        self.geometry("610x500+100+20") #fixes the applications size
        self.iconbitmap('LC.ico')
        for item in parent.tv.selection():
            item_text = parent.tv.item(item,"values")
        frame = tk.LabelFrame(self,frame_styles,text=item_text[0]+"待生產工卡數據")
        frame.place(relx=0.02,rely=0.02,height=480,width=592)
        newtv = ttk.Treeview(frame,selectmode='browse')
        column_list_account = ['工卡號','染單號','重量(kg)','急件風險(%)','工時(期望)','重切交期']
        newtv['columns'] = column_list_account # 資料表頭
        newtv["show"] = "headings"  # 移除第一空白行
        ytreescroll = tk.Scrollbar(frame)
        ytreescroll.configure(command=newtv.yview)
        newtv.configure(yscrollcommand=ytreescroll.set)
        ytreescroll.pack(side="right", fill="y")
        if len(controller.urgent)>0:
            urgentDeadlineInd = list(controller.urgent_head).index('重切交期')
            urgentInd = list(controller.urgent_head).index('染單')
            urgentKAs = controller.urgent[:,urgentInd]
        widths = (90,80,50,70,70,80)
        for column,w in zip(column_list_account,widths):
            newtv.heading(column, text=column)
            newtv.column(column, width=w)
        for s in parent.static:
            if s.name == item_text[0]:
                for row in s.inner:
                    if len(controller.urgent)>0 and row[1] in urgentKAs:
                        j = list(controller.urgent[:,urgentInd]).index(row[1])
                        da = datetime.combine(controller.urgent[j,urgentDeadlineInd],time())
                        isurgent = [dB.risk(row[3:5],parent.searchtime,da),round(row[3],2),dB.myStrftime(da)]
                    else:
                        isurgent = ['','','']
                    newtv.insert("", 'end', values=row[:3]+isurgent)
        def copyEKA(event):
            menu = tk.Menu(parent,tearoff=0)
            def copyinE():
                for item  in newtv.selection():
                    item_text = newtv.item(item,"values")
                card = item_text[0]
                copy(card)    
            def copyinKA():
                for item  in newtv.selection():
                    item_text = newtv.item(item,"values")
                card = item_text[1]
                copy(card)
            menu.add_command(label='複製工卡號',command=copyinE) #點擊後複製工卡號
            menu.add_command(label='複製染單號',command=copyinKA)#點擊後複製工卡號 
            menu.post(event.x_root, event.y_root)
        newtv.bind('<Button-3>', copyEKA) #雙擊出現複製選單
        newtv.place(relheight=0.995, relwidth=0.995)

    
class waitGraph(tk.Toplevel):
     def __init__(self, parent,controller):
        tk.Toplevel.__init__(self, parent, bg="#BEB2A7")
        
        self.title('待加工走勢圖')
        self.resizable(0, 0) #prevents the app from being resized
        self.geometry("815x530+50+20") #fixes the applications size
        self.iconbitmap('LC.ico')
        
        var = tk.StringVar()
        var.set('走勢圖')
        frame1 = tk.LabelFrame(self, frame_styles, text=var.get())
        frame1.place(relx=0.127, rely=0.02, height=500, width=700)
        frame2 = tk.LabelFrame(self, frame_styles, text="選擇站點")
        frame2.place(relx=0.02, rely=0.02, height=320, width=83)
        
        f = Figure(figsize=(5, 4), dpi=100)
        f_plot = f.add_subplot(111)
        canvs = FigureCanvasTkAgg(f, frame1)
        canvs.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)       
        
        
        m = len(parent.allstatic)
        n = len(parent.timelist)
        graphdata = np.zeros((m,n))
        for j,t in enumerate(parent.timelist):
            for i,s in enumerate(parent.allstatic):
                graphdata[i,j] = sum([d[2] for d in s.inner if d[3][j]])
        

        #製作各繪圖函數
        t64list = [np.datetime64(i) for i in parent.timelist]
        class gif:
            def __init__(self,vec,title):
                self.vec = vec
                self.title = title
            def plot(self):
                f_plot.clear()
                f_plot.plot(t64list, self.vec)
                f_plot.set_ylabel('To be produced(Kg)')
                f_plot.set_title(self.title)
                cdf = mpl.dates.ConciseDateFormatter(f_plot.xaxis.get_major_locator())
                f_plot.xaxis.set_major_formatter(cdf)
                canvs.draw()
        chs = step_ch+['全廠']
        ens = step_en+['All Clothes']
        stepdict={}
        for i,s in enumerate(chs):
            stepdict[s] = gif(graphdata[i],ens[i])
        
        A = [stepdict[i].plot for i in chs]
        B = [s.name for s in parent.allstatic]
        for i,(a,b) in enumerate(zip(A[:11],B[:11])):
            tk.Button(frame2, text=b,width=4,command=a).grid(column=0,row=i,sticky='ew')
        for i,(a,b) in enumerate(zip(A[11:],B[11:])):
            tk.Button(frame2, text=b,width=4,command=a).grid(column=1,row=i,sticky='ew')