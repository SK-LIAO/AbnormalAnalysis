# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 15:43:56 2022

@author: A90127
"""

import numpy as np
import xlwings as xw
from stepAnaly import isdata
from dataBuild import urgentBuild
from pandas import read_excel

def renewUrgent(data,head,path):
    urgent, KAhead = urgentBuild(path)
    app = xw.App(visible=True,add_book=False)
    xb = app.books.open(path)
    st1 = xb.sheets[0]
    try:
        st2 = xb.sheets[1]
    except:
        st2 = xb.sheets.add(name='工卡急件進度表',after=xb.sheets[0])
        
    KAyhead = ['下染量','未開卡量','未完成量','進度']
    #填充上head可能欠缺的欄位
    KAhead = list(KAhead)+[h for h in KAyhead if h not in KAhead]
    st1.cells[0,0].value = np.array(KAhead)
    KAheaddict = {}
    for i,h in enumerate(KAhead):
        KAheaddict[h] = i
    
    drophead = ['下染量','需完成下染量','未開卡量','未完成量',]
    addhead = ['工卡','數量KG','包裝良品量']
    conservehead = [h for h in KAhead if h not in drophead]
    
    Ehead = conservehead[:KAheaddict['染單']+1] + addhead + conservehead[KAheaddict['染單']+1:]
    #工作表2填入欄位名稱
    st2.cells[0,0].value = np.array(Ehead)
    Eheaddict = {}
    for i,h in enumerate(Ehead):
        Eheaddict[h] = i

    #拉出急件的工卡進度
    headdict = {}
    for i,h in enumerate(head):
        headdict[h] = i 
    data = np.array([d for d in data if d[headdict['染單單號']] in urgent[:,KAheaddict['染單']]])
    
    #拉出工卡進度所需要的欄位
    subhead = ['工卡號','染單單號','表頭狀態','開卡量','站別','刷卡日期','轉卡量','下染量','入庫重量']
    inds = [headdict[h] for h in subhead]
    data = data[:,inds]
    
    KAlen = len(KAhead)
    Elen = len(Ehead)
    
    def st2record(mat,row):
        E = mat[0,0]
        KA = mat[0,1]
        j = list(urgent[:,KAheaddict['染單']]).index(KA)
        conservevalue = [urgent[j,KAheaddict[h]] for h in conservehead]
        value = conservevalue[:KAheaddict['染單']+1] + [E,mat[0,3],mat[0,8]-max(mat[:,6])] +conservevalue[KAheaddict['染單']+1:]
        steps = mat[:,4]
        sign = [i for i in mat[:,5] if isdata(i)]
        if mat[0,2] in ['強迫結案','結案','作廢']:
            value[Eheaddict['進度']] = mat[0,2]
            st2.cells[row,0].value = value
            st2.cells[row,:Elen].color = (100,255,100)
        elif len(steps)==len(sign):
            value[Eheaddict['進度']] = '已包裝'
            st2.cells[row,0].value = value
            st2.cells[row,:Elen].color = (255,255,100)
        else:
            value[Eheaddict['進度']] = '待'+steps[len(sign)]
            st2.cells[row,0].value = value
            st2.cells[row,:Elen].color = (255,100,100)   
    E = data[0,0]
    ind = 0
    row = 1
    for i,d in enumerate(data):
        if d[0] != E:
            mat = data[ind:i,:]
            st2record(mat,row)
            ind = i
            row+=1
            E = d[0]
    st2record(data[ind:i,:],row)
    xb.save(path)        
    Edata = np.array(read_excel(path,1))
    #print('更新染單狀態')
    #renew染單進度
    for i, d in enumerate(urgent):
        row = i+1
        KA = d[KAheaddict['染單']]

        #蒐集同KA的所有工卡
        Ocs = [s for s in Edata if s[Eheaddict['染單']]==KA]
        #補上下染量
        a = data[list(data[:,1]).index(KA),7] 
        st1.cells[row,KAheaddict['下染量']].value = a
        #計算良品入倉總量
        m1 = sum([s[Eheaddict['包裝良品量']] for s in Ocs if isdata(s[Eheaddict['包裝良品量']])])
        #計算已開卡未結案量(正在染整廠加工的量)
        m2 = sum([s[Eheaddict['數量KG']] for s in Ocs if not isdata(s[Eheaddict['包裝良品量']]) and 
                  s[Eheaddict['進度']] not in ['強迫結案','結案','作廢']])
        #補上未完成量
        st1.cells[row,KAheaddict['未完成量']].value = round(a-m1,1)
        #補上未開卡量
        st1.cells[row,KAheaddict['未開卡量']].value = round(a - m1 - m2,1)
        #補上進度
        if round(a-m1,1) < 2.2+a/1.1*0.1:
            st1.cells[row,KAheaddict['進度']].value = '已完成'
            st1.cells[row,:KAlen].color = (100,255,100)
        elif round(a - m1 - m2,1) < 2.2+a/1.1*0.1:
            st1.cells[row,KAheaddict['進度']].value = '待完成'
            st1.cells[row,:KAlen].color = (255,255,100)
        else:
            st1.cells[row,KAheaddict['進度']].value = '待全入胚'
            st1.cells[row,:KAlen].color = (255,100,100)
        #print('更新染單 {} 列'.format(i))

    return 

