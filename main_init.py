# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 09:29:23 2021

@author: A90127
"""

#於下方輸入從erp抓下來csv資料數據的
#       路徑及檔名(不含副檔名),r=read,勿刪 
path = r'D:\A90127\AbnormalAnalysis\csv\1101月統計'
#輸入
path_urgent = r'D:\A90127\AbnormalAnalysis\csv\2022農曆年前必出明細'



'''
USER INTERFACE
0.dB:引入數據模組
    (1). dataBuild(path,title=False)
        #給定資料檔路徑,回傳 數據欄位的title 與 數據資料(不含title)
        #head = False: 指回傳數據資料、不回傳title
    (2).preyearUrgent(path_urgent)
        #給定資料檔路徑,回傳2筆資料數據資料
1.aA:異常分析模組
    (1). stepStatic(year,mon,day,data,ds=1,NGtype='效能',NGtypeClass=0,finish=True,specific='',restep='')------21/12/14追加NGtypeClass
        #給定日期 year mon day 基礎數據 data
        #統計當日am 8:00起 無效/NG生產量與無效/NG生產率
        #ds: ds天以內 預設1天
        #NGtype: NG類型, 效能NG(預設) or 品管NG
        #NGtypeClass(NG類型分類法): 
        #       0:依照檢驗結果, [色差,物性,布面,製程,廠內]
        #       1:依照異常原因, [色差,物性,布面,廠內NG,鞋型不符,螢光汙染,
        #                        色花/色不均,單絲直條/胚布直條,其他]
        #finish: 是否只考慮已完成工卡, 預設:是 (若關注在產能上建議改 否:False )
        #specific: 指定型體品名, 預設不指定品名
        #restep: 回傳該加工站點資訊(預設不回傳,直接列印數據)
    (2). totalStatic(year,mon,day,data,ds=1,NGtype='效能',NGtypeClass=0,finish=True,specific='',restep='')------21/12/16追加NGtypeClass
        #功能同(1),但是不統計通過該加工站點的工卡,改成統計生管當天所開的工卡
        #restep: 可輸入 '淨總'/'正規', 正規的計算會扣除轉(副)卡
    (3). NGanaly(s,reclass='')
        #給定NG數據 s 根據NG類型統計, NG數據請用(1)/(2)的回傳功能取得
        #reclass: 回傳該類別NG數據(預設不回傳,直接列印數據),根據分類法不同可用的名稱有
        #       檢驗結果: '色差','物性','布面','製程','廠內', '其他' 等六種 
        #       異常原因: '色差','物性','布面','廠內NG','鞋型不符',
        #                '螢光汙染','色花/色不均','單絲直條/胚布直條','其他' 等九種
2.wA:待加工分析模組
    (1). stepStatic(year,mon,day,hr,data,specific='',restep='')
        #給定日期時間 year mon day hr 基礎數據 data
        #統計當下時間各站點的待加工量數據
        #specific: 指定型體品名, 預設不指定品名
        #回傳該站點資訊(預設不回傳,直接列印數據)
3.sA:站點分析模組
    (1). prodNextStep(year,mon,day,Step,data,ds=0)
        #給定站點名稱 Step 基礎數據data
        #統計下一站名稱的比例
    (2). prodBackStep(year,mon,day,Step,data,ds=0)
        #給定站點名稱 Step 基礎數據data
        #統計前一站名稱的比例
    (3). maxProdDays(year,mon,day,data,ds=0,finish=True,specific='')
        #給定基礎數據data
        #統計工卡加工最久時間
    (4.) prodStay(year,month,day,x,data,ds=0,finish=True,specific='')
        #給定 天數 x 基礎數據 data
        #回傳: 統計加工時間大於x天的工卡數與工卡號
        #showcard: 是否回傳工卡號(預設否)
    (5.) avgProdDays(year,mon,day,data,ds=1,specific='')---21/12/16追加
        #給定時間 year month day 數據 data,
        #列印出統計ds(預設1)天內所開，且有至包裝完工工卡(不含轉卡)的
        #1.停留時間的平均值 2.停留時間的標準差
        #specific: 指定型體品名, 預設不指定品名
    (6.) stepStatic(year,mon,day,data,ds=1,finish=True,specific=''):---21/12/16追加
        #計算給定時間 year month day 數據 data,
        #統計ds(預設1)天內所開工卡的各站點
        #1.停留時間的平均值 2.停留時間的標準差
        #finish: 是否只統計已結案工卡(預設是)
        #specific: 指定型體品名, 預設不指定品名

'''


import abnormalAnaly as aA
import waitAnaly as wA
import stepAnaly as sA
import dataBuild as dB

 


