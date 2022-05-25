# -*- coding: utf-8 -*-
"""
Created on Fri May 13 13:15:08 2022

@author: A90127
"""

import numpy as np
from dataBuild import isdata
from mydict import NG2Lossdict
import matplotlib.pyplot as plt

def normalLoss(data,shoetype=True,factor=0):
    #只拉斗工廠工卡數據
    if factor==0: 
        data = np.array([d for d in data if d[0][0]=='E'])
    #只拉雲科廠工卡數據
    else:
        data = np.array([d for d in data if d[0][0]=='P'])
    #建立開有異常單資料
    abnormal = np.array([d for d in data if isdata(d[12])])
    
    #不統計轉卡 與 未結案工卡 只需過濾出包裝欄位即可
    data = np.array([d for d in data if d[6] in ['包裝','PF'] and len(d[0])==10
                    and d[3] not in ['新增','核准','作廢']])
    #只考慮進良品倉量
    data = np.array([d for d in data if isdata(d[23])])
    
    def NGeffect(c):
        if c not in abnormal[:,0]:
            return False
        else:
            ind = list(abnormal[:,0]).index(c)
            if abnormal[ind,20]=='轉開副卡':
                return True
            else:
                NG = abnormal[ind,17:20]
                return any([NG2Lossdict[i] for i in NG])
    data = np.array([d for d in data if not NGeffect(d[0])])
    if shoetype:
        #鞋形布
        data = np.array([d for d in data if isdata(d[5])])
    else:
        #非鞋形布
        data = np.array([d for d in data if not isdata(d[5])])
    return data

#迴歸公式 y = a1*x + a0
#給定陣列 x 及 y
#回傳其回歸係數 a1, a0
def lin_regre(x,y):
    n = len(x)
    s_x = sum(x)
    s_y = sum(y)
    s_xy = sum(x*y)
    s_x2 = sum(x*x)
    a1 = (n*s_xy-s_x*s_y)/(n*s_x2-s_x**2)
    a0 = s_y/n-a1*s_x/n
    return a1, a0

#迴歸公式 y = a*exp(b*x)
#給定陣列 x 及 y
#回傳其回歸係數 a, b 
def exp_regre(x,y):
    n = len(x)
    lny= np.log(y)
    s_x = sum(x)
    s_lny = sum(lny)
    s_xlny = sum(x*lny)
    s_x2 = sum(x*x)
    b = (n*s_xlny-s_x*s_lny)/(n*s_x2-s_x**2)
    lna = s_lny/n - b*s_x/n
    return np.exp(lna), b
#迴歸公式 y = a*log(x) + b
#給定陣列 x 及 y
#回傳其回歸係數 a, b
def log_regre(x,y):
    x = np.log(x)
    return lin_regre(x,y)

#迴歸公式 y = a/x + b
#給定陣列 x 及 y
#回傳其回歸係數 a, b
def reciprocal_regre(x,y):
    x = 1/np.sqrt(x)
    return lin_regre(x,y)


def piecewiseLoss(x,y,int_num,std_num):
    I = np.linspace(min(x), max(x),num=int_num, endpoint=True)
    piecewiseline = np.zeros((len(I)-1,2))
    for i, (s,e) in enumerate(zip(I[:-1],I[1:])):
        piecewiseline[i,0] = s
        y_im = np.array([k for j,k in zip(x,y) if e>j>=s])
        mean = y_im.mean()
        std = y_im.std()
        piecewiseline[i,1] = mean + std_num*std
    return piecewiseline 


#散點圖 + 線性回歸線
def graph1(x,y):
    #colors = np.random.rand(len(x))
    plt.scatter(x, y, alpha=0.3)
    m, b = np.polyfit(list(x),list(y),1)
    plt.plot(x, m*x+b,color='r')
    plt.show()

#散點圖  + 損耗估計圖     
def graph2(x,y,int_num,std_num):
    I = np.linspace(min(x), max(x),num=int_num, endpoint=True)
    line = np.zeros((len(I)-1,2))
    for i, (s,e) in enumerate(zip(I[:-1],I[1:])):
        line[i,0] = s
        y_im = np.array([k for j,k in zip(x,y) if e>j>=s])
        mean = y_im.mean()
        std = y_im.std()
        line[i,1] = mean + std_num*std
    plt.scatter(x, y, alpha=0.3)
    plt.plot(line[:,0],line[:,1],color='r')
    plt.show()
    return line

#散點圖 + 對數回歸圖
def graph3(x,y,a,b):
    I = np.linspace(min(x), max(x),50, endpoint=True)
    plt.scatter(x, y, alpha=0.3)
    plt.plot(I,np.array([a*np.log(i)+b for i in I]),color='r')
    plt.show
    