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

#writer = pd.ExcelWriter('E:/desktop/mmix/fbd_modeldata.xlsx')
#sales
f = pd.read_excel('e:/desktop/mmix/PTR Data for FBD&FLX MMM_18M06.xlsx')
f = f[f['Brand'].str.contains('FENBID')]
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
                    
                    if len(tp)>0:
                       tb = pd.merge(tb,tp,how='left',on=['audit_cd','Date'])
                       print(i,j,k,n,m,len(tb))
tb=tb.fillna(0)
tb.to_excel('e:/desktop/mmix/modeldata/fbd_sales.xlsx')     
f[['audit_cd','Date']].drop_duplicates().to_excel('e:/desktop/mmix/citymonth.xlsx')


#######brand sales
f = pd.read_excel('e:/desktop/mmix/PTR Data for FBD&FLX MMM_18M06.xlsx')

f['Date'] = f['Date'].map(lambda x:str(x).split('-')[0]+'/'+str(int(str(x).split('-')[1]))+'/1')
tb = f[['audit_cd','Date']].drop_duplicates()

f = f.groupby(['audit_cd','Date','Brand'])['VAL','PACK','ND','WD'].sum().reset_index()
brand = f['Brand'].drop_duplicates()

for i in brand:
    tp = f[(f['Brand']==i)][['audit_cd','Date','VAL','PACK','ND','WD']]
    sn = str(i+'_')
    tp.columns = ['audit_cd','Date',sn+'VAL',sn+'PACK',sn+'ND',sn+'WD']
    if len(tp)>0:
        tb = pd.merge(tb,tp,how='left',on=['audit_cd','Date'])
tb=tb.fillna(0)
tb.to_excel('e:/desktop/mmix/modeldata/brand_sales.xlsx') 
-------------
##underling
u = pd.read_excel('e:/desktop/mmix/fbd_underlying_161718.xlsx',sheet_name='total')
u.to_excel('e:/desktop/mmix/modeldata/fbd_underlying.xlsx') 
--------
#CompetitorSales


#otv
o = pd.read_excel('e:/desktop/mmix/rawdata/MMM- FBD 2016-2018.Jun OTV_0910.xlsx')
o = o.groupby(['Year', 'Month', 'Market ', 'Media Platform', 'PC/Mobile/OTT',' Impression（total）', ' Impression（TA）', 'Universe-city', 'iGRP','Population-city', 'GRP', 'Population-全国','Population-27mkt', 'Click-Total', 'Click-TA'])['Spending'].sum().reset_index()
o['Year'] = o['Year'].map(lambda x:str(int(x)))
o['Month'] = o['Month'].map(lambda x:str(int(x)))
o['Date'] = o['Year'].str.cat(o['Month'],sep='/')

otb = o[['Date','Market ','Population-city','Population-全国','Population-27mkt']].drop_duplicates()
['Date','Market ','Population-city','Population-全国','Population-27mkt']


platform = o['Media Platform'].drop_duplicates()
device = o['PC/Mobile/OTT'].drop_duplicates()

col = [i for i in o.columns[5:-1] if i not in ['Date','Market ','Population-city','Population-全国','Population-27mkt','Universe-city']]

for i in platform:
    for j in device:
        tp = o[(o['Media Platform']==i)&(o['PC/Mobile/OTT']==j)][['Date','Market ']+col]
        sn = str(i+'_'+j)
        co = [sn+'_'+n for n in col]
        tp.columns = ['Date','Market ']+co
        tp.drop_duplicates()
        if len(tp)>2:
            otb = pd.merge(otb,tp,how='outer',on=['Date','Market '])
            print(i,j,len(otb))

otb = otb.fillna(0)
otb = otb.groupby(['Date', 'Market '])[otb.columns[5:]].sum().reset_index()
otb.to_excel('e:/desktop/mmix/modeldata/fbd_otv.xlsx')

#tv
lis = ['MMM- FBD 2016 TV GRP.xlsx','MMM- FBD 2017 TV GRP.xlsx','MMM- FBD 2018 TV 1-6 GRP.xlsx']
contb = pd.DataFrame(columns=['广告名称','Date','城市','毛评点'])
for i in lis:
    t = pd.read_excel('e:/desktop/mmix/rawdata/FBD_TVOTV_161718/%s'%i)
    t.columns = t.loc[1]
    t = t[3:]
    #t2 = pd.read_excel('e:/desktop/mmix/rawdata/FBD_TVOTV_161718/MMM- FBD 2016 TV Spending.xls')
   
    t = t.fillna(0)
    t['channelgroup'] = '地方台'
    t.loc[t['频道'].str.contains('卫视'),'channelgroup']='卫视'
    t.loc[t['频道'].str.contains('中央'),'channelgroup']='央视'
    cgroup = t['channelgroup'].drop_duplicates()
    
    
    tb = pd.DataFrame(columns=['广告名称','日期','城市','毛评点'])
    for i in t.columns[8:-1]:
        print(i)
        tt = t[['广告名称','日期']]
        tt['城市'] = i
        tt['毛评点'] = t[[i]]
        
        tb = pd.concat([tb,tt],axis=0,ignore_index = True)
    
    tb['Date'] = tb['日期'].str.split('/').map(lambda x:'/'.join([str(x[0]),str(x[1]),str('1')]))
    tb['城市'] = tb['城市'].str.split("(").map(lambda x:x[0])
    
    tb[tb['毛评点']!='.'].dtypes
    tb=tb[tb['毛评点']!='.'].groupby(['广告名称','Date','城市'])['毛评点'].sum().reset_index()
    contb = pd.concat([contb,tb],ignore_index=True)

contb.groupby(['Date', '城市'])['毛评点'].sum().reset_index()
contb.to_excel('e:/desktop/mmix/modeldata/fbd_tv.xlsx')


#sem

s = pd.read_excel('e:/desktop/mmix/rawdata/FBD_SEM_161718.xlsx')
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
            if len(tp)>2:
                tb = pd.merge(tb,tp,how='left',on=['Date','Market'])
                tb = tb.fillna(0)
#tb = tb.groupby(['Market','Date'])['Clicks','Impressions','Actual Spending (RMB)'].sum().reset_index()
tb.to_excel('e:/desktop/mmix/modeldata/fbd_sem.xlsx')


#posm&remaind

p16 = pd.read_excel('e:/desktop/mmix/rawdata/FBD_rmd_16的副本.xlsx')
p16 = p16[1:]
p16.columns = ['收货区域', '数量', 'total cost', '2016/7/1', '2016/8/1', '2016/9/1', '2016/10/1', '2016/11/1', '2016/12/1']
tb16 = pd.DataFrame(columns=['City','Date','Cost'])
for i in p16.columns[3:]:
    tp = p16[['收货区域',i]]
    tp['Date'] = i
    tp = tp[['收货区域','Date',i]]
    tp.columns = ['City','Date','Cost']
    tb16 = pd.concat([tb16,tp],axis=0)
tb16['分类'] = '品牌提示物'
tb16['合计预计单品数量'] = 0
tb16['物料名称']='芬必得保温杯--面向消费者-品牌提示物'
tb16.columns = ['收货区域','下单日期时间','成本（含税）','分类','合计预计单品数量','物料名称']

p = pd.read_excel('e:/desktop/mmix/rawdata/fbd_posm&rmd_1718.xlsx',sheet_name='总表')
p = p[['货主简称','物流订单号','下单日期时间','收货区域','物料代码','物料名称','合计预计单品数量','规格','分类','品牌']]
pcost = pd.read_excel('e:/desktop/mmix/rawdata/POSM and brand reminder cost - Fenbid.xlsx')

pcost.columns = ['分类2', '物料代码', '物料名称', '成本（含税）']
pcost = pcost[['物料代码','成本（含税）']].drop_duplicates()
pp = pd.merge(p,pcost,how = 'left',on =['物料代码'])
pp = pp[['收货区域','下单日期时间','成本（含税）','分类','合计预计单品数量','物料名称']]
pp['下单日期时间'] = pp['下单日期时间'].map(lambda x:str(x)).str.split('-').map(lambda x:'/'.join([str(x[0]),str(x[1]),str(1)]))

pp = pd.concat([pp,tb16],axis=0)

rmd = pp[pp['分类']=='品牌提示物']
#rmdt =  pd.read_excel('e:/desktop/mmix/rawdata/fbd_posm&rmd_1718.xlsx',sheet_name='总表')
#rmd = pd.merge(rmd,rmdt,how='left',on='物料名称')

matname = rmd['物料名称'].drop_duplicates()
tb = pp[['下单日期时间','收货区域']].drop_duplicates()
for i in matname:
    tp = rmd[(rmd['物料名称']==i)][['下单日期时间','收货区域','合计预计单品数量','成本（含税）']]
    tp.columns = ['下单日期时间','收货区域',i+'_'+'合计预计单品数量',i+'_'+'成本（含税）']
    tp=tp.groupby(['下单日期时间','收货区域'])[i+'_'+'合计预计单品数量',i+'_'+'成本（含税）'].sum().reset_index()
    if len(tp)>0:
        tb = pd.merge(tb,tp,how='left',on=['下单日期时间','收货区域'])
        tb = tb.fillna(0)
tb.to_excel('e:/desktop/mmix/modeldata/fbd_rmd.xlsx')

#--------
po = pp[pp['分类']=='POSM']
matname = po['物料名称'].drop_duplicates()
tb = pp[['下单日期时间','收货区域']].drop_duplicates()
for i in matname:
    tp = po[(po['物料名称']==i)][['下单日期时间','收货区域','合计预计单品数量','成本（含税）']]
    tp.columns = ['下单日期时间','收货区域',i+'_'+'合计预计单品数量',i+'_'+'成本（含税）']
    tp=tp.groupby(['下单日期时间','收货区域'])[i+'_'+'合计预计单品数量',i+'_'+'成本（含税）'].sum().reset_index()
    if len(tp)>2:
        tb = pd.merge(tb,tp,how='left',on=['下单日期时间','收货区域'])
        tb = tb.fillna(0)
tb.to_excel('e:/desktop/mmix/modeldata/fbd_posm.xlsx')



#edu
lis = [i for i in os.listdir('e:/desktop/mmix/rawdata/') if 'edu' in i]

e1 = pd.read_excel('e:/desktop/mmix/rawdata/both_edu_2018.xlsx')
e1['服务费(单位：元)'] = e1['服务费(单位：元)']+e1['EOT酒店费用(单位：元)']
e1 = e1[['活动客户所在城市','实际执行时间','实际培训产品','实际人数','服务费(单位：元)']].fillna(0)
e1.columns = ['活动客户所在城市','实际执行时间','实际培训产品','实际人数','服务费']
e2 = pd.read_excel('e:/desktop/mmix/rawdata/both_edu_2017.xlsx')
e2['服务费'] = e2['服务费']+e2['EOT酒店费']
e2 = e2[['活动客户所在城市','实际执行时间','实际培训产品','实际人数','服务费', ]].fillna(0)

e3 = pd.read_excel('e:/desktop/mmix/rawdata/FBD_edu_16.xlsx')
def ola(s):
    s = str(s)
    if '月' in s:
        x = re.findall(r'\d*月',s)[0][:-1]
        xx = '2016-%s-1'%x
    else:
        x = s.split('-')[1]
        xx = '2016-%s-1'%x
    return xx
        
e3.实际执行时间 = e3.实际执行时间.apply(lambda x:ola(x))


e = pd.concat([e1,e2,e3],axis=0)

e['实际执行时间'] = e['实际执行时间'].map(lambda x:str(x)).str.split('-').map(lambda x:'/'.join([str(x[0]),str(x[1]),'1']))

ee = e[e['实际培训产品'].str.contains('芬')]
ee = ee.groupby(['活动客户所在城市', '实际执行时间'])['实际人数', '服务费'].sum().reset_index()
ee.to_excel('e:/desktop/mmix/modeldata/fbd_edu.xlsx')



#app
f300 = pd.read_excel('e:/desktop/mmix/rawdata/both_app_161718.xlsx',sheet_name='芬300')
f400 = pd.read_excel('e:/desktop/mmix/rawdata/both_app_161718.xlsx',sheet_name='芬400')
f300.columns = ['品牌名称', 'Market (City)', 'Year', '月份', 'fbd300_扫码量', 'fbd300_折扣额']
f400.columns = ['品牌名称', 'Market (City)', 'Year', '月份', 'fbd400_扫码量', 'fbd400_折扣额']
f300 = f300[['Market (City)','月份', 'fbd300_扫码量', 'fbd300_折扣额']]
f400 = f400[['Market (City)','月份', 'fbd400_扫码量', 'fbd400_折扣额']]


f = pd.merge(f300,f400,how='outer',on=[ 'Market (City)', '月份'])
f = f.groupby(['Market (City)', '月份'])['fbd300_扫码量', 'fbd300_折扣额', 'fbd400_扫码量','fbd400_折扣额'].sum().reset_index()
f = f.fillna(0)
f.to_excel('e:/desktop/mmix/modeldata/fbd_app.xlsx')


#competitor TV GRP

lis = ['2016.1-2016.12','2017.1-2017.12','2018.1-2018.6']
contb = pd.DataFrame(columns=['广告名称','Date','城市','毛评点','weighted毛评点'])
for i in lis:
    t = pd.read_excel('e:/desktop/mmix/rawdata/FBD_CompetitorTVGRP_161718.xlsx',sheet_name=i)
    #t.columns = t.loc[1]
    t = t[2:]
    #t2 = pd.read_excel('e:/desktop/mmix/rawdata/FBD_TVOTV_161718/MMM- FBD 2016 TV Spending.xls')
   
    t = t.fillna(0)
    t.rename(columns={t.columns[1]:'广告名称',t.columns[2]:'频道',t.columns[6]:'日期'},inplace=True)
    t['channelgroup'] = '地方台'
    t.loc[t['频道'].str.contains('卫视'),'channelgroup']='卫视'
    t.loc[t['频道'].str.contains('中央'),'channelgroup']='央视'
    cgroup = t['channelgroup'].drop_duplicates()
    
    
    tb = pd.DataFrame(columns=['广告名称','日期','城市','毛评点','weighted毛评点'])
    lis = t.columns[10:-1]
    for i in range(int(len(lis)/2)):
        x = 2*i
        print(lis[x])
        tt = t[['广告名称','日期']]
        tt['城市'] = lis[x]
        tt['毛评点'] = t[[lis[x]]]
        tt['weighted毛评点'] = t[[lis[x+1]]]
        
        tb = pd.concat([tb,tt],axis=0,ignore_index = True)
    
    tb['Date'] = tb['日期'].map(lambda x:str(x)).str.split('-').map(lambda x:'/'.join([str(x[0]),str(x[1]),str('1')]))
    #tb['城市'] = tb['城市'].str.split("(").map(lambda x:x[0])
    
    tb.replace('.',0,inplace=True)
    tb=tb.groupby(['广告名称','Date','城市'])['毛评点','weighted毛评点'].sum().reset_index()
    contb = pd.concat([contb,tb],ignore_index=True)
contb = contb.groupby(['Date', '城市'])['毛评点', 'weighted毛评点'].sum().reset_index()
contb.to_excel('e:/desktop/mmix/modeldata/fbd_competitors_tv.xlsx')

#competitor TV SPD

fs = pd.read_excel('e:/desktop/mmix/rawdata/FBD_CompetitorTVSPD_161718.xlsx')
x = fs
fs.loc[fs['Actual Spending'].isna(),'Actual Spending'] = fs[fs['Actual Spending'].isna()]['Spending 000']

fs['Day'] = '1'
fs[['Year','Month']]=fs[['Year','Month']].astype(str)
fs['Date']=fs['Year'].str.cat([fs['Month'],fs['Day']],sep='/')
del fs['Day'],fs[0]

['Brand-C','Date','TV','Actual Spending']

Brand = fs['Brand-C'].drop_duplicates()
Tv  = fs['TV'].drop_duplicates()

tb = fs['Date'].drop_duplicates()
tb = pd.DataFrame(data=tb,columns=['Date'])
for i in Brand:
    for j in Tv:
        tp = fs[(fs['Brand-C']==i)&(fs['TV']==j)][['Date','Actual Spending']]
        tp = tp.groupby(['Date'])['Actual Spending'].sum().reset_index()
        tp.columns = ['Date',i+'_'+j+'_'+'Actual Spending']
        if len(tp)>0:
            tb = pd.merge(tb,tp,how='left',on=['Date'])
tb.fillna(0,inplace=True)
tb.to_excel('e:/desktop/mmix/modeldata/fbd_competitors_tvspd.xlsx')





##digital
lis =['2016','2017','2018']
tb = pd.DataFrame()
for i in lis:
    d = pd.read_excel('e:/desktop/mmix/rawdata/FBD_digital_161718.xlsx',sheet_name='%s'%i)
    tb=pd.concat([tb,d],axis=0,ignore_index=True)
tb=tb.groupby(['date','product','platform','Type'])['Impression','Spending'].sum().reset_index()
product=tb['product'].drop_duplicates()
platform=tb['platform'].drop_duplicates()
Type=tb['Type'].drop_duplicates()
tp=pd.DataFrame(tb['date'].drop_duplicates())
for i in product:
    for j in platform:
        for k in Type:
            tbb=tb[(tb['product']==i)&(tb['platform']==j)&(tb['Type']==k)][['date','Impression','Spending']]
            tbb.columns = ['date',i+'_'+j+'_'+k+'_'+'Impression',i+'_'+j+'_'+k+'_'+'Spending']
            if len(tbb)>0:
                tp = pd.merge(tp,tbb,how='left',on=['date']).fillna(0)
tp['date'] = tp.date.apply(lambda x:str(x).split('-')[0]+'/'+str(x).split('-')[1]+'/1')
tp = tp.groupby(['date'])[tp.columns[1:]].sum().reset_index()

tp.to_excel('e:/desktop/mmix/modeldata/fbd_digital.xlsx')

#social
s = pd.read_excel('e:/desktop/mmix/rawdata/FBD_social_161718.xlsx',sheet_name='Sheet1')




s.to_excel('e:/desktop/mmix/modeldata/fbd_social.xlsx')

##allergy

al = pd.read_excel('e:/desktop/mmix/墨迹2017年8月16日至2018年5月31日过敏数据-final.xlsx')
li = list(al.columns)
for i in li:
    
    
    
    
    
#tvspd

lis = os.listdir('e:/desktop/mmix/rawdata/FBD_TVOTV_161718')
spd = pd.DataFrame(columns=['Month','Media','Spending'])
for i in lis:
    if 'Spending' in i:
        f = pd.read_excel('e:/desktop/mmix/rawdata/FBD_TVOTV_161718/%s'%i)
        f = f[['Month','Media','芬必得']]
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
tp.to_excel('e:/desktop/mmix/modeldata/fbd_tvspd.xlsx')
