# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 17:18:27 2018

@author: wfsha
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 10:33:19 2018

@author: wfsha
"""

import pandas as pd
import numpy as np
import subprocess
import datetime
import os

writer = pd.ExcelWriter('E:/desktop/mmix/fbd_modeldata.xlsx')
#sales
f = pd.read_excel('e:/desktop/mmix/PTR Data for FBD&FLX MMM_18M06.xlsx')
f = f[f['Brand']=='FLIXONASE AQUA']
f['Date'] = f['Date'].map(lambda x:str(x).split('-')[0]+'/'+str(int(str(x).split('-')[1]))+'/1')

tb = f[['audit_cd','Date']].drop_duplicates()

Sub_Category = f['Sub Category'].drop_duplicates()
SKU_Name = f['SKU Name'].drop_duplicates()
TSKF_Defined_Category = f['TSKF Defined Category'].drop_duplicates()
OTC_RX = f['OTC/RX'].drop_duplicates()
#Manu_Type = f['Manu Type'].drop_duplicates()
Package = f['Package'].drop_duplicates()

for i in Sub_Category:
    for j in SKU_Name:
        for k in TSKF_Defined_Category:
            for n in OTC_RX:
                for m in Package:
                    tp = f[(f['Sub Category']==i)&(f['SKU Name']==j)&(f['TSKF Defined Category']==k)&(f['OTC/RX']==n)&(f['Package']==m)][['audit_cd','Date','VAL','PACK','ND','WD']]
                    sn = str(i+'_'+j+'_'+k+'_'+n+'_'+m+'_')
                    tp.columns = ['audit_cd','Date',sn+'VAL',sn+'PACK',sn+'ND',sn+'WD']
                    if len(tp)>2:
                       tb = pd.merge(tb,tp,how='left',on=['audit_cd','Date'])
tb=tb.fillna(0)
tb.to_excel('e:/desktop/mmix/modeldata/flx_sales.xlsx')     



---#otv
--o = pd.read_excel('e:/desktop/mmix/rawdata/FLX_TVOTV_161718/TV+OTV/MMM- FLX 2016-2018.Jun OTV-27city.xlsx')
o = o.groupby(['Year', 'Month', 'Market ', 'Media Platform', 'PC/Mobile/OTT',' Impression（total）', ' Impression（TA）', 'Universe-city', 'iGRP','Population-city', 'GRP', 'Population-全国','Population-27mkt', 'Click-Total', 'Click-TA'])['Spending'].sum().reset_index()
o['Year'] = o['Year'].map(lambda x:str(int(x)))
o['Month'] = o['Month'].map(lambda x:str(int(x)))
o['Date'] = o['Year'].str.cat(o['Month'],sep='/')

otb = o[['Date','Market ','Population-city','Population-全国','Population-27mkt']].drop_duplicates()
['Date','Market ','Population-city','Population-全国','Population-27mkt']


platform = o['Media Platform'].drop_duplicates()
device = o['PC/Mobile/OTT'].drop_duplicates()

col = [i for i in o.columns[5:-1] if i not in ['Date','Market ','Population-city','Population-全国','Population-27mkt']]

for i in platform:
    for j in device:
        tp = o[(o['Media Platform']==i)&(o['PC/Mobile/OTT']==j)][['Date','Market ']+col]
        sn = str(i+'_'+j)
        co = [sn+'_'+n for n in col]
        tp.columns = ['Date','Market ']+co
        tp.drop_duplicates()
        if len(tp)>2:
            otb = pd.merge(otb,tp,how='outer',on=['Date','Market '])
otb = otb.fillna(0)
otb.to_excel('e:/desktop/mmix/modeldata/flx_otv.xlsx')


#target OTV
o = pd.read_excel('e:/desktop/mmix/rawdata/FLX_targetOTV_17.XLSX')
o['Year'] = o['Year'].map(lambda x:str(int(x)))
o['Month'] = o['Month'].map(lambda x:str(int(x))+'/1')
o['Date'] = o['Year'].str.cat(o['Month'],sep='/')
o = o.groupby(['Date', 'Market ', 'Media Platform', 'PC/Mobile'])['Click', 'iGRP',u'Weighted_全国_iGRP','Weighted_27mkt_iGRP',' Impression'].sum().reset_index()

platform = o['Media Platform'].drop_duplicates()
device = o['PC/Mobile'].drop_duplicates()

otb = o[['Date','Market ']].drop_duplicates()
col = ['Click', 'iGRP',u'Weighted_全国_iGRP','Weighted_27mkt_iGRP',' Impression']
for i in platform:
    for j in device:
        tp = o[(o['Media Platform']==i)&(o['PC/Mobile']==j)][['Date','Market ','Click', 'iGRP',u'Weighted_全国_iGRP','Weighted_27mkt_iGRP',' Impression']]
        sn = str(i+'_'+j+'_')
        co = [sn+n for n in col]
        tp.columns = ['Date','Market ']+co
        tp.drop_duplicates()
        if len(tp)>2:
            otb = pd.merge(otb,tp,how='outer',on=['Date','Market '])
otb = otb.fillna(0)
otb.to_excel('e:/desktop/mmix/modeldata/flx_targetotv.xlsx')

#new otv additional mix reach--------
o = pd.read_excel('e:/desktop/mmix/rawdata/FLX_TVOTV_161718/TV+OTV/MMM- FLX 2016-2018.Jun OTV-final(additional mix reach）.xlsx')
o = o.groupby(['Year', 'Month', 'Market ', 'Media Platform', 'PC/Mobile/OTT',' Impression（total）', ' Impression（TA）', 'Universe-city', 'iGRP','Population-city', 'GRP', 'Population-全国','Population-27mkt', 'Click-Total', 'Click-TA'])['Spending'].sum().reset_index()
o['Year'] = o['Year'].map(lambda x:str(int(x)))
o['Month'] = o['Month'].map(lambda x:str(int(x)))
o['Date'] = o['Year'].str.cat(o['Month'],sep='/')

otb = o[['Date','Market ','Population-city','Population-全国','Population-27mkt']].drop_duplicates()
#['Date','Market ','Population-city','Population-全国','Population-27mkt']


platform = o['Media Platform'].drop_duplicates()
device = o['PC/Mobile/OTT'].drop_duplicates()

col = [i for i in o.columns[5:-1] if i not in ['Date','Market ','Population-city','Population-全国','Population-27mkt','Universe-city']]

for i in platform:
    for j in device:
        tp = o[(o['Media Platform']==i)&(o['PC/Mobile/OTT']==j)][['Date','Market ']+col]
        sn = str(i+'_'+j)
        co = [sn+'_'+n for n in col]
        tp.columns = ['Date','Market ']+co
        tp = tp.groupby(['Date','Market '])[tp.columns[2:]].sum().reset_index()
        if len(tp)>0:
            otb = pd.merge(otb,tp,how='outer',on=['Date','Market '])
        print(i,j,len(otb))
otb = otb.fillna(0)
#otb=otb.groupby(['Date', 'Market '])[otb.columns[5:]].sum().reset_index()
otb.to_excel('e:/desktop/mmix/modeldata/flx_otv.xlsx')

#tv
lis = os.listdir('e:/desktop/mmix/rawdata/FLX_TVOTV_161718/TV+OTV/TV data')
contb = pd.DataFrame(columns=['广告名称','Date','城市','卫视_15S_毛评点', '卫视_5S_毛评点', '地方台_15S_毛评点','地方台_5S_毛评点','央视_15S_毛评点','央视_5S_毛评点'])
for li in lis:
    t = pd.read_excel('e:/desktop/mmix/rawdata/FLX_TVOTV_161718/TV+OTV/TV data/%s'%li,sheet_name='data')
    #t.columns = t.loc[1]
    t = t[2:]
    #t2 = pd.read_excel('e:/desktop/mmix/rawdata/FBD_TVOTV_161718/MMM- FBD 2016 TV Spending.xls')
   
    t = t.fillna(0)
    t['channelgroup'] = '地方台'
    t.loc[t['频道'].str.contains('卫视'),'channelgroup']='卫视'
    t.loc[t['频道'].str.contains('中央'),'channelgroup']='央视'
    
    t['duration'] = '5S'
    t.loc[t['时长']=='0000:15','duration']  = '15S'
    
    
    tb = pd.DataFrame(columns=['广告名称','日期','城市','毛评点','duration','channelgroup'])
    for i in t.columns[7:-3]:
        print(i)
        tt = t[['广告名称','日期','duration','channelgroup']]
        tt['城市'] = i
        tt['毛评点'] = t[[i]]
        
        tb = pd.concat([tb,tt],axis=0,ignore_index = True)
    
    tb['Date'] = tb['日期'].map(lambda x:str(x)).str.split('-').map(lambda x:'/'.join([str(x[0]),str(x[1]),str('1')]))
    tb['城市'] = tb['城市'].str.split("(").map(lambda x:x[0])
    
    tb[tb['毛评点']!='.'].dtypes
    tb=tb[tb['毛评点']!='.'].groupby(['广告名称','Date','城市','duration','channelgroup'])['毛评点'].sum().reset_index()
    
    cgroup = tb['channelgroup'].drop_duplicates()
    dgroup = tb['duration'].drop_duplicates()
    xb = tb[['广告名称','Date','城市']].drop_duplicates()
    for i in cgroup:
        for j in dgroup:
            ttb = tb[(tb['channelgroup']==i)&(tb['duration']==j)][['广告名称','Date','城市','毛评点']]
            ttb.columns = ['广告名称','Date','城市',i+'_'+j+'_'+'毛评点']
            xb = pd.merge(xb,ttb,how='outer',on=['广告名称','Date','城市'])
    contb = pd.concat([contb,xb],ignore_index=True)

contb=contb[['Date','城市','卫视_15S_毛评点', '卫视_5S_毛评点', '地方台_15S_毛评点','地方台_5S_毛评点','央视_15S_毛评点','央视_5S_毛评点']].fillna(0)
contb.to_excel('e:/desktop/mmix/modeldata/flx_tv.xlsx')


#sem

s = pd.read_excel('e:/desktop/mmix/rawdata/FLX_SEM_161718.xlsx',sheet_name='FLX Search')
s['Year'] = s['Year'].map(lambda x:str(int(x)))
s['Month'] = s['Month'].map(lambda x:str(int(x)))
s['Date'] = s['Year'].str.cat(s['Month'],sep='/')
s['Date'] = s['Date'].map(lambda x:'/'.join([x,'1']))
s.columns = ['Product', 'Market', 'Year', 'Month', 'Campaign', 'Website','Platform (PC/Mobile)', 'Normal/Targeting', 'Clicks', 'Impressions','Actual Spending (RMB)', 'Date']

product = s['Product'].drop_duplicates()
campaign = s['Campaign'].drop_duplicates()
platform = s['Platform (PC/Mobile)'].drop_duplicates()

col =  ['Clicks','Impressions','Actual Spending (RMB)']
tb = s[['Date','Market']].drop_duplicates()
for i in product:
    for j in campaign:
        for k in platform:
            tp = s[(s['Product']==i)&(s['Campaign']==j)&(s['Platform (PC/Mobile)']==k)][['Date','Market']+col]
            sn = str(i+'_'+j+'_'+k+'_')
            tp.columns = ['Date','Market',sn+'Clicks',sn+'Impressions',sn+'Spending']
            tp=tp.groupby(['Date','Market'])[sn+'Clicks',sn+'Impressions',sn+'Spending'].sum().reset_index()
            if len(tp)>0:
                tb = pd.merge(tb,tp,how='left',on=['Date','Market'])
                tb = tb.fillna(0)
#tb = tb.groupby(['Market','Date'])['Clicks','Impressions','Actual Spending (RMB)'].sum().reset_index()
tb.to_excel('e:/desktop/mmix/modeldata/flx_sem.xlsx')




#posm&remaind-----------------

#p16 = pd.read_excel('e:/desktop/mmix/rawdata/FBD_rmd_16的副本.xlsx')
#p16 = p16[1:]
#p16.columns = ['收货区域', '数量', 'total cost', '2016/7/1', '2016/8/1', '2016/9/1', '2016/10/1', '2016/11/1', '2016/12/1']
#tb16 = pd.DataFrame(columns=['City','Date','Cost'])
#for i in p16.columns[3:]:
#    tp = p16[['收货区域',i]]
#    tp['Date'] = i
#    tp = tp[['收货区域','Date',i]]
#    tp.columns = ['City','Date','Cost']
#    tb16 = pd.concat([tb16,tp],axis=0)
#tb16['分类'] = '品牌提示物'
#tb16['合计预计单品数量'] = 0
#tb16['物料名称']='芬必得保温杯品牌提示物cost'
#tb16.columns = ['收货区域','下单日期时间','成本（含税）','分类','合计预计单品数量','物料名称']

p = pd.read_excel('e:/desktop/mmix/rawdata/flx_posm&rmd_1718.xlsx',sheet_name='总表')
p = p[['货主简称','物流订单号','下单日期时间','收货区域','物料代码','物料名称','合计预计单品数量','规格','分类','品牌']]
#pcost = pd.read_excel('e:/desktop/mmix/rawdata/POSM and brand reminder cost - Fenbid.xlsx')
#pcost.columns = ['分类2', '物料代码', '物料名称', '成本（含税）']
#pcost = pcost[['物料代码','成本（含税）']].drop_duplicates()
#pp = pd.merge(p,pcost,how = 'left',on =['物料代码'])
pp = p[['收货区域','下单日期时间','分类','合计预计单品数量','物料名称']]
pp['下单日期时间'] = pp['下单日期时间'].map(lambda x:str(x)).str.split('-').map(lambda x:'/'.join([str(x[0]),str(x[1]),str(1)]))

#pp = pd.concat([pp,tb16],axis=0)

pp1=pp[pp['分类']=='POSM']
matname = pp1['物料名称'].drop_duplicates()
cate = pp1['分类'].drop_duplicates()
tb = pp1[['下单日期时间','收货区域']].drop_duplicates()
for i in matname:
    for j in cate:
        tp = pp1[(pp1['物料名称']==i)&(pp1['分类']==j)][['下单日期时间','收货区域','合计预计单品数量']]
        tp.columns = ['下单日期时间','收货区域',i+'_'+j+'_'+'合计预计单品数量']
        tp=tp.groupby(['下单日期时间','收货区域'])[i+'_'+j+'_'+'合计预计单品数量'].sum().reset_index()
        if len(tp)>2:
            tb = pd.merge(tb,tp,how='left',on=['下单日期时间','收货区域'])
            tb = tb.fillna(0)
tb.to_excel('e:/desktop/mmix/modeldata/flx_posm.xlsx')
#------
pp2=pp[pp['分类']=='品牌提示物']
matname = pp2['物料名称'].drop_duplicates()
cate = pp2['分类'].drop_duplicates()
tb = pp2[['下单日期时间','收货区域']].drop_duplicates()
for i in matname:
    for j in cate:
        tp = pp2[(pp2['物料名称']==i)&(pp2['分类']==j)][['下单日期时间','收货区域','合计预计单品数量']]
        tp.columns = ['下单日期时间','收货区域',i+'_'+j+'_'+'合计预计单品数量']
        tp=tp.groupby(['下单日期时间','收货区域'])[i+'_'+j+'_'+'合计预计单品数量'].sum().reset_index()
        if len(tp)>2:
            tb = pd.merge(tb,tp,how='left',on=['下单日期时间','收货区域'])
            tb = tb.fillna(0)
tb.to_excel('e:/desktop/mmix/modeldata/flx_rmd.xlsx')

#edu-------------------
e1 = pd.read_excel('e:/desktop/mmix/rawdata/both_edu_2018.xlsx')
e1['服务费(单位：元)'] = e1['服务费(单位：元)']+e1['EOT酒店费用(单位：元)']
e1 = e1[['活动客户所在城市','实际执行时间','实际培训产品','实际人数','服务费(单位：元)']].fillna(0)
e1.columns = ['活动客户所在城市','实际执行时间','实际培训产品','实际人数','服务费']
e2 = pd.read_excel('e:/desktop/mmix/rawdata/both_edu_2017.xlsx')
e2['服务费'] = e2['服务费']+e2['EOT酒店费']
e2 = e2[['活动客户所在城市','实际执行时间','实际培训产品','实际人数','服务费', ]].fillna(0)

e = pd.concat([e1,e2],axis=0)

e['实际执行时间'] = e['实际执行时间'].map(lambda x:str(x)).str.split('-').map(lambda x:'/'.join([str(x[0]),str(x[1]),'1']))

ee = e[e['实际培训产品'].str.contains('辅舒良')]
ee = ee.groupby(['活动客户所在城市', '实际执行时间'])['实际人数', '服务费'].sum().reset_index()
ee.to_excel('e:/desktop/mmix/modeldata/flx_edu.xlsx')



#app----------------
f = pd.read_excel('e:/desktop/mmix/rawdata/both_app_161718.xlsx',sheet_name='辅舒良')
f.columns = ['品牌名称', 'City', 'Year', 'Month', 'flx_扫码量', 'flx_折扣额']

f = f[['City', 'Month', 'flx_扫码量', 'flx_折扣额']]
f.to_excel('e:/desktop/mmix/modeldata/flx_app.xlsx')


#competitor TV GRP

lis = ['FLX_CompetitorTVGRP_17.xlsx','FLX_CompetitorTVGRP_16.xlsx']
contb = pd.DataFrame(columns=['标题','Date','城市','毛评点'])
for i in lis:
    t = pd.read_excel('e:/desktop/mmix/rawdata/%s'%i,sheet_name='载体')
    #t.columns = t.loc[1]
    t = t[2:]
    #t2 = pd.read_excel('e:/desktop/mmix/rawdata/FBD_TVOTV_161718/MMM- FBD 2016 TV Spending.xls')
   
    t = t.fillna(0)
    t['channelgroup'] = '地方台'
    t.loc[t['频道'].str.contains('卫视'),'channelgroup']='卫视'
    t.loc[t['频道'].str.contains('中央'),'channelgroup']='央视'
    cgroup = t['channelgroup'].drop_duplicates()
    
    
    tb = pd.DataFrame(columns=['标题','日期','城市','毛评点'])
    for i in t.columns[6:-2]:
        print(i)
        tt = t[['标题','日期']]
        tt['城市'] = i
        tt['毛评点'] = t[[i]]
        
        tb = pd.concat([tb,tt],axis=0,ignore_index = True)
    
    tb['Date'] = tb['日期'].str.split('/').map(lambda x:'/'.join([str(x[0]),str(x[1]),str('1')]))
    tb['城市'] = tb['城市'].str.split("(").map(lambda x:x[0])
    
    tb[tb['毛评点']!='.'].dtypes
    tb=tb[tb['毛评点']!='.'].groupby(['标题','Date','城市'])['毛评点'].sum().reset_index()
    contb = pd.concat([contb,tb],ignore_index=True)

contb.to_excel('e:/desktop/mmix/modeldata/flx_competitors_tvGRP.xlsx')



#competitor TV SPD

fs = pd.read_excel('e:/desktop/mmix/rawdata/FLX_CompetitorTVSPD_16.xlsx',sheet_name='Sheet1')

fs['TV'] = '地方台'
fs.loc[fs['媒体(中)'].str.contains('卫视'),'TV']='卫视'
fs.loc[fs['媒体(中)'].str.contains('中央'),'TV']='央视'

fs['日期'] = fs['日期'].apply(lambda x:str(x).split('-')[0]+'/'+str(x).split('-')[1]+'/1')
#['媒体(中)','费用1(RMB)','日期','产品(中)']

Brand = fs['产品(中)'].drop_duplicates()
Tv  = fs['TV'].drop_duplicates()

tb = fs['日期'].drop_duplicates()
tb = pd.DataFrame(tb)
tb.columns=['Date']
for i in Brand:
    for j in Tv:
        tp = fs[(fs['产品(中)']==i)&(fs['TV']==j)][['日期','费用1(RMB)']]
        tp = tp.groupby(['日期'])['费用1(RMB)'].sum().reset_index()
        tp.columns = ['Date',i+'_'+j+'_'+'Spending']
        if len(tp)>0:
            tb = pd.merge(tb,tp,how='left',on=['Date'])
tb.fillna(0,inplace=True)
tb.to_excel('e:/desktop/mmix/modeldata/flx_competitors_tvspd.xlsx')





##competitordigital
d = pd.read_excel('e:/desktop/mmix/rawdata/FLX_Competitordigital_161718.xlsx',sheet_name='Sheet1')
#d.columns = d.loc[1]
#d = d[2:]

brand = d['品牌'].drop_duplicates()
IModealEName = d['广告形式'].drop_duplicates()
mediacate = d['媒体类别'].drop_duplicates()
d['投放时间'] = d['投放时间'].map(lambda x:str(x)[:4]+'/'+str(int(str(x)[4:]))+'/1')

tb = pd.DataFrame(d['投放时间'].drop_duplicates())
for i in brand:
    for j in IModealEName:
        for k in mediacate:
            tp = d[(d['品牌']==i)&(d['广告形式']==j)&(d['媒体类别']==k)][['投放时间','投放天次','预估费用']]
            tp = tp.groupby(['投放时间'])['投放天次','预估费用'].sum().reset_index()
            tp.columns = ['投放时间',i+'_'+j+'_'+k+'_'+'投放天次',i+'_'+j+'_'+k+'_'+'预估费用']
            if len(tp)>0:
                tb = pd.merge(tb,tp,how='left',on=['投放时间'])
tb.fillna(0,inplace=True)
tb.to_excel('e:/desktop/mmix/modeldata/flx_competitordigital.xlsx')


##competitorOOH

o = pd.read_excel('e:/desktop/mmix/rawdata/FLX_CompetitorOOH_161718.xlsx',sheet_name='数据导出结果')
brand = o['品牌'].drop_duplicates()
mediacate = o['媒体小类'].drop_duplicates()
mediatype = o['发布形式'].drop_duplicates()

o['监测日期'] = pd.to_datetime(o['监测日期']).map(lambda x:str(x).split('-')[0]+'/'+str(x).split('-')[1]+'/1')
tb = o[['市场','监测日期']].drop_duplicates()
oo = o.groupby(['市场','监测日期','品牌','媒体小类','发布形式'])['投放总额（元）'].sum().reset_index()

for i in brand:
    for j in mediacate:
        for k in mediatype:
            tp = oo[(oo['品牌']==i)&(oo['媒体小类']==j)&(oo['发布形式']==k)][['市场','监测日期','投放总额（元）']]
            tp.columns = ['市场','监测日期',i+'_'+j+'_'+k+'_'+'投放总额']
            if len(tp)>1:
                tb=pd.merge(tb,tp,how='left',on=['市场','监测日期'])
tb.fillna(0,inplace=True)

tb.to_excel('e:/desktop/mmix/modeldata/flx_competitorOOH.xlsx')

#social
s = pd.read_excel('e:/desktop/mmix/rawdata/FLX_social_161718.xlsx',sheet_name='微信')
s.fillna(0,inplace=True)
s.to_excel('e:/desktop/mmix/modeldata/flx_social.xlsx')


#FLX_digital
d = pd.read_excel('e:/desktop/mmix/rawdata/FLX_digital&ooh_161718.xlsx',sheet_name='Sheet1')
d['年']=d['年'].map(lambda x:str(int(x)))
d['月']=d['月'].map(lambda x:str(int(x))+'/1')
d['Date'] = d['年'].str.cat(d['月'],sep='/')

d = d.groupby(['网站', 'Type','Targeting/Non targeting','Date'])['浏览量', '点击量', '实际花费'].sum().reset_index()

platform = d['网站'].drop_duplicates()
Type = d['Type'].drop_duplicates()
target = d['Targeting/Non targeting'].drop_duplicates()
tb = pd.DataFrame(d['Date'].drop_duplicates())
for i in platform:
    for j in Type:
        for k in target:
            tp = d[(d['网站']==i)&(d['Type']==j)&(d['Targeting/Non targeting']==k)][['Date','浏览量', '点击量', '实际花费']]
            tp.columns = ['Date',i+'_'+j+'_'+k+'_'+'浏览量', i+'_'+j+'_'+k+'_'+'点击量', i+'_'+j+'_'+k+'_'+'实际花费']
            if len(tp)>0:
                tb = pd.merge(tb,tp,how='left',on = ['Date'])
tb = tb.fillna(0)

tb.to_excel('e:/desktop/mmix/modeldata/fbd_digital.xlsx')

#################################################################

#tvspd

lis = os.listdir('e:/desktop/mmix/rawdata/FLX_TVOTV_161718/TV+OTV/TV spending')
spd = pd.DataFrame(columns=['Month','Media','Spending'])
for i in lis:
    f = pd.read_excel('e:/desktop/mmix/rawdata/FLX_TVOTV_161718/TV+OTV/TV spending/%s'%i)
    f = f[['Month','Media','辅舒良']]
    f.columns=['Month','Media','Spending']
    spd = pd.concat([spd,f],axis=0,ignore_index=True)
        
spd['channel'] = '地方台'
spd.loc[spd['Media'].str.contains('卫视'),'channel']='卫视'
spd.loc[spd['Media'].str.contains('中央'),'channel']='央视'
spd = spd[['Month','channel','Spending']]

tp=pd.DataFrame(spd['Month'].drop_duplicates())
tp.Month=tp.Month.astype(int,inplace=True)
for i in spd.channel.drop_duplicates():
    tb = spd[spd.channel==i][['Month','Spending']]
    tb=tb.groupby(['Month'])['Spending'].sum().reset_index()
    tb.columns=['Month',i+'_Spending']
    tp = pd.merge(tp,tb,how='left',on=['Month'])
tp.fillna(0,inplace=True)
tp.to_excel('e:/desktop/mmix/modeldata/flx_tvspd.xlsx')








