# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 11:33:51 2018

@author: wfsha
"""

import skimage
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage import io
import re
from xpinyin import Pinyin
import os
#opencv tensorflow
%matplotlib

cat = io.imread('e:/desktop/cat.jpg')

df = pd.DataFrame(['Cat'], columns=['Image'])

fig = plt.figure(figsize = (8,4))
ax1 = fig.add_subplot(1,2, 1)
ax1.imshow(cat)

import os

fd = 'e:/desktop/mmix/modeldata/'
lis = os.listdir(fd)
writer = pd.ExcelWriter('E:/desktop/mmix/modeldata.xlsx')
for i in lis:
    f = pd.read_excel(fd+i)
    f.to_excel(writer,sheet_name=i)
writer.save()


######

City = ['Market (City)','城市','活动客户所在城市','Market ','Market','收货区域','audit_cd','City','市场']
Month = ['月份','投放时间','Date','date','实际执行时间','下单日期时间','Month','监测日期','日期']
fd = 'e:/desktop/mmix/modeldata/'
lis = os.listdir(fd)

def to_City(s):
    s = str(s)
    if '市' in s:s = s[:-1]
    if '(' in s:s = s.split('(')[0]
    if '（' in s:s = s.split('（')[0]
    return Pinyin().get_pinyin(s,'').title()

def to_Month(s):
    s = str(s)
    xx=0
    if '/' in s:
        x = s.split('/')
        xx=x[0] + '/'+ str(int(x[1])) + '/1'
    if '-' in s:
        x = s.split('-')
        xx=x[0] + '/'+ str(int(x[1])) + '/1'
    return xx


    

#------------------------------------------------------
    
fd = 'e:/desktop/test/'
lis = os.listdir(fd)
fbd = []
flx = ['brand_sales.xlsx']
for i in lis:
    if 'flx' in i:
        flx.append(i)
    else:
        fbd.append(i)

#fbd
tb = pd.read_excel('e:/desktop/mmix/citymonth.xlsx')
tb.columns = ['City','Month']
tb.City = tb['City'].apply(lambda x:to_City(x))


for i in fbd:
    print(i)
    f = pd.read_excel(fd+i)
    col = f.columns
    if 'City' in col:
        f = f.groupby(['Month','City'])[col.difference(['Month','City'])].sum().reset_index()
        tb = pd.merge(tb,f,how = 'left',on=['Month','City'])
    else:
        f = f.groupby(['Month'])[col.difference(['Month'])].sum().reset_index()
        tb = pd.merge(tb,f,how = 'left',on=['Month'])
    print(len(tb))

tb.to_excel('e:/desktop/mmix_fbd.xlsx')

#flx
tb = pd.read_excel('e:/desktop/mmix/citymonth.xlsx')
tb.columns = ['City','Month']
tb.City = tb['City'].apply(lambda x:to_City(x))

for i in flx:
    print(i)
    f = pd.read_excel(fd+i)
    col = f.columns
    if 'City' in col:
        f = f.groupby(['Month','City'])[col.difference(['Month','City'])].sum().reset_index()
        tb = pd.merge(tb,f,how = 'left',on=['Month','City'])
    else:
        f = f.groupby(['Month'])[col.difference(['Month'])].sum().reset_index()
        tb = pd.merge(tb,f,how = 'left',on=['Month'])
    print(len(tb)) 

tb.to_excel('e:/desktop/mmix_flx.xlsx')

j = 0
d = {}
for i in flx:
    f = pd.read_excel(fd+i)
    col = f.columns
    col2 = col.difference(['Month','City'])
    for k in col2:
        d[i[:-5]+'-'+k] = i

dic = pd.DataFrame()
dic['var'] = list(d.keys())
dic['file'] = list(d.values())
dic.to_excel('e:/desktop/flx_cata.xlsx')

d = {}
for i in fbd:
    f = pd.read_excel(fd+i)
    col = f.columns
    col2 = col.difference(['Month','City'])
    for k in col2:
        d[i[:-5]+'-'+k] = i

dic = pd.DataFrame()
dic['var'] = list(d.keys())
dic['file'] = list(d.values())
dic.to_excel('e:/desktop/fbd_cata.xlsx')


--vtt
m = pd.read_excel('e:/desktop/mmix_flx.xlsx',sheet_name='附录')
m['vtt'] = m['var'].apply(lambda x:Pinyin().get_pinyin(x.split('-')[1]+'.'+x.split('-')[0].split('_')[1],''))
m.to_excel('e:/desktop/test1.xlsx')




####################
fd = 'e:/desktop/test/'
lis = os.listdir(fd)

-----
f = pd.read_excel('e:/desktop/mmix_flx.xlsx')
tb = pd.read_excel('e:/desktop/test/flx_social.xlsx')

ff = pd.merge(f,tb,how = 'left',on=['Month'])
ff.fillna(0,inplace=True)
ff.to_excel('e:/desktop/mmix_flx2.xlsx')
------


f = pd.read_excel('e:/desktop/mmix_flx.xlsx',sheet_name='附录')
f['ch']=f['vtt'].map(lambda x: x.split('.')[0].split('_')[-1])
f.to_excel('e:/desktop/test1.xlsx')



tb = pd.read_excel('e:/desktop/mmix/modeldata/fbd_tvspd.xlsx')
tb.Month = tb.Month.apply(lambda x:str(x)[:4]+'/'+str(int(str(x)[-2:]))+'/1')


f = pd.merge(f,tb,how='left',on=['Month'])
f.fillna(0,inplace=True)
f.to_excel('e:/desktop/test1.xlsx')
