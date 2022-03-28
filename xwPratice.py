# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 08:43:22 2022

@author: A90127
"""

import xlwings as xw
path = r'D:\A90127\AbnormalAnalysis\csv\TestFile.xlsx'


app = xw.App(visible=False,add_book=False)
xb = app.books.open(path)
st = xb.sheets[0]
# 方法一
shape = st.used_range.shape
print(shape)

# 方法二
nrow = st.api.UsedRange.Rows.count
ncol = st.api.UsedRange.Columns.count
print(nrow)
print(ncol)

xb.save(path)
app.quit()




