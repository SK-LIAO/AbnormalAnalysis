# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 08:10:00 2022

@author: A90127
"""
import numpy as np
import tkinter as tk
from tkinter import filedialog,ttk
from datetime import datetime, time

import dataBuild as dB

from app_GUI import GUI
from readme import frame_styles
from renewUrgent import renewUrgent


class urgentbdPage(GUI):  # 繼承GUI
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        self.name = 'urgentPage'

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
            inds = [list(head).index(ch) for ch in ('染單','重切交期')]
            for grid in urgent[:,inds].flatten():
                if not dB.isdata(grid):
                    tk.messagebox.showerror(title='錯誤', message='必要欄位有空白，請補充資料後重新匯入')
                    Label2['fg'] = '#FF0000'
                    Label2['text'] = '檔案匯入失敗'
                    controller.urgent=np.array([[]])
                    return
            #檢驗交其是否符合日期格式
            for i,grid in enumerate(urgent[:,inds[1]]):
                try:
                    urgent[i,inds[1]] = datetime.combine(grid,time())
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
            
