# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 13:07:08 2021

@author: A90127
"""
'''
注意:
1.因為工卡開立時間數據只有日期數據,沒有時間數據,因此開立時間都當成是開卡日期的早上8:01
2.生管0:00~8:00不上班
'''
 
import numpy as np
from datetime import datetime, timedelta

from stepAnaly import myStrptime, isdata
from readme import step_ch
#急件工時預估字典、仔細做的話應該要是函數
from mydict import Urgentdict

              
    #統計在某個特定時間點存放的工卡總量
    #輸入 月m(7~9)、日d(1~31)、時hr(0~23) 回傳各站點: 待加工卡 重量 剩餘工作天數 
def stepStatic(dati,data,specific='',restep='',ra=False):
    #拉出特定品項數據資料
    if len(specific)>0:
        data = np.array([d for d in data if specific == d[5]])
    #拿掉作廢工卡資料 和 在時間點後所開出的工卡 
    tsearch = dati
    data = np.array([d for d in data if d[3]!='作廢' and myStrptime(d[1],805)<=tsearch])
    class steps:
        inner = []
        def __init__(self,name):
            self.name = name
            self.inner = []
            steps.inner +=  [self]           
    chs = step_ch + ['全廠']
    stepdict = {}
    for ch in chs:
        stepdict[ch] = steps(ch)
    
    def classify(mat):
        tnow = myStrptime(mat[0,1],805)
        for i,d in enumerate(mat):
            if tnow:
                if isdata(d[7]) and isdata(d[8]):
                    tnext = myStrptime(d[7],d[8])
                    if tnow<=tsearch<tnext:
                        #估計剩餘工作天數期望值,標準差
                        leftmean = round(sum([Urgentdict[ch][0] for ch in mat[i:,6]]),2)
                        leftstd = round(sum([Urgentdict[ch][1] for ch in mat[i:,6]]),2)
                        stepdict[d[6]].inner += [ [d[0],d[2],d[4],leftmean,leftstd] ]
                elif d[3] not in ['結案','強迫結案']:
                    tnext = ''
                    if tnow<=tsearch:
                        #估計剩餘工作天數
                        leftmean = round(sum([Urgentdict[ch][0] for ch in mat[i:,6]]),2)
                        leftstd = round(sum([Urgentdict[ch][1] for ch in mat[i:,6]]),2)
                        stepdict[d[6]].inner += [ [d[0],d[2],d[4],leftmean,leftstd] ]
                tnow = tnext
            else:
                break
    #統計工卡
    i0 = 0
    card = data[0,0]
    for i,d in enumerate(data):
        if d[0] != card:
            classify(data[i0:i])
            i0 = i
            card = d[0]
    classify(data[i0:])

    #全廠不能重複計算
    for s in steps.inner[:-1]:
        stepdict['全廠'].inner += s.inner
    if ra:
        return steps.inner
    for s in steps.inner:
        if restep == s.name:
            return s.inner
    else:
        for s in steps.inner:
            print(s.name+'待加工: ',round(sum([i[2] for i in s.inner]),1),'kg ',len(s.inner),'卡')       
               
#給定數據data 回傳在時間起timestart 迄timeend內
#各個加工站點內待加工的 工卡號 重量 時間點是否存在的bool序列
def staticGraph(timestart,timeend,data,specific=''):   
    #拉出特定品項數據資料
    if len(specific)>0:
        data = np.array([d for d in data if specific == d[5]])
    #拿掉作廢工卡資料 和 在時間範圍後所開出的工卡       
    data = np.array([d for d in data if d[3]!='作廢' and myStrptime(d[1],805)<=timeend])
    class steps:
        inner = []
        def __init__(self,name):
            self.name = name
            self.inner = []
            steps.inner +=  [self]           
    chs = step_ch + ['全廠']
    stepdict = {}
    for ch in chs:
        stepdict[ch] = steps(ch)

    dt = timeend - timestart
    n_hrs = int(dt.days*24 + dt.seconds/60/60)
    timelist = [timestart+timedelta(hours=i) for i in range(n_hrs)]
    def classify(mat):
        #建立開卡時間
        tnow = myStrptime(mat[0,1],805)
        #建立有刷卡紀錄站點
        testmat = [d for d in mat if isdata(d[7]) and isdata(d[8])]
        if len(testmat)==0 or mat[0,3] not in ['結案','強迫結案']:
            tend = datetime.now()
        else:
            t, ch = np.array(testmat)[-1][7:9]
            tend = myStrptime(t,ch)        
        
        mark = np.zeros(n_hrs)
        for i,t in enumerate(timelist):
            if tnow<=t<tend:
                mark[i] = 1
        if sum(mark)>0:
            stepdict['全廠'].inner += [ [mat[0,0],mat[0,2],mat[0,4],mark] ]
   
        for d in mat:
            mark = np.zeros(n_hrs)
            if tnow:
                if isdata(d[7]) and isdata(d[8]):
                    tnext = myStrptime(d[7],d[8])
                    for i,t in enumerate(timelist):
                        if tnow<=t<tnext:
                            mark[i] = 1
                    if sum(mark)>0:
                        stepdict[d[6]].inner += [ [d[0],d[2],d[4],mark] ]

                elif d[3] not in ['結案','強迫結案']:
                    tnext = ''
                    for i,t in enumerate(timelist):
                        if tnow<=t:
                            mark[i] = 1
                    if sum(mark)>0:
                        stepdict[d[6]].inner += [ [d[0],d[2],d[4],mark] ]
                tnow = tnext
            else:
                break
    
    #統計工卡
    i0 = 0
    card = data[0,0]
    for i,d in enumerate(data):
        if d[0] != card:
            classify(data[i0:i])
            card = d[0]
            i0 = i
    classify(data[i0:])
    '''
    #print統計數據
    for i, t in enumerate(timelist):
        print('時間: ' + t.strftime("%m/%d/%Y, %H:%M:%S"))
        for s in steps.inner:
            m = sum([d[1] for d in s.inner if d[2][i]])
            print(s.name+'待加工: {:.1f}kg'.format(m))
        print('\n')
    '''   
    return steps.inner
            