# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 08:30:40 2021

@author: A90127
"""

import numpy as np

from datetime import datetime as dt
from pandas import read_csv, read_excel
from scipy import stats

#讀取工卡進度檔(.csv)、回工卡進度需要的欄位資料檔。
#該檔案請從erp抓取
def myfunc(path):
    data = np.array(read_csv(path,low_memory=False))
    heads = np.array(read_csv(path[:-4]+'-head.csv').columns)
    return data, heads
def dataBuild(path):
    data, heads = myfunc(path)
    subheads = ('工卡號','開卡日','染單單號','表頭狀態','開卡量','型體品名','站別', #7個
                '刷卡日期','刷卡時間','生產完成量','轉卡量','完成狀態','異常單號',  #6個
                '改善方案','檢驗結果1','檢驗結果2','檢驗結果3','異常代碼1','異常代碼2', #6個
                '異常代碼3','處理狀態','重下胚量','下染量','入庫重量', #4個
                )
    inds = [i for i,t in enumerate(heads) if t in subheads]
    return data[:,inds], subheads


#輸入excel檔
#回傳 excel的表頭檔 與 數據資料
def urgentBuild(path):
    data = read_excel(path)
    return np.array(data), np.array(data.columns) 


#將文字數字、轉datetime.datetime格式
def myStrptime(date,time=0):
    time = '{0:04d}'.format(int(time))
    return dt.strptime(date+' '+time[:2]+':'+time[2:],'%Y/%m/%d %H:%M')
def myStrftime(ymd):
    return dt.strftime(ymd, '%Y/%m/%d')

def isdata(a):
    if type(a)==float:
        return not np.isnan(a)
    else:
        return True
#給定常態分布normal = (期望值,標準差)
#現在時間,死線,回傳風險值(%)    
def risk(normal,searchtime,deadline):
    lt = deadline-searchtime
    lt = lt.days + lt.seconds/86400
    if lt<=0:
        return 100
    else:
        return round((1-stats.norm(normal[0],normal[1]).cdf(lt))*100,1)
    
    
    
    
    
