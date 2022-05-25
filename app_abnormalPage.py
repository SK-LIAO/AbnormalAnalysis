# -*- coding: utf-8 -*-
"""
Created on Thu May  5 14:48:34 2022

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


import abnormalAnaly as aA
from app_GUI import GUI
from readme import frame_styles, step_en, step_ch,step_air
from tkcalendar import DateEntry #日曆模組

class abnormalPage(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        
        frame1 = tk.LabelFrame(self, frame_styles, text="分析結果")
        frame1.place(relx=0.3, rely=0.02, height=550, width=600)
        frame2 = tk.LabelFrame(self, frame_styles, text="生產走勢")
        frame2.place(relx=0.1, rely=0.02, height=550, width=202)
        frame3 = tk.LabelFrame(frame2, frame_styles, text="生產異常統計")
        frame3.place(relx=0.01, rely=0.27, height=383, width=192)
        
        tv1 = ttk.Treeview(frame1,selectmode='browse')#建立資料數
        column_list_account = ['生產站點','生產量(kg)','異常量(kg)','百分比(%)']
        tv1['columns'] = column_list_account # 資料表頭
        tv1["show"] = "headings"  # 移除第一空白行
        for column in column_list_account:
            tv1.heading(column, text=column)
            tv1.column(column, width=140)
        def checkdata(*args):
            abnormalCheck(self, controller, tv1)
        tv1.bind('<Double-1>', checkdata) #雙擊檢視詳細資料
        tv1.place(relheight=0.995, relwidth=0.995)
        
            
        self.var1 = tk.IntVar()
        Radiobutton1 = tk.Radiobutton(frame2,text='斗工(水)',variable=self.var1,value=0)
        Radiobutton2 = tk.Radiobutton(frame2,text='雲科(氣)',variable=self.var1,value=1)
        Radiobutton1.grid(column=0,row=0,sticky='ew')
        Radiobutton2.grid(column=1,row=0,sticky='w')
        self.var1.set(0)
        
        Label1 = tk.Label(frame2,text='日期(起)')
        Label1.grid(column=0,row=1,sticky='ew')
        Button1_1 = DateEntry(frame2, width=13, background='darkblue',
                    foreground='white', borderwidth=3)
        Button1_1.set_date(datetime.now()-timedelta(days=1))
        Button1_1.grid(column=1,row=1,sticky='w')
        
        
        Label2 = tk.Label(frame2,text='日期(迄)')
        Label2.grid(column=0,row=2,sticky='ew')
        Button2_1 = DateEntry(frame2, width=13, background='darkblue',
                    foreground='white', borderwidth=3)
        Button2_1.grid(column=1,row=2,sticky='w')
        
        Label5 = tk.Label(frame2,text='指定型體')
        Label5.grid(column=0,row=3,sticky='ew')
        self.var4 = tk.StringVar()
        self.var4.set('')
        self.Entry5_1 = tk.Entry(frame2,textvariable=self.var4,width=17)
        self.Entry5_1.grid(column=1,row=3,sticky='w')
        
        button3 = tk.Button(frame2,text="繪製圖表", command = lambda: graph())
        button3.grid(column=0,row=4,sticky='ew')
        
        Label3 = tk.Label(frame3,text='NG類型')
        Label3.grid(column=0,row=1,sticky='ew')
        self.var2 = tk.StringVar()
        self.Combobox3_1 = ttk.Combobox(frame3,textvariable=self.var2,
                                   values = ['效能/結果','效能/原因','品管/結果','品管/原因'],
                                   width=13,state="readonly")
        self.Combobox3_1.current(0)
        self.Combobox3_1.grid(column=1,row=1,sticky='ew')
        
        Label4 = tk.Label(frame3,text='已結案')
        Label4.grid(column=0,row=2,sticky='ew')
        self.var3 = tk.StringVar()
        self.Combobox4_1 = ttk.Combobox(frame3,textvariable=self.var3,
                                   values = ['否','是'],width=13,state="readonly")
        self.Combobox4_1.current(1)
        self.Combobox4_1.grid(column=1,row=2,sticky='w')
        
        button1 = tk.Button(frame3,text="各站統計", command = lambda: each())
        button1.grid(column=0,row=3,sticky='ew')
        button2 = tk.Button(frame3,text="全站統計", command = lambda: total())
        button2.grid(column=0,row=4,sticky='ew')
        
        
        def graph():
            a = datetime.combine(Button1_1.get_date(),time())
            b = datetime.combine(Button2_1.get_date(),time())
            ds = (b-a).days
            self.timelist = [a + timedelta(days=i) for i in range(ds)]
            specific = self.var4.get()
            self.allstatic = aA.prodGraph(a,b,controller.data,specific,self.var1.get())
            abnormalGraph(self,controller)
            
        self.static = 0
        def each():
            Refresh()
            a = datetime.combine(Button1_1.get_date(),time())
            b = datetime.combine(Button2_1.get_date(),time())
            ds = (b-a).days
            NGtype = '效能' if self.var2.get()[:2]=='效能' else '品管'
            NGtypeClass = 0 if self.var2.get()[-2:]=='結果' else 1
            finish = True if self.var3.get()=='是' else False
            specific = self.var4.get()
            self.static = aA.stepStatic(a,controller.data,ds,NGtype,NGtypeClass,finish,
                                        specific,'',True,self.var1.get())
            data =[ [s.name, 
                    round(sum([i[2] for i in s.inner]),1),
                    round(sum([i[2] for i in s.abnormal]),1),
                    round(100*sum([i[2] for i in s.abnormal])/(sum([i[2] for i in s.inner])+0.001),1)] for s in self.static] 
            for row in data:
                tv1.insert("", 'end', values=row)
            
        def total():
            Refresh()
            a = datetime.combine(Button1_1.get_date(),time())
            b = datetime.combine(Button2_1.get_date(),time())
            ds = (b-a).days
            NGtype = '效能' if self.var2.get()[:2]=='效能' else '品管'
            NGtypeClass = 0 if self.var2.get()[-2:]=='結果' else 1
            finish = True if self.var3.get()=='是' else False
            specific = self.var4.get()
            self.static = aA.totalStatic(a,controller.data,ds,NGtype,NGtypeClass,finish,
                                         specific,'',True,self.var1.get())
            data =[ [s.name, 
                    round(sum([i[2] for i in s.inner]),1),
                    round(sum([i[2] for i in s.abnormal]),1),
                    round(100*sum([i[2] for i in s.abnormal])/(sum([i[2] for i in s.inner])+0.001),1)] for s in self.static] 
            for row in data:
                tv1.insert("", 'end', values=row)
            
        #    for row in controller.data[:50]:
        #        tv1.insert("", 'end', values=list(row))
            
        def Refresh():
            tv1.delete(*tv1.get_children())  # *=splat operator
            
class abnormalCheck(tk.Toplevel):
    def __init__(self, parent,controller,tv):
        tk.Toplevel.__init__(self, parent, bg="#BEB2A7")
    
        self.title('詳細資料')
        self.resizable(0, 0) #prevents the app from being resized
        self.geometry("780x300+100+20") #fixes the applications size
        self.iconbitmap('LC.ico')
        
        for item in tv.selection():
            item_text = tv.item(item,"values")
        frame1 = tk.LabelFrame(self,frame_styles,text=item_text[0]+"異常統計")
        frame1.place(relx=0.02,rely=0.02,height=280,width=300)
        frame2 = tk.LabelFrame(self,frame_styles,text=item_text[0]+"異常工卡")
        frame2.place(relx=0.41,rely=0.02,height=280,width=445)
        column_list_account1 = ['類別','重量(kg)','比例(%)']
        column_list_account2 = ['工卡號','指染單號','類別','重量(kg)']
        tv1 = ttk.Treeview(frame1,columns=column_list_account1,show="headings",selectmode='none')
        tv2 = ttk.Treeview(frame2,columns=column_list_account2,show="headings",selectmode='browse')
        for column in column_list_account1:
            tv1.heading(column, text=column) 
            tv1.column(column, width=100)
        for s in parent.static:
            if s.name == item_text[0]:
                NG = aA.NGanaly((s.inner,s.abnormal),ra=True)
                allmass = round(sum([i[2] for i in s.abnormal]),1)
                break
        ytreescroll = tk.Scrollbar(frame2)
        ytreescroll.configure(command=tv2.yview)
        tv2.configure(yscrollcommand=ytreescroll.set)
        ytreescroll.pack(side="right", fill="y")
        for column in column_list_account2:
            tv2.heading(column, text=column)
            tv2.column(column, width=100)
        for s in NG:
            mass = round(sum([i[2] for i in s.inner]),1)
            tv1.insert('','end',values=[s.name,mass,round(mass/(allmass+0.001)*100,1)])
            for i in s.inner:
                tv2.insert("", 'end', values=(i[0],i[1],s.name,i[2]))
        tv1.place(relheight=0.995, relwidth=0.995)
        def copyEKA(event):
            menu = tk.Menu(parent,tearoff=0)
            def copyinE():
                for item  in tv2.selection():
                    item_text = tv2.item(item,"values")
                card = item_text[0]
                copy(card)
            def copyinKA():
                for item  in tv2.selection():
                    item_text = tv2.item(item,"values")
                card = item_text[1]
                copy(card)
            menu.add_command(label='複製工卡號',command=copyinE) #點擊後複製工卡號
            menu.add_command(label='複製指染單號',command=copyinKA)
            menu.post(event.x_root, event.y_root)
        tv2.bind('<Button-3>', copyEKA) #右鍵單擊出現複製選單
        tv2.place(relheight=0.995, relwidth=0.995)
        
class abnormalGraph(tk.Toplevel):
    def __init__(self, parent,controller):
        tk.Toplevel.__init__(self, parent, bg="#BEB2A7")
        
        self.title('生產走勢圖')
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
        if parent.var1.get()==0:
            chs = ['開卡']+step_ch
            ens = ['New Cards']+step_en
        else:
            chs = ['NEW'] + step_air
            ens = ['New Cards'] + step_air
        #加工站點數
        m = len(parent.allstatic)
        #日期天數
        n = len(parent.timelist)
        graphdata = np.zeros((m,n))
        for j,t in enumerate(parent.timelist):
            for i,s in enumerate(parent.allstatic):
                graphdata[i,j] = sum([d[2] for d in s.inner if d[3]==j])
        t64list = [np.datetime64(i) for i in parent.timelist]
        

        #製作各繪圖函數
        class gif:
            def __init__(self,vec,title):
                self.vec = vec
                self.title = title
            def plot(self):
                f_plot.clear()
                #可以考慮過濾掉放假日的產值,但加班日不好考慮
                dm = np.array([[d1,m] for d1, m, d2 in zip(t64list,self.vec,parent.timelist) if d2.weekday() not in [6]])
                f_plot.plot(list(dm[:,0]), dm[:,1])
                f_plot.set_ylabel('To be produced(Kg)')
                f_plot.set_title(self.title)
                cdf = mpl.dates.ConciseDateFormatter(f_plot.xaxis.get_major_locator())
                f_plot.xaxis.set_major_formatter(cdf)
                canvs.draw()
        stepdict={}
        for i,s in enumerate(chs):
            stepdict[s] = gif(graphdata[i],ens[i])
        
        A = [stepdict[i].plot for i in chs]
        B = [s.name for s in parent.allstatic]
        for i,(a,b) in enumerate(zip(A[:11],B[:11])):
            tk.Button(frame2, text=b,width=4,command=a).grid(column=0,row=i,sticky='ew')
        for i,(a,b) in enumerate(zip(A[11:],B[11:])):
            tk.Button(frame2, text=b,width=4,command=a).grid(column=1,row=i,sticky='ew')