# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 11:54:09 2021

@author: A90127
"""

#import xlwings as xw
import numpy as np
from datetime import datetime, timedelta

from readme import step_ch, step_air
from dataBuild import myStrptime, isdata
'''
#水染加工站
steps = ['胚倉','前定','前品','染色','中檢','定型','品驗','對色','驗布', '烘乾',
         '配布','精煉','釘邊','剝色','配布2','中檢2','品驗2','驗布2','烘乾2','包裝']

#氣染加工站
step_air = ['BO','BW','CP','CT','DC','DI','DI2','DP','HO','HP','OQC','PF','PS','RR','SQC']
'''

#給定起始時間 year年 mon月 day日, 
#分析ds天內所開工卡指定站點step的所有下一站點比例
#ds<=0則考慮資料全工卡
#ra:是否回傳給app
def prodNextStep(dati,Step,data,ds=0,ra=False):
    #拉出指定期間的空卡
    if ds>0:
        t1 = dati
        t2 = dati+timedelta(days=ds)
        data = np.array([i for i in data if t2>myStrptime(i[1])>=t1])
    #抓出所有下一站名稱      
    nexts = [ data[i+1][6] for i, s in enumerate(data[:-1]) if s[6] == Step and s[0]==data[i+1][0]]
    #蒐集下一站集合
    steps = [n for n in set(nexts)]
    #列出下一站統計
    if ra:
        return [ [s,round(sum([1 for n in nexts if s==n])/(len(nexts)+0.0001)*100,2)] for s in steps]
    for s in steps:
        n = sum([1 for n in nexts if s==n])
        print(s+': {:.1f}%'.format(n/len(nexts)*100) )
  
#給定起始時間 year年 mon月 day日, 
#分析ds天內所開工卡指定站點step的所有前一站點比例        
#ds<=0則考慮資料全工卡
#ra:是否回傳給app
def prodBackStep(dati,Step,data,ds=0,ra=False):
    if ds>0:
        t1 = dati
        t2 = dati+timedelta(days=ds)
        data = np.array([d for d in data if t2>myStrptime(d[1])>=t1])
    backs = [ data[i-1][6] for i, s in enumerate(data) if s[6] == Step and s[0]==data[i-1][0]]
    steps = [n for n in set(backs)]
    if ra:
        return [ [s,round(sum([1 for n in backs if s==n])/(len(backs)+0.0001)*100,2)] for s in steps]
    for s in steps:
        n = sum([1 for n in backs if s==n])
        print(s+': {:.1f}%'.format(n/len(backs)*100) )



#給定起始時間 year年 mon月 day日, 
#分析ds天內所開工卡(若ds<=0則考慮資料全工卡),停留最長的時間
#finish: 是否結案 
#specific: 指定品項名稱(預設不指定)
#ra: 是否回傳給app 
def maxProdDays(dati,data,ds=0,finish=0,specific='',ra=False,factor=0):
    #只拉斗工廠工卡數據
    if factor==0: 
        data = np.array([d for d in data if d[0][0]=='E'])
    #只拉雲科廠工卡數據
    else:
        data = np.array([d for d in data if d[0][0]=='P'])
    #刪除作廢工卡
    data = np.array([i for i in data if i[3]!='作廢'])
    if specific != '':
        data = np.array([d for d in data if d[5]==specific])
    if ds>0:
        t1 = dati
        t2 = dati+timedelta(days=ds)
        data = np.array([d for d in data if t2>myStrptime(d[1])>=t1])    
    data1 = np.array([d for d in data if d[3] in ['新增', '核准'] ])
    data2 = np.array([d for d in data if d[3] not in ['新增', '核准'] ])
    #NoneType = type(None)
    try:
        m1 = max([datetime.now()-myStrptime(d[1]).replace(hour=8) for d in data1 if isdata(d[7])])
    except:
        m1 = timedelta()
    try:    
        m2 = max([myStrptime(d[7],d[8])-myStrptime(d[1]).replace(hour=8) for d in data2 if isdata(d[7])])
    except:
        m2 = timedelta()
    
    if finish==0:
        m = m2
    elif finish==1:
        m = m1
    else:
        m = max(m1,m2)
    if ra:
        return m.days+m.seconds/86400
    print('工卡停留最大時間: {.:2f}days'.format(m.days+m.seconds/86400))
#秀出裡加工時間大於x天工卡數
def prodStay(dati,x,data,ds=0,finish=0,specific='',ra=False,factor=0):
    #只拉斗工廠工卡數據
    if factor==0: 
        data = np.array([d for d in data if d[0][0]=='E'])
    #只拉雲科廠工卡數據
    else:
        data = np.array([d for d in data if d[0][0]=='P'])
    
    #刪除作廢工卡
    data = np.array([i for i in data if i[3]!='作廢'])
    #拉出特殊品項工卡
    if specific != '':
        data = [d for d in data if d[5]==specific]
    if ds>0:
        t1 = dati
        t2 = dati+timedelta(days=ds)
        data = np.array([i for i in data if t2>myStrptime(i[1])>=t1])    
    data1 = np.array([d for d in data if d[3] in ['新增', '核准'] ])#未結案工卡
    data2 = np.array([d for d in data if d[3] not in ['新增', '核准'] ])#已結案工卡
    
    #儲存未結案工卡的加工時間
    CD1 = []
    tem = ''
    now = datetime.now()
    for d in data1:
        if d[0] != tem:
            m = now-myStrptime(d[1]).replace(hour=8)
            dt = round(m.days+m.seconds/(24*60*60),1)
            CD1 += [ (d[0],d[2],dt,'未結案') ]
            tem = d[0]

    #儲存已結案工卡站點加工時間序列
    CDs2 = []
    for d in data2:
        if isdata(d[7]) and isdata(d[8]):
            st = myStrptime(d[1]).replace(hour=8)
            et = myStrptime(d[7],d[8])
            dt = round((et-st).days+(et-st).seconds/(24*60*60))
            CDs2 += [ (d[0],d[2],dt,'已結案') ]
    
    #儲存已結案工卡的加工時間序列 拉出工卡加工時間
    tem = CDs2[0][0]
    CD2 = []
    for i, cd in enumerate(CDs2):
        if cd[0] != tem:
            CD2 += [ CDs2[i-1] ]
            tem = cd[0]
    CD2 += [ CDs2[-1] ]
    
    if finish==0:
        CD = CD2
    elif finish==1:
        CD = CD1
    else:
        CD = CD2+CD1
    if ra:
        return [d for d in CD if d[2]>x]
    else:
        for d in CD:
            if d[2]>x:
                print(d[0],d[1],'滯留',round(d[2],1),'天 ',d[3])
        print('共{}卡'.format(len([d for d in CD if d[2]>x])))
    
#計算給定時間 year month day 數據 data,統計ds(預設1)天內且順利(即轉卡不計算)包裝完成工卡的
#1.總加工時間的平均值 2.總加工時間的標準差     
#specific: 指定品項(預設無指定)
def avgProdDays(dati,data,ds=0,specific='',re=False,factor=0):
    #只拉斗工廠工卡數據
    if factor==0: 
        data = np.array([d for d in data if d[0][0]=='E'])
    #只拉雲科廠工卡數據
    else:
        data = np.array([d for d in data if d[0][0]=='P'])
    #刪除作廢工卡
    data = np.array([d for d in data if d[3]!='作廢'])
    #拉出特定品項數據資料
    if specific != '':
        data = np.array([d for d in data if specific == d[5]])
    #選取時間內資料
    if ds>0:
        t1 = dati
        t2 = dati+timedelta(days=ds)
        data = np.array([d for d in data if t2>myStrptime(d[1])>=t1])
    #只考慮結案工卡
    data = np.array([d for d in data if d[3] not in ['新增', '核准'] ])
    #儲存有加工時間的數據列 工卡名稱欄 與 (加工時間欄-開卡時間欄)
    CDs = []
    for d in data:
        #只統計有做到包裝的站點且非轉卡
        if isdata(d[7]) and isdata(d[8]) and d[6] in ['包裝','PF'] and len(d[0])==10:
            st = myStrptime(d[1],800)
            et = myStrptime(d[7],d[8])
            CDs += [ (d[0],(et-st).days+(et-st).seconds/(24*60*60)) ]
    SD = np.array([cd[1] for cd in CDs])
    if re:
        return CDs
    else:
        print('每張工卡加工時間\n平均    {:.1f}天\n標準差  {:.1f}天'.format(np.average(SD),np.std(SD)))
#計算給定時間 year month day 數據 data,統計ds(預設1)天內所開工卡的各站點
#1.停留時間的平均值 2.停留時間的標準差   
def stepStatic(dati,data,ds=0,finish=0,specific='',ra=False,factor=0):
    #只拉斗工廠工卡數據
    if factor==0: 
        data = np.array([d for d in data if d[0][0]=='E'])
    #只拉雲科廠工卡數據
    else:
        data = np.array([d for d in data if d[0][0]=='P'])
    #拉出特定品項數據資料
    if specific != '':
        data = np.array([d for d in data if specific == d[5]])
    class steps:
        inner = []
        def __init__(self,name):
            self.name = name
            self.inner = [] #生產工卡
            self.dt = []
            steps.inner +=  [self]
    if factor == 0:
        stepname = step_ch
    else:
        stepname = step_air
    stepdict={}
    for ch in stepname:
        stepdict[ch] = steps(ch)
    
    #刪除作廢工卡 且 拉出有加工時間紀錄數據列
    data = np.array([d for d in data if d[3]!='作廢' and isdata(d[7]) and isdata(d[8])])     
    #選取時間內資料已經加工過
    if ds>0:
        t1 = dati
        t2 = dati+timedelta(days=ds)
        data = np.array([d for d in data if t2>myStrptime(d[1])>=t1])
    #只考慮已完成工卡
    if finish==0:
        data = np.array([d for d in data if d[3] not in ['新增', '核准'] ])
    #只考慮未完成工卡
    elif finish==1:
        data = np.array([d for d in data if d[3] in ['新增', '核准'] ])
    #已完成、未完成同時考慮
    else:
        pass
    tem = ''    
    for i,d in enumerate(data):
        if tem != d[0]:
            bt = myStrptime(d[1],805)
            et = myStrptime(d[7],d[8])
            dt = et-bt
            tem = d[0]
        else:
            bt = myStrptime(data[i-1,7],data[i-1,8])
            et = myStrptime(d[7],d[8])
            dt = et-bt
        stepdict[d[6]].inner += [ d[0] ]
        stepdict[d[6]].dt += [ [dt.days,dt.seconds] ]
        
    if ra:
        return steps.inner
    else:
        tt = []
        print('各站點停留時間')
        for s in steps.inner:
            if s.dt:
                avg = np.average([i[0]+i[1]/(24*60*60) for i in s.dt])
                std = np.std([i[0]+i[1]/(24*60*60) for i in s.dt])
                print('{}: 平均 {:.1f}天, 標準差: {:.1f}天'.format(s.name,avg,std))
                tt += [avg]
    #print('平均總共: {:.1f}天'.format(sum(tt)))

#抓出時間序列錯誤個工卡、未加入app
def timeBug(dati,data,ds=1):
    #選取時間內資料
    t1 = dati
    t2 = dati+timedelta(days=ds)
    data = np.array([d for d in data if t2>myStrptime(d[1])>=t1 and d[3]!='作廢'])
    #選取已經加工過工卡
    data = np.array([d for d in data if isdata(d[11])])
    #print(data.shape)
    tem = ''
    BUG = []
    for i,d in enumerate(data):
        if tem != d[0]:
            bt = myStrptime(d[1],805)
            et = myStrptime(d[7],d[8])
            dt = et-bt
            tem = d[0]
        else:
            #print(data[i-1,11:13])
            bt = myStrptime(data[i-1,7],data[i-1,8])
            et = myStrptime(d[7],d[8])
            dt = et-bt
        if dt.days<0:
            BUG += [(d[0],d[6])]
    return BUG

#急件統計副程式,未加入app
#urgent需具兩欄位 0:急件工卡號,1:升級急件時間
def urgentStepStatic(dati,data,urgent,ds=0,finish=0,specific='',ra=False):
    #拉出特定品項數據資料
    if specific != '':
        data = np.array([i for i in data if specific == i[5]])
    class steps:
        inner = []
        def __init__(self,name):
            self.name = name
            self.inner = [] #生產工卡
            self.dt = []
            steps.inner +=  [self]
    stepdict = {}
    for ch in step_ch:
        stepdict[ch] = steps(ch)
    #刪除作廢工卡 且 拉出有加工時間紀錄數據列
    data = np.array([d for d in data if d[3]!='作廢' and isdata(d[7]) and isdata(d[8])])     
    #選取時間內資料已經加工過
    if ds>0:
        t1 = dati
        t2 = dati+timedelta(days=ds)
        data = np.array([d for d in data if t2>myStrptime(d[1])>=t1])
    if finish==0:
        data = np.array([d for d in data if d[3] not in ['新增', '核准'] ])
    #只考慮未完成工卡
    elif finish==1:
        data = np.array([d for d in data if d[3] in ['新增', '核准'] ])
    #已完成、未完成同時考慮
    else:
        pass
    #拉出急件
    data = np.array([d for d in data if d[0] in urgent[:,0]])
    #拉出急件升級時間起算數據
    data = np.array([d for d in data if urgent[list(urgent[:,0]).index(d[0]),1]<myStrptime(d[7],d[8])])
    tem = ''
    for i,d in enumerate(data):
        if tem != d[0]:
            bt = urgent[list(urgent[:,0]).index(d[0]),0]
            et = myStrptime(d[7],d[8])
            dt = et-bt
            tem = d[0]
        else:
            bt = myStrptime(data[i-1,7],data[i-1,8])
            et = myStrptime(d[7],d[8])
            dt = et-bt
        for s in steps.inner:
            if s.name == d[10]:
                s.inner += [ d[0] ]
                s.dt += [ [dt.days,dt.seconds] ]
    
    if ra:
        return steps.inner
    else:
        tt = []    
        print('各站點停留時間')
        for s in steps.inner:
            if s.dt:
                avg = np.average([i[0]+i[1]/(24*60*60) for i in s.dt])
                std = np.std([i[0]+i[1]/(24*60*60) for i in s.dt])
                print('{}: 平均 {:.1f}天, 標準差: {:.1f}天'.format(s.name,avg,std))
                tt += [avg]
    #print('平均總共: {:.1f}天'.format(sum(tt)))
                    
             
    