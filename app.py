# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 13:58:12 2021

@author: A90127
"""

import tkinter as tk
import numpy as np

import matplotlib as mpl

from pyperclip import copy
from datetime import datetime, timedelta, time
from tkinter import filedialog
from tkinter import ttk
from tkcalendar import DateEntry #日曆模組
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


import dataBuild as dB
import abnormalAnaly as aA
import waitAnaly as wA
import stepAnaly as sA

from readme import RM, frame_styles, step_en, step_ch
from renewUrgent import renewUrgent


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
        
        
        pages = (databdPage,urgentbdPage,
                 abnormalPage, waitPage, stepPage, authorPage)
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
    
        
class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        menu_file = tk.Menu(self, tearoff=0)
        self.add_cascade(label="檔案", menu=menu_file)
        menu_file.add_command(label="匯入資料", command=lambda: parent.show_frame(databdPage))
        
        menu_file.add_command(label="匯入急件", command=lambda: parent.show_frame(urgentbdPage))
        menu_file.add_separator() #分隔線
        menu_file.add_command(label="離開", command=lambda: parent.Quit_application())

        menu_analysis = tk.Menu(self, tearoff=0)
        self.add_cascade(label="分析", menu=menu_analysis)
        menu_analysis.add_command(label='生產異常', command=lambda: parent.show_frame(abnormalPage))
        menu_analysis.add_command(label='待加工', command=lambda: parent.show_frame(waitPage))
        menu_analysis.add_command(label='站點工時', command=lambda: parent.show_frame(stepPage))

        menu_expression = tk.Menu(self, tearoff=0)
        self.add_cascade(label="說明", menu=menu_expression)
        menu_expression.add_command(label="關於App", command=lambda: parent.show_frame(authorPage))

                
            
class GUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.main_frame = tk.Frame(self, bg="#BEB2A7", height=600, width=1024)
        # self.main_frame.pack_propagate(0)
        self.main_frame.pack(fill="both", expand="true")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)


class databdPage(GUI):  # inherits from the GUI class
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
       
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
           
        

class urgentbdPage(GUI):  # inherits from the GUI class
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)

        frame1 = tk.LabelFrame(self, frame_styles, text="急件數據瀏覽")
        frame1.place(relx=0.1, rely=0.02, height=450, width=800)

        frame2 = tk.LabelFrame(self, frame_styles, text="匯入")
        frame2.place(relx=0.1, rely=0.77, height=105, width=800)

        button1 = tk.Button(frame2, text="選擇檔案", command=lambda: Load_path(self))
        button1.grid(column=0,row=0)
        button2 = tk.Button(frame2, text="匯入資料", command=lambda: Load_data(self))
        button2.grid(column=0,row=1)
        button3 = tk.Button(frame2, text="更新檔案", command=lambda: Renew_data(self))
        button3.grid(column=0,row=2)
        Label1 = tk.Label(frame2,text='',width=100)
        Label1.grid(column=1,row=0)
        Label2 = tk.Label(frame2,text='',width=100)
        Label2['fg'] = '#0000FF'
        Label2.grid(column=1,row=1)
        Label3 = tk.Label(frame2,text='',width=100)
        Label3['fg'] = '#0000FF'
        Label3.grid(column=1,row=2)
        
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
            urgent, head = dB.urgentBuild(self.path)
            #檢驗欄位是否重複
            if len(head)>len(set(head)):
                tk.messagebox.showerror(title='錯誤', message='該檔案欄位重複，請修改後重新匯入')
                Label2['fg'] = '#FF0000'
                Label2['text'] = '檔案匯入失敗'
                controller.urgent=np.array([[]])
                return
            #檢驗是否有必備欄位
            test1 = [ch for ch in ('染單','需完成下染量','重切交期') if ch not in head]
            if len(test1)>0:
                tk.messagebox.showerror(title='錯誤', message='該檔案缺少: '+','.join(test1)+' 欄位，請修改後重新匯入')
                Label2['fg'] = '#FF0000'
                Label2['text'] = '檔案匯入失敗'
                controller.urgent=np.array([[]])
                return
            #檢驗染單欄位是否重複
            ind = list(head).index('染單')
            if len(urgent[:,ind])>len(set(urgent[:,ind])):
                tk.messagebox.showerror(title='錯誤', message='染單號碼重複，請修改後重新匯入')
                Label2['fg'] = '#FF0000'
                Label2['text'] = '檔案匯入失敗'
                controller.urgent=np.array([[]])
                return
            #檢驗 '染單','需完成下染量','重切交期' 數據是否有缺少
            inds = [list(head).index(ch) for ch in ('染單','需完成下染量','重切交期')]
            for grid in urgent[:,inds].flatten():
                if not dB.isdata(grid):
                    tk.messagebox.showerror(title='錯誤', message='必要欄位有空白，請補充資料後重新匯入')
                    Label2['fg'] = '#FF0000'
                    Label2['text'] = '檔案匯入失敗'
                    controller.urgent=np.array([[]])
                    return
            #檢驗交其是否符合日期格式
            for i,grid in enumerate(urgent[:,inds[2]]):
                try:
                    urgent[i,inds[2]] = datetime.combine(grid,time())
                except:
                    tk.messagebox.showerror(title='錯誤', message='重切交期數據格式不符,採用格式 year/month/day')
                    Label2['fg'] = '#FF0000'
                    Label2['text'] = '檔案匯入失敗'
                    controller.urgent=np.array([[]])
                    return
            #提示缺少輔助更新欄位、更新時將自動追加欄
            test = [ch for ch in ('下染量','未開卡量','未完成量','進度') if ch not in head]
            if len(test)>0:
                tk.messagebox.showinfo(title='注意', message='該檔案缺少: '+','.join(test)+' 欄位,更新時會自動補充欄位更新')
            controller.urgent, controller.urgent_head = urgent, head
            column_list_account = list(head)
            tv1['columns'] = column_list_account
            for column in column_list_account:
                tv1.heading(column, text=column)
                tv1.column(column, width=140)
            for row in controller.urgent:
                tv1.insert('', 'end', values=list(row))
            Label2['fg'] = '#0000FF'
            Label2['text'] = '檔案已經匯入'
        
        def Renew_data(self):
            Label3['fg'] = '#FF0000'
            Label3.configure(text='資料更新中')
            tk.messagebox.showinfo(title='注意', message='將開啟檔案自動更新、這需要一段時間。')
            renewUrgent(controller.data,controller.head,self.path)
            Label3['fg'] = '#0000FF'
            Label3.configure(text='資料更新完畢')
            
            
        def Refresh_data():
            tv1.delete(*tv1.get_children())  # *=splat operator



class abnormalPage(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        
        frame1 = tk.LabelFrame(self, frame_styles, text="分析結果")
        frame1.place(relx=0.3, rely=0.02, height=550, width=600)
        frame2 = tk.LabelFrame(self, frame_styles, text="生產走勢")
        frame2.place(relx=0.1, rely=0.02, height=550, width=202)
        frame3 = tk.LabelFrame(frame2, frame_styles, text="生產異常統計")
        frame3.place(relx=0.01, rely=0.27, height=382, width=192)
        
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
        
            
        Label1 = tk.Label(frame2,text='日期(起)')
        Label1.grid(column=0,row=0,sticky='ew')
        Button1_1 = DateEntry(frame2, width=13, background='darkblue',
                    foreground='white', borderwidth=3)
        Button1_1.set_date(datetime.now()-timedelta(days=1))
        Button1_1.grid(column=1,row=0,sticky='w')
        
        
        Label2 = tk.Label(frame2,text='日期(迄)')
        Label2.grid(column=0,row=1,sticky='ew')
        Button2_1 = DateEntry(frame2, width=13, background='darkblue',
                    foreground='white', borderwidth=3)
        Button2_1.grid(column=1,row=1,sticky='w')
        
        Label5 = tk.Label(frame2,text='指定型體')
        Label5.grid(column=0,row=2,sticky='ew')
        self.var4 = tk.StringVar()
        self.var4.set('')
        self.Entry5_1 = tk.Entry(frame2,textvariable=self.var4,width=19)
        self.Entry5_1.grid(column=1,row=2,sticky='nsw')
        
        button3 = tk.Button(frame2,text="繪製圖表", command = lambda: graph())
        button3.grid(column=0,row=3)
        
        Label3 = tk.Label(frame3,text='NG類型')
        Label3.grid(column=0,row=0,sticky='ew')
        self.var2 = tk.StringVar()
        self.Combobox3_1 = ttk.Combobox(frame3,textvariable=self.var2,
                                   values = ['效能/結果','效能/原因','品管/結果','品管/原因'],
                                   width=13,state="readonly")
        self.Combobox3_1.current(0)
        self.Combobox3_1.grid(column=1,row=0,sticky='w')
        
        Label4 = tk.Label(frame3,text='已結案')
        Label4.grid(column=0,row=1,sticky='ew')
        self.var3 = tk.StringVar()
        self.Combobox4_1 = ttk.Combobox(frame3,textvariable=self.var3,
                                   values = ['是','否'],width=13,state="readonly")
        self.Combobox4_1.current(1)
        self.Combobox4_1.grid(column=1,row=1,sticky='w')
        
        button1 = tk.Button(frame3,text="各站統計", command = lambda: each())
        button1.grid(column=0,row=2)
        button2 = tk.Button(frame3,text="全站統計", command = lambda: total())
        button2.grid(column=0,row=3)
        
        
        def graph():
            a = datetime.combine(Button1_1.get_date(),time())
            b = datetime.combine(Button2_1.get_date(),time())
            ds = (b-a).days
            self.timelist = [a + timedelta(days=i) for i in range(ds)]
            specific = self.var4.get()
            self.allstatic = aA.prodGraph(a,b,controller.data,specific)
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
            self.static = aA.stepStatic(a,controller.data,ds,NGtype,NGtypeClass,finish,specific,'',ra=True)
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
            self.static = aA.totalStatic(a,controller.data,ds,NGtype,NGtypeClass,finish,specific,'',ra=True)
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

class stepPage(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)

        frame1 = tk.LabelFrame(self, frame_styles, text="分析結果")
        frame1.place(relx=0.33, rely=0.02, height=550, width=576)
        frame2 = tk.LabelFrame(self, frame_styles, text="共同參數")
        frame2.place(relx=0.1, rely=0.02, height=550, width=227)
        frame3 = tk.LabelFrame(frame2, frame_styles, text="計算前後站點比例")
        frame3.place(relx=0.02, rely=0.095, height=100, width=213)
        frame4 = tk.LabelFrame(frame2, frame_styles, text="總加工時間統計")
        frame4.place(relx=0.02, rely=0.3, height=365, width=213)
        frame5 = tk.LabelFrame(frame4, frame_styles, text="各站加工時間統計")
        frame5.place(relx=0.02, rely=0.16, height=284, width=200)
        frame6 = tk.LabelFrame(frame5, frame_styles, text="查詢滯留工卡")
        frame6.place(relx=0.02, rely=0.3, height=179, width=187)
        
        
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
            menu.add_command(label='複製欄位1',command=copyinE) #點擊後複製工卡號
            menu.add_command(label='複製欄位2',command=copyinKA)
            menu.post(event.x_root, event.y_root)
        tv1.bind('<Button-3>', copyEKA) #右鍵單擊出現複製選單
        
        tv1.place(relheight=0.995, relwidth=0.995)
        #設定y軸滑桿
        ytreescroll = tk.Scrollbar(frame1)
        ytreescroll.configure(command=tv1.yview)
        tv1.configure(yscrollcommand=ytreescroll.set)
        ytreescroll.pack(side="right", fill="y")           
        
        pm = datetime.now()-timedelta(days=30)            
        Label1 = tk.Label(frame2,text='日期(起)')
        Label1.grid(column=0,row=0,sticky='ew')
        Button1_1 = DateEntry(frame2, width=13, background='darkblue',
                    foreground='white', borderwidth=3,
                    year=pm.year, month=pm.month, day=pm.day)
        Button1_1.grid(column=1,row=0,sticky='w')
        
        Label2 = tk.Label(frame2,text='日期(迄)')
        Label2.grid(column=0,row=1,sticky='ew')
        Button2_1 = DateEntry(frame2, width=13, background='darkblue',
                    foreground='white', borderwidth=3)
        Button2_1.grid(column=1,row=1,sticky='w')
        
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
        steps = ['胚倉','前定','前品','染色','中檢','定型','品驗','對色','驗布', '烘乾',
         '配布','精煉','釘邊','中檢2','品驗2','驗布2','烘乾2','包裝']
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
            
        def each():
            Refresh()
            Retitle(['生產站點','平均時間(天)','標準差(天)'])
            startdate = datetime.combine(Button1_1.get_date(), time())
            enddate = datetime.combine(Button2_1.get_date(),time())
            ds = (enddate-startdate).days            
            specific = self.var3.get()
            self.static = sA.stepStatic(startdate,controller.data,ds,fidict[self.var2.get()],specific,ra=True)
            data =[ [s.name, 
                    round(np.average([i[0]+i[1]/24/60/60 for i in s.dt]),1),
                    round(np.std([i[0]+i[1]/24/60/60 for i in s.dt]),1)] for s in self.static if len(s.inner)>0] 
            for row in data:
                tv1.insert("", 'end', values=row)
            
        def total():
            Refresh()
            Retitle(['平均時間(天)','標準差(天)'])
            startdate = datetime.combine(Button1_1.get_date(), time())
            enddate = datetime.combine(Button2_1.get_date(),time())
            ds = (enddate-startdate).days
            specific = self.var3.get()
            data = sA.avgProdDays(startdate,controller.data,ds,specific,True)
            avg = round(np.average([d[1] for d in data]),1)
            std = round(np.std([d[1] for d in data]),1)
            tv1.insert('', 'end', values=[avg,std])
            

        def maxday():
            startdate = datetime.combine(Button1_1.get_date(), time())
            enddate = datetime.combine(Button2_1.get_date(),time())
            ds = (enddate-startdate).days
            specific = self.var3.get()
            ch = sA.maxProdDays(startdate,controller.data,ds,fidict[self.var2.get()],specific,ra=True)
            self.var5.set(round(ch,1))
            
        def staycard():
            Refresh()
            Retitle(['工卡號','指染單號','滯留天數','是否結案'])
            startdate = datetime.combine(Button1_1.get_date(), time())
            enddate = datetime.combine(Button2_1.get_date(),time())
            ds = (enddate-startdate).days
            stayd = self.var1.get()
            specific = self.var3.get()
            self.static = sA.prodStay(startdate,stayd,controller.data,ds,fidict[self.var2.get()],specific,True)
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


class authorPage(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        
        frame1 = tk.LabelFrame(self, frame_styles, text="開發說明")
        frame1.place(relx=0.15, rely=0.02, height=550, width=750)
        
        
        
        label1 = tk.Label(frame1, font=("Verdana", 12), text=RM,bg='#BEB2A7')
        label1.pack(side="top")

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
        
        chs = ['開卡']+step_ch
        ens = ['New Cards']+step_en
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
                dm = np.array([[d1,m] for d1, m, d2 in zip(t64list,self.vec,parent.timelist) if d2.weekday() not in [5,6]])
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
        
root = MyApp()
root.title("利勤資料分析App")

root.mainloop()