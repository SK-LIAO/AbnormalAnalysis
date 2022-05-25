# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 11:18:10 2021

@author: A90127
"""
import numpy as np

#急件統計結果字典 
# 站點-> (平均值,標準差) 
Urgentdict = {
    '胚倉':(0.63,0.7),
    '前定':(0.45,0.56),
    '前品':(0.08,0.08),
    '染色':(1.55,1.99),
    '中檢':(0.0,0.0),
    '定型':(0.48,0.73),
    '品驗':(0.04,0.06),
    '對色':(-0.01,0.41),
    '驗布':(0.46,0.95),
    '烘乾':(0.46,0.64),
    '配布':(0.4,0.22),
    '精煉':(0.48,0.73),#注意,並無此資料,以定型為基礎
    '釘邊':(0.27,0.15),
    '剝色':(1.55,1.99),#注意,並無此資料,以染色為基礎
    '配布2':(0.4,0.22),#注意,並無此資料,以配布為基礎
    '中檢2':(0.43,1.38),#注意,並無此資料,以中檢為基礎
    '品驗2':(0.04,0.06),
    '驗布2':(0.34,0.68),
    '烘乾2':(0.46,0.64),#注意,並無此資料,以烘乾為基礎
    '包裝':(0.96,2.26),
    '品驗3':(0.04,0.06),#注意,並無此資料,以品驗2為基礎
    'BO':(0,1), #注意,以下氣染站點尚無統計數據
    'BO2':(0,1),
    'BW':(0,1),
    'BW2':(0,1), 
    'CP':(0,1),
    'CT':(0,1),
    'DC':(0,1),
    'DC2':(0,1),
    'DI':(0,1),
    'DI2':(0,1),
    'DP':(0,1),
    'DP2':(0,1),
    'HO':(0,1),
    'HP':(0,1),
    'OQC':(0,1),
    'PF':(0,1),
    'PS':(0,1),
    'RR':(0,1),
    'SQC':(0,1)
    }


'''
目前擁有的,卻仍然被歸類為其他類別的NG:
    研發不良
    待改染
    標準外
    拆卡下染
    成品烘乾
    入報廢倉
    取消重修
'''
NGclass = {
    '色差':0,
    '物性':1,
    '布面':2,
    '廠內':3,
    '鞋型不符':4,
    '螢光汙染':5,
    '色花/色不均':6,
    '單絲直條/胚布直條':7,
    '其他':8,
    }
NGdict = {
        '(排程)染程衝突延誤':'其他',
        '(排程)生壓衝突延誤':'其他',
        '(排程)降壓衝突延誤':'其他',	
        '(設備)I2流量異常':'其他',
        '(設備)dP壓差異常':'其他',
        '(設備)異常延誤出缸':'其他',
        'MEK不佳	':'物性',
        'MEN NG':'物性',
        'NG入庫':'其他',	
        'PH偏低':'物性',
        'PH偏高':'物性',
        'PVC NG':'物性',
        'QUV NG':'物性',
        'R3出缸鹼性':'其他',
        '上下孔不符':'其他',	
        '上柔軟':'其他',
        '上色不均':'色花/色不均',
        '上錯助劑':'廠內',
        '下缸修布面':'其他',
        '下錯染料':'廠內',
        '不織布溶解':'其他',
        '不織布鬆脫':'其他',
        '中檢方向錯誤':'廠內',
        '乾溼摩擦NG':'物性',
        '乾磨擦':'物性',
        '偏橘':'色差',
        '偏深':'色差',
        '偏淺':'色差',
        '偏白':'色差',
        '偏紅':'色差',
        '偏紫':'色差',
        '偏綠':'色差',
        '偏艷':'色差',
        '偏藍':'色差',
        '偏鈍':'色差',
        '偏黃':'色差',
        '偏黑':'色差',
        '克米平方':'物性',
        '克米平方偏輕':'物性',
        '克米平方偏重':'物性',
        '入不良倉':'其他',
        '入報廢倉':'其他',
        '入錯布':'廠內',
        '其他-其他因素':'其他',
        '其他-含螢光':'其他',
        '其他-外勞入錯布':'其他',
        '其他-外勞秤錯藥':'其他',
        '再送':'其他',
        '刮毛':'布面',
        '刷錯卡':'廠內',
        '前定排回':'其他',
        '前定異常':'其他',
        '加工變色':'其他',
        '助劑斑':'布面',
        '勾傷嚴重-布中半疋':'布面',
        '勾傷嚴重-布邊"整疋':'布面',
        '勾紗':'布面',
        '勾紗嚴重':'布面',
        '包錯布':'廠內',
        '化套':'其他',	
        '厚度偏厚':'物性',
        '厚度偏薄':'物性',
        '取消重修':'其他',
        '吃大邊':'其他',
        '吃深針':'布面',
        '品NG布面':'布面',
        '品NG物性':'物性',
        '品NG色差':'色差',
        '品OK':'其他',
        '品OK(D)	':'其他',
        '品OK布面':'其他',
        '品管驗布':'其他',
        '噴染失敗':'其他',
        '回復力NG':'其他',
        '壓痕':'其他',
        '外導布鬆脫':'其他',
        '孔型不符':'布面',
        '孔型歪斜':'布面',
        '孔形上下不對稱':'布面',
        '孔形不符':'布面',
        '孔形偏大':'布面',
        '孔形偏小':'布面',
        '孔形歪斜':'布面',
        '定型不佳':'其他',
        '定型修PH值':'其他',
        '定型溫度不符':'廠內',
        '定型走錯布':'廠內',
        '客NG布面':'布面',
        '客NG物性':'物性',
        '客NG色差':'色差',
        '客OK':'其他',
        '尺寸不符':'鞋型不符',
        '左右差力偏差±10%':'其他',
        '左右異色':'色花/色不均',
        '布太薄':'物性',
        '布捲吹向 Support<5cm':'其他',	
        '布捲完全吸到 Holder':'其他',
        '布捲完全吹到 Support':'其他',
        '布捲鬆脫下垂':'其他',
        '布濕':'布面',
        '布痕':'布面',
        '布皺':'布面',
        '布身不平':'布面',
        '布面刮毛':'布面',
        '布面勾紗':'布面',
        '布面待確認':'布面',
        '布面油污':'布面',
        '布面異常NG':'布面',
        '布面皺折':'布面',
        '布面風洞':'布面',
        '幅寬異常':'布面',
        '廠內NG':'廠內',
        '廠內OK':'其他',
        '延伸NG':'物性',
        '張力不均':'物性',
        '張力偏差±1kg':'物性',
        '彈性不佳':'物性',
        '待改染':'其他',
        '待確認':'其他',
        '成品凸紗':'布面',
        '成品烘乾':'其他',
        '手感不符':'布面',
        '手感偏硬':'布面',
        '手感偏軟':'布面',
        '折卡下染':'其他',
        '折痕':'布面',
        '折邊':'其他',
        '拆包':'其他',
        '拆包驗布':'其他',
        '拉力NG':'物性',
        '捲布確認OK':'其他',	
        '捲邊':'布面',
        '接頭':'其他',
        '換色卡':'其他',
        '損耗偏高':'廠內',
        '摺痕':'布面',
        '撕力NG':'物性',
        '擠壓痕':'色花/色不均',
        '擦傷':'布面',
        '擦痕':'布面',
        '整排斷紗':'其他',	
        '整排歪斜':'其他',
        '整排跳針':'其他',
        '斷紗':'布面',
        '斷紗1碼	':'布面',
        '斷紗一碼':'布面',
        '斷紗半碼':'布面',
        '暫不重修':'其他',
        '暫待不重修':'其他',
        '染出OK':'其他',
        '染出布邊皺褶':'其他',
        '染出布面OK':'其他',
        '染出未測色':'其他',
        '染房OK':'其他',
        '染房修色':'其他',
        '染料殘留_Blue':'其他',
        '染料殘留_Red':'其他',
        '染料殘留_Yellow	':'其他',
        '染料熔解_Blue':'其他',
        '染料熔解_Red':'其他',
        '染料熔解_Yellow	':'其他',
        '染錯布':'廠內',
        '業NG布面':'布面',
        '業OK':'其他',
        '業OK布面':'其他',
        '業OK物性':'其他',
        '業OK顏色':'其他',
        '業務NG色差':'色差',
        '標準內':'其他',
        '標準外':'其他',
        '樹脂斑':'布面',
        '橫板色花':'色花/色不均',
        '橫檔':'布面',
        '欠橘':'色差',
        '欠紅':'色差',
        '欠紫':'色差',
        '欠綠':'色差',
        '欠藍':'色差',
        '欠黃':'色差',
        '正常出缸':'其他',	
        '正背面不一':'其他',
        '氧化':'其他',
        '水洗不佳':'物性',
        '水痕':'布面',
        '水紋':'布面',
        '污染':'布面',
        '油污':'布面',
        '油污試修':'其他',	
        '油紗':'其他',
        '流色':'布面',
        '測試用':'廠內',
        '溫度不符':'其他',
        '漏針':'布面',
        '漸近色':'色花/色不均',
        '潑水不良':'物性',
        '濕磨擦':'物性',
        '烘乾驗布':'廠內',
        '烘乾驗布面':'廠內',
        '無標準':'其他',
        '牢度不佳':'物性',
        '物性待確認':'其他',	
        '疋差':'布面',
        '白度不一':'布面',
        '白斑':'布面',
        '白粉殘留過多':'布面',
        '皺折':'布面',
        '直條':'單絲直條/胚布直條',
        '直條(中度)':'單絲直條/胚布直條',
        '直條(嚴重)':'單絲直條/胚布直條',
        '直條色花':'色花/色不均',
        '研發不良':'其他',
        '研發不良排回':'其他',
        '破洞':'布面',
        '碼重偏輕':'布面',
        '碼重偏重':'布面',
        '秤錯染料':'廠內',
        '站別錯誤':'其他',
        '管差':'布面',
        '篇淺':'色差',
        '紋路歪斜':'布面',
        '組織不符':'布面',
        '結點':'布面',
        '纏車':'布面',
        '缸差在改染':'其他',	
        '缸差錯誤':'廠內',
        '置中誤差±2cm':'其他',	
        '耐侯NG':'物性',
        '耐汗NG':'物性',
        '耐磨NG':'物性',
        '耐黃變':'物性',
        '耐黃變NG':'物性',
        '胚因斷紗':'布面',
        '胚布凸紗':'布面',
        '胚布凹陷':'布面',
        '胚布勾紗':'布面',
        '胚布吐白紗':'布面',
        '胚布成圈不均-點點狀':'布面',
        '胚布斷紗':'布面',
        '胚布橫板':'布面',
        '胚布橫條':'布面',
        '胚布橫檔':'布面',
        '胚布油紗':'布面',
        '胚布直條':'布面',
        '胚布紋路歪斜':'布面',
        '胚布結點':'布面',
        '胚布走紗':'布面',
        '胚布跳紗':'布面',
        '胚布錯誤':'布面',
        '胚布髒污':'布面',
        '胚布黃化':'布面',
        '脆化':'物性',
        '色不均':'色花/色不均',
        '色移型':'物性',
        '色移行':'物性',
        '色花':'色花/色不均',
        '色跡':'布面',
        '色跡試修':'其他',	
        '藥點':'布面',
        '螞蟻斑':'布面',
        '螢光污染':'螢光汙染',
        '裁切不齊':'其他',
        '裂紗':'布面',
        '補捲吸向 Holder<5cm':'其他',	
        '製程-':'其他',
        '製程-下缸縮碼走色':'其他',
        '製程-值條':'其他',
        '製程-昇溫異常':'其他',
        '製程-染機故障':'其他',
        '製程-染程錯誤':'其他',
        '製程-水跳流動大':'其他',
        '製程-污染':'其他',
        '製程-熱交換器故障':'其他',	
        '製程-色花':'其他',
        '製程-色跡':'其他',
        '製程NG':'廠內',
        '製程錯誤':'廠內',
        '設立標準不符':'其他',	
        '走紗':'布面',
        '走錯布':'廠內',
        '起毛':'布面',
        '跳紗':'布面',
        '部分NG待包裝':'其他',
        '配方-併染色差':'其他',
        '配方-外勞秤錯藥':'其他',
        '配方-技研配方錯誤':'其他',
        '配方-色光偏差大':'其他',
        '配方錯誤':'廠內',
        '配錯布':'廠內',
        '酚黃變':'物性',
        '酚黃變NG':'物性',
        '重修':'其他',
        '重修碼重':'其他',
        '重走定型':'其他',
        '露針':'其他',
        '鞋形不符':'鞋型不符',
        '鞋形斷紗':'其他',
        '鞋形歪斜':'鞋型不符',
        '顏色待確認':'其他',
        '風洞':'布面',
        '風洞一碼':'布面',
        '髒污':'布面',
        '鬆紗':'其他',
        '黃化':'布面',
        'MEK NG':'物性',
        '偏豔':'色差',
        '拆卡下染':'其他',	
    }

#NG是否影響損耗清單
NG2Lossdict = {
        '(排程)染程衝突延誤':False,
        '(排程)生壓衝突延誤':False,
        '(排程)降壓衝突延誤':False,	
        '(設備)I2流量異常':False,
        '(設備)dP壓差異常':False,
        '(設備)異常延誤出缸':False,
        'MEK不佳	':False,
        'MEN NG':False,
        'NG入庫':False,	
        'PH偏低':False,
        'PH偏高':False,
        'PVC NG':False,
        'QUV NG':False,
        'R3出缸鹼性':False,
        '上下孔不符':False,	
        '上柔軟':False,
        '上色不均':False,
        '上錯助劑':False,
        '下缸修布面':False,
        '下錯染料':False,
        '不織布溶解':False,
        '不織布鬆脫':False,
        '中檢方向錯誤':False,
        '乾溼摩擦NG':False,
        '乾磨擦':False,
        '偏橘':False,
        '偏深':False,
        '偏淺':False,
        '偏白':False,
        '偏紅':False,
        '偏紫':False,
        '偏綠':False,
        '偏艷':False,
        '偏藍':False,
        '偏鈍':False,
        '偏黃':False,
        '偏黑':False,
        '克米平方':False,
        '克米平方偏輕':True,
        '克米平方偏重':True,
        '入不良倉':False,
        '入報廢倉':False,
        '入錯布':False,
        '其他-其他因素':False,
        '其他-含螢光':False,
        '其他-外勞入錯布':False,
        '其他-外勞秤錯藥':False,
        '再送':False,
        '刮毛':True,
        '刷錯卡':False,
        '前定排回':False,
        '前定異常':False,
        '加工變色':False,
        '助劑斑':True,
        '勾傷嚴重-布中半疋':True,
        '勾傷嚴重-布邊"整疋':True,
        '勾紗':True,
        '勾紗嚴重':True,
        '包錯布':False,
        '化套':False,	
        '厚度偏厚':False,
        '厚度偏薄':False,
        '取消重修':False,
        '吃大邊':False,
        '吃深針':True,
        '品NG布面':False,
        '品NG物性':False,
        '品NG色差':False,
        '品OK':False,
        '品OK(D)	':False,
        '品OK布面':False,
        '品管驗布':False,
        '噴染失敗':False,
        '回復力NG':False,
        '壓痕':False,
        '外導布鬆脫':False,
        '孔型不符':True,
        '孔型歪斜':True,
        '孔形上下不對稱':False,
        '孔形不符':True,
        '孔形偏大':False,
        '孔形偏小':False,
        '孔形歪斜':True,
        '定型不佳':False,
        '定型修PH值':False,
        '定型溫度不符':False,
        '定型走錯布':False,
        '客NG布面':False,
        '客NG物性':False,
        '客NG色差':False,
        '客OK':False,
        '尺寸不符':True,
        '左右差力偏差±10%':False,
        '左右異色':False,
        '布太薄':False,
        '布捲吹向 Support<5cm':False,	
        '布捲完全吸到 Holder':False,
        '布捲完全吹到 Support':False,
        '布捲鬆脫下垂':False,
        '布濕':False,
        '布痕':False,
        '布皺':False,
        '布身不平':False,
        '布面刮毛':True,
        '布面勾紗':True,
        '布面待確認':False,
        '布面油污':True,
        '布面異常NG':False,
        '布面皺折':False,
        '布面風洞':True,
        '幅寬異常':True,
        '廠內NG':False,
        '廠內OK':False,
        '延伸NG':False,
        '張力不均':False,
        '張力偏差±1kg':False,
        '彈性不佳':False,
        '待改染':False,
        '待確認':False,
        '成品凸紗':True,
        '成品烘乾':False,
        '手感不符':False,
        '手感偏硬':False,
        '手感偏軟':False,
        '折卡下染':False,
        '折痕':False,
        '折邊':False,
        '拆包':False,
        '拆包驗布':False,
        '拉力NG':False,
        '捲布確認OK':False,	
        '捲邊':True,
        '接頭':False,
        '換色卡':False,
        '損耗偏高':False,
        '摺痕':True,
        '撕力NG':False,
        '擠壓痕':False,
        '擦傷':True,
        '擦痕':True,
        '整排斷紗':True,	
        '整排歪斜':True,
        '整排跳針':True,
        '斷紗':True,
        '斷紗1碼	':True,
        '斷紗一碼':True,
        '斷紗半碼':True,
        '暫不重修':False,
        '暫待不重修':False,
        '染出OK':False,
        '染出布邊皺褶':False,
        '染出布面OK':False,
        '染出未測色':False,
        '染房OK':False,
        '染房修色':False,
        '染料殘留_Blue':False,
        '染料殘留_Red':False,
        '染料殘留_Yellow	':False,
        '染料熔解_Blue':False,
        '染料熔解_Red':False,
        '染料熔解_Yellow	':False,
        '染錯布':False,
        '業NG布面':False,
        '業OK':False,
        '業OK布面':False,
        '業OK物性':False,
        '業OK顏色':False,
        '業務NG色差':False,
        '標準內':False,
        '標準外':False,
        '樹脂斑':True,
        '橫板色花':True,
        '橫檔':True,
        '欠橘':False,
        '欠紅':False,
        '欠紫':False,
        '欠綠':False,
        '欠藍':False,
        '欠黃':False,
        '正常出缸':False,	
        '正背面不一':False,
        '氧化':False,
        '水洗不佳':False,
        '水痕':True,
        '水紋':True,
        '污染':True,
        '油污':True,
        '油污試修':False,	
        '油紗':True,
        '流色':True,
        '測試用':True,
        '溫度不符':False,
        '漏針':True,
        '漸近色':False,
        '潑水不良':False,
        '濕磨擦':False,
        '烘乾驗布':False,
        '烘乾驗布面':False,
        '無標準':False,
        '牢度不佳':False,
        '物性待確認':False,	
        '疋差':True,
        '白度不一':False,
        '白斑':True,
        '白粉殘留過多':False,
        '皺折':False,
        '直條':False,
        '直條(中度)':False,
        '直條(嚴重)':False,
        '直條色花':False,
        '研發不良':False,
        '研發不良排回':False,
        '破洞':True,
        '碼重偏輕':True,
        '碼重偏重':True,
        '秤錯染料':False,
        '站別錯誤':False,
        '管差':True,
        '篇淺':False,
        '紋路歪斜':True,
        '組織不符':True,
        '結點':True,
        '纏車':False,
        '缸差在改染':False,	
        '缸差錯誤':False,
        '置中誤差±2cm':False,	
        '耐侯NG':False,
        '耐汗NG':False,
        '耐磨NG':False,
        '耐黃變':False,
        '耐黃變NG':False,
        '胚因斷紗':True,
        '胚布凸紗':True,
        '胚布凹陷':True,
        '胚布勾紗':True,
        '胚布吐白紗':True,
        '胚布成圈不均-點點狀':False,
        '胚布斷紗':True,
        '胚布橫板':True,
        '胚布橫條':True,
        '胚布橫檔':True,
        '胚布油紗':True,
        '胚布直條':False,
        '胚布紋路歪斜':True,
        '胚布結點':True,
        '胚布走紗':True,
        '胚布跳紗':True,
        '胚布錯誤':False,
        '胚布髒污':True,
        '胚布黃化':False,
        '脆化':False,
        '色不均':False,
        '色移型':False,
        '色移行':False,
        '色花':False,
        '色跡':False,
        '色跡試修':False,	
        '藥點':True,
        '螞蟻斑':False,
        '螢光污染':False,
        '裁切不齊':False,
        '裂紗':True,
        '補捲吸向 Holder<5cm':False,	
        '製程-':False,
        '製程-下缸縮碼走色':False,
        '製程-值條':False,
        '製程-昇溫異常':False,
        '製程-染機故障':False,
        '製程-染程錯誤':False,
        '製程-水跳流動大':False,
        '製程-污染':False,
        '製程-熱交換器故障':False,	
        '製程-色花':False,
        '製程-色跡':False,
        '製程NG':False,
        '製程錯誤':False,
        '設立標準不符':False,	
        '走紗':True,
        '走錯布':False,
        '起毛':True,
        '跳紗':True,
        '部分NG待包裝':False,
        '配方-併染色差':False,
        '配方-外勞秤錯藥':False,
        '配方-技研配方錯誤':False,
        '配方-色光偏差大':False,
        '配方錯誤':False,
        '配錯布':False,
        '酚黃變':False,
        '酚黃變NG':False,
        '重修':False,
        '重修碼重':False,
        '重走定型':False,
        '露針':True,
        '鞋形不符':True,
        '鞋形斷紗':True,
        '鞋形歪斜':True,
        '顏色待確認':False,
        '風洞':True,
        '風洞一碼':True,
        '髒污':True,
        '鬆紗':False,
        '黃化':True,
        'MEK NG':False,
        '偏豔':False,
        '拆卡下染':True,	
        np.nan:False
    }