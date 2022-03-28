# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 10:34:15 2021

@author: A90127
"""

import numpy as np
from datetime import datetime, timedelta

from dataBuild import  myStrptime, isdata
from mydict import NGdict, NGclass
from readme import step_ch, NG_type1, NG_type2

#統計某日時dati起 ds天內 無效生產量與無效生產率
#finish:是否只考慮已完成工卡
#specific:指定型體品名
#restep:回傳該站點資訊(預設不回傳)
#NGtypeClass(NG類型分類法): 
#       0:依照檢驗結果, ['色差','物性','布面','製程','廠內']
#       1:依照異常原因, ['色差','物性','布面','廠內NG','鞋型不符',
#                        '螢光汙染','色花/色不均','單絲直條/胚布直條','其他']
#ra : 是否回傳app所需資料(GUI 專用)
def stepStatic(dati,data,ds=1,NGtype='效能',NGtypeClass=0,finish=True,specific='',restep='',ra=False):
    class steps:
        inner = []
        def __init__(self,name):
            self.name = name
            self.inner = [] #生產工卡
            self.abnormal = [] #異常工卡
            steps.inner +=  [self]
    
    #中文站點名對應到該站點類
    stepdict = {} 
    for n in step_ch:
        stepdict[n] = steps(n)
    #指定型體品名時資料
    if len(specific)>0:
        data = np.array([i for i in data if specific == i[6]])
        
    #降低資料量,只考慮前後28天以內所開的工卡紀錄,且拿掉作廢工卡
    t1 = dati-timedelta(days=28)
    t2 = dati+timedelta(days=ds+28)
    data = np.array([i for i in data if t2>myStrptime(i[1])>t1 and i[3]!='作廢'])
    
    #只考慮完成的工卡
    if finish:
        data = np.array([i for i in data if i[3] not in ['新增', '核准'] ])
    
    #建立開有異常單資料
    abnormal = np.array([i for i in data if isdata(i[12])])
    
    #要統計範圍的起迄時間
    tmS = dati
    tmE = dati+timedelta(days=ds)
    
    #統計各站點NG
    for i,d in enumerate(data):
        #建立完成時間點(若尚未完成時間設定為當下時間)
        if isdata(d[7]) and isdata(d[8]):
            ct = myStrptime(d[7],d[8])
        else:
            ct = datetime.now()+timedelta(days=ds)
        #只考慮完成時間點在統計時間的起迄範圍內的工卡
        if ct>=tmS and ct<tmE:
            #改站點字典存入生產 工卡號、染單號、開卡種
            stepdict[d[6]].inner += [ [d[0],d[2],d[4]] ]
            if NGtype == '效能':
                e, m, ng = normal1(d[0],d[6],data,abnormal,NGtypeClass)
            else:
                e, m, ng = normal3(d[0],data,abnormal,NGtypeClass)
            if not e:
                #存入異常工卡
                stepdict[d[6]].abnormal += [ [d[0],d[2],m]+ng ]

    if ra:
        return steps.inner
    #show/回傳 統計數據
    for s in steps.inner:
        if s.name == restep:
            return s.inner, s.abnormal
          
    else:
        #輸出無效生產率
        for s in steps.inner:
            a = sum([i[2] for i in s.inner])+0.0001
            b = sum([i[2] for i in s.abnormal])
            print(s.name+'生產量: ',round(a,1),'kg  異常量: ',round(b,1),'kg 佔生產量: ',round(b/a*100,1),'% ')
       

def totalStatic(dati,data,ds=1,NGtype='效能',NGtypeClass=0,finish=True,specific='',restep='',ra=False):
    class steps:
        inner = []
        def __init__(self,name):
            self.name = name
            self.inner = [] #生產工卡
            self.abnormal = [] #異常工卡
            steps.inner +=  [self]
    AL = steps('淨總')
    RE = steps('正規') #扣掉轉卡
    
    #指定型體品名時資料
    if len(specific)>0:
        data = np.array([i for i in data if specific == i[5]])
       
    #抓出範圍內開出的工卡數據
    t1 = dati
    t2 = dati+timedelta(days=ds)
    data = np.array([i for i in data if t2>myStrptime(i[1])>=t1 and i[3]!='作廢'])
    #只考慮完成的工卡
    if finish:
        data = np.array([i for i in data if i[3] not in ['新增', '核准'] ])
    
    #建立開有異常單資料
    abnormal = np.array([i for i in data if isdata(i[12])])
    
    Ecard = ''
    for d in data:
        if Ecard != d[0]:
            AL.inner += [ [d[0],d[2],d[4]] ]
            if NGtype == '效能':
                e, m, ng = normal2(d[0],data,abnormal,NGtypeClass)
            else:
                e, m, ng = normal3(d[0],data,abnormal,NGtypeClass)    
            if not e:
                AL.abnormal += [ [d[0],d[2],d[4]]+ng ]
            if len(d[0])==10:
                RE.inner += [ [d[0],d[2],d[4]] ]
                if NGtype=='效能':
                    e, m, ng = normal2(d[0],data,abnormal,NGtypeClass)
                else:
                    e, m, ng = normal3(d[0],data,abnormal,NGtypeClass)    
                if not e:
                    RE.abnormal += [ [d[0],d[2],d[4]]+ng ]    
        Ecard = d[0]
    if ra:
        return steps.inner
    for s in steps.inner:
        if s.name == restep:
            return s.inner, s.abnormal
    else:  
        #輸出無效生產率
        for s in steps.inner:
            a = sum([i[2] for i in s.inner])+0.0001
            b = sum([i[2] for i in s.abnormal])
            print(s.name+'生產量: ',round(a,1),'kg  異常量: ',round(b,1),'kg 佔生產量: ',round(b/a*100,1),'% ')
       
#傳入工卡、站點，根據異常單回傳是該站點 是否正常、異常量(KG)、異常分類
def normal1(ecard,step,data,abnormal,NGtypeClass=0):
    level = ['-1A','-1B','-1C','-1D','-2A','-2B','-2C','-3A','-3B','-4A']    
    #沒開異常單情況 : 正常 重修0
    if len(abnormal)==0:
        if NGtypeClass == 0:
            return True, 0, [0,0,0,0,0]
        elif NGtypeClass == 1:
            return True, 0, [0,0,0,0,0,0,0,0,0]
        else:
            print('NGtypeClass 只能選 0 or 1')
            return None         
    if ecard not in abnormal[:,0]:
        if NGtypeClass == 0:
            return True, 0, [0,0,0,0,0]
        elif NGtypeClass == 1:
            return True, 0, [0,0,0,0,0,0,0,0,0]
        else:
            print('NGtypeClass 只能選 0 or 1')
            return None
    #有開異常單時
    else:
        #找出工卡重:
        ind = list(abnormal[:,0]).index(ecard)
        mass = abnormal[ind,9]
        refix_mass = 0
        if NGtypeClass == 0:
            NG = classAbnormal1(abnormal[ind,14:17])
        elif NGtypeClass == 1:
            NG = classAbnormal2(abnormal[ind,17:20])
        else:
            print('NGtypeClass 只能選 0 or 1')
            return None
        #找往後所有重下胚量 
        #---*異常單開了重下胚但似乎也有可能取消重修、因此這段可能需要修改---
        if len(ecard) == 10:
            ecard_new = [ecard]+[ecard+ch for ch in level]
        elif ecard[-2] == '1':
            ecard_new = [ecard]+[ecard[:10]+ch for ch in level[4:]]
        elif ecard[-2] == '2':
            ecard_new = [ecard]+[ecard[:10]+ch for ch in level[7]]
        else:
            ecard_new = [ ecard]+[ecard[:10]+level[-1] ]
        for card in ecard_new:
            if card in list(abnormal[:,0]):
                ind = list(abnormal[:,0]).index(card)    
                if isdata(abnormal[ind,21]):
                    refix_mass += abnormal[ind,21]
        #------------------------可能修改段到此為止-------------------
        
        #找下一階級重修工卡量        
        if len(ecard) == 10:
            ecard_new = [ecard+ch for ch in level[:4]   ]
        elif ecard[-2]=='1':
            ecard_new = [ecard[:10]+ch for ch in level[4:7]  ]
        elif ecard[-2] == '2':
            ecard_new = [ecard[:10]+ch for ch in level[7:-1] ]
        elif ecard[-2] =='3':
            ecard_new = [ ecard[:10]+level[-1] ]
        
        #找重修量    
        for card in ecard_new:
            if card in data[:,0]:
                #找出該工卡號的第一個組碼
                ind = list(data[:,0]).index(card)
                #加工站點不超過15站,多拉一點沒關係
                ma = data[ind:ind+15]
                for ls in ma:
                    #工卡號符合 站點名稱相同
                    if ls[0]==card and ls[6]==step:
                        refix_mass += ma[0,9]
        if refix_mass >0:
            #重修+重下胚如果大於原始重量、則取原始重量為失敗重量
            return False, min(refix_mass,mass), NG
        else:
            return True, 0, NG
#考慮一次順利走完， 回傳 是否順利、不順利量(KG)、不順利的異常分類
def normal2(ecard,data,abnormal,NGtypeClass=0):
    #沒開異常單情況 : 正常 重修0
    if len(abnormal)==0:
        if NGtypeClass == 0:
            return True, 0, [0,0,0,0,0]
        elif NGtypeClass == 1:
            return True, 0, [0,0,0,0,0,0,0,0,0]
        else:
            print('NGtypeClass 只能選 0 or 1')
            return None 
    #工卡沒開出異常單 : 正常 重修0
    if ecard not in abnormal[:,0]:
        if NGtypeClass == 0:
            return True, 0, [0,0,0,0,0]
        elif NGtypeClass == 1:
            return True, 0, [0,0,0,0,0,0,0,0,0]
        else:
            print('NGtypeClass 只能選 0 or 1')
            return None
    #有開異常則統計
    else:
        #找出異常單組碼
        ind = list(abnormal[:,0]).index(ecard)
        #工卡重
        mass = abnormal[ind,4]
        #轉卡重
        a = 0 if abnormal[ind,10]=='' else float(abnormal[ind,10])
        #重下胚重
        b = 0 if abnormal[ind,21]=='' else float(abnormal[ind,21])
        #異常分類代號
        if NGtypeClass == 0:
            NG = classAbnormal1(abnormal[ind,14:17])
        elif NGtypeClass == 1:
            NG = classAbnormal2(abnormal[ind,17:20])
        else:
            print('NGtypeClass 只能選 0 or 1')
            return None
        if a+b>0:
            return False,  min(mass,a+b), NG
        else:
            return True, 0, NG
#回傳 是否開異常單、該工卡重、異常分類
def normal3(ecard,data,abnormal,NGtypeClass=0):
    #沒開異常單情況 : 正常 重修0
    if len(abnormal)==0:
        return True, 0, [0,0,0,0,0] 
    if ecard not in abnormal[:,0]:
        return True, 0, [0,0,0,0,0]
    else:
        #找出異常單組碼
        ind = list(abnormal[:,0]).index(ecard)
        if NGtypeClass == 0:
            NG = classAbnormal1(abnormal[ind,14:17])
        elif NGtypeClass == 1:
            NG = classAbnormal2(abnormal[ind,17:20])
        else:
            print('NGtypeClass 只能選 0 or 1')
            return None
        return False, abnormal[ind,4] , NG 
#檢驗結果分類異常
def classAbnormal1(ls):
    NG = [0,0,0,0,0]
    ch = ' '.join([i for i in ls if isdata(i)])
    if 'NG色差' in ch:
        NG[0] = 1
    elif 'NG物性' in ch:
        NG[1] = 1
    elif 'NG布面' in ch:
        NG[2] = 1
    elif '製程NG' in ch:
        NG[3] = 1
    elif '廠內NG' in ch:
        NG[4] = 1
    return NG
#異常代碼分類異常
def classAbnormal2(ls):
    # 暫時分成9類
    #'色差','物性','布面','廠內','鞋型不符',
    #'螢光汙染','色花/色不均','單絲直條/胚布直條','其他'
    NG = [0,0,0,0,0,0,0,0,0]
    for i in ls:
        if isdata(i):
            NG[ NGclass[ NGdict[i] ] ] = 1
    return NG
            
#根據檢驗結果分類異常類型 
#s有某站點的兩筆數據 s[0]: 某站點生產出的工卡 s[1]:某站點異常的工卡
def NGanaly(s,reclass='',ra=False):
    #NG類型序列: [色差,物性,布面,製程,廠內,其他]
    class NG:
        inner = []
        def __init__(self,name):
            self.name = name
            self.inner = []
            NG.inner += [self]
    prod = s[0]
    ng = s[1]
    NGdict = {}
    #有異常才統計
    if ng:
        if len(ng[0][3:])==5:
            for ch in NG_type1:
                NGdict[ch] = NG(ch)
            for d in ng:
                for i,s in enumerate(NG.inner[:5]):
                    if d[3+i]==1:
                        s.inner += [ d[0:3] ]
                if sum(d[2:])<1:
                    NGdict['其他'].inner += [ d[0:3] ]
        else:
            for ch in NG_type2:
                NGdict[ch] = NG(ch)
            for d in ng:
                for i, s in enumerate(NG.inner):
                    if d[3+i]==1:
                        s.inner+= [ d[0:3] ]
    
    if ra:
        return NG.inner
    totalmass = sum([d[2] for d in prod])
    for s in NG.inner:
        if s.name == reclass:
            return s.inner
    else:
        print('共生產: {}卡 {}kg'.format(len(prod),round(totalmass,1)))
        for s in NG.inner:
            if len(s.inner)>0:
                print('{}NG: {}卡 {}kg {}%'.format(s.name,len(s.inner),\
                                round(sum([i[2] for i in s.inner]),1),\
                                round(100*sum([i[2] for i in s.inner])/totalmass,1)))
                    

#給定日期起datestart 日期迄dateend 數據data
#回傳各加工站點當天早上8點到隔天早上8點的 完成工卡、開卡量、起始時間起第dds天完成
def prodGraph(datestart,dateend,data,specific=''):
    #建立各站點數據袋
    class steps:
        inner = []
        def __init__(self,name):
            self.name = name
            self.inner = [] #生產工卡
            steps.inner +=  [self]
    #中文站點名稱        
    chs = ['開卡']+step_ch
    #中文站點名對應到該站點類
    stepdict = {} 
    for n in chs:
        stepdict[n] = steps(n)
    
    #指定型體品名時資料
    if len(specific)>0:
        data = np.array([i for i in data if specific == i[5]])
    #降低數據計算量 
    a = datestart - timedelta(days=28)
    b = dateend + timedelta(days=1) 
    data = np.array([i for i in data if a<myStrptime(i[1])<b and i[3]!='作廢']) 
    days = (dateend-datestart).days
    
    def classify(mat):
        dds = (myStrptime(mat[0,1])-datestart).days
        if 0<=dds<days:
            stepdict['開卡'].inner += [ [mat[0,0],mat[0,2],mat[0,4],dds] ]
        for d in mat:
            if isdata(d[7]) and isdata(d[8]):
                et = myStrptime(d[7],d[8])
                dds = (et-datestart.replace(hour=8)).days
                if 0<=dds<days:
                    stepdict[d[6]].inner += [ [d[0],d[2],d[4],dds] ]
    
    #統計工卡
    i0 = 0
    card = data[0,0]
    for i,d in enumerate(data):
        if d[0] != card:
            classify(data[i0:i])
            card = d[0]
            i0 = i
    classify(data[i0:])    
    return steps.inner
    