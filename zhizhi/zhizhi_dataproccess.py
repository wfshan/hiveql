# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 14:02:57 2018

@author: wfsha
"""

import pandas as pd
from coordTransform_utils import bd09_to_wgs84
import numpy as np


#############profile

f = pd.read_csv('E:/Desktop/jinan/allslide2/allslides2.csv')

#fp3 = pd.read_csv('E:/Desktop/jinan/p3slide/p3slides.csv')

fp1 = pd.read_csv('E:/Desktop/jinan/p1slide2/p1slides2.csv')

f.columns = ['i','ptype','lat','lon','iscore','gender','age','n']
   #fp3.columns = ['i','date','ptype','city','lat','lon','local','gender','age','n']
#fp3 = fp3[['ptype','lat','lon','local','gender','age','n']]
fp = fp3[(fp3.ptype == 1)]

fp1.columns = ['i','ptype','lat','lon','iscore','gender','age','n']
fp1 = fp1[['ptype','lat','lon','iscore','gender','age','n']]
fp = fp1[(fp1.ptype == 1)]

s = sum(fp.n)
fx = 3148410/s

fp.ptype = 2
fp.n = fp.n*fx

final = pd.concat([f,fp],axis = 0)
sum(final[final.ptype == 1].n)


########################poi

#car'车'
#stay'地名|住宅'
#shop'购物'
#rest'餐饮'
#trans'通行设施|交通设施服务|道路附属设施'
#edu'科教文化服务'
#hos'医疗保健服务'

def iscar(s):
    return '车' in s

def isstay(s):
    return ('地名' in s) or ('住宅' in s)

def isshop(s):
    return '购物' in s

def isrest(s):
    return '餐饮' in s

def istrans(s):
    return ('通行设施' in s) or ('交通设施服务' in s) or ('道路附属设施' in s)

def isedu(s):
    return '科教文化服务' in s

def ishos(s):
    return '医疗保健服务' in s




poi = pd.read_excel('E:/Desktop/jinan/2018济南poi .xlsx')
poi['typelabel'] = 'others'
poi.loc[list(map(iscar,poi.type)),'typelabel'] = 'car'
poi.loc[list(map(isstay,poi.type)),'typelabel'] = 'stay'
poi.loc[list(map(isshop,poi.type)),'typelabel'] = 'shop'
poi.loc[list(map(isrest,poi.type)),'typelabel'] = 'rest'
poi.loc[list(map(istrans,poi.type)),'typelabel'] = 'trans'
poi.loc[list(map(isedu,poi.type)),'typelabel'] = 'edu'
poi.loc[list(map(ishos,poi.type)),'typelabel'] = 'hos'

['car','stay','shop','rest','trans','edu','hos','others']

newlist = pd.DataFrame(list(map(bd09_to_wgs84,poi['bdx'],poi['bdy'])))
poi['wgslon'] = newlist[0]
poi['wgslat'] = newlist[1]


def wgs_to_grid(lon,lat):
    slon = 116.22606588
    slat = 36.03114099
    mlon = 0.00279126825981685
    mlat = 0.00225487243034554
    lon1 = int((lon-slon)/mlon)
    lat1 = int((lat-slat)/mlat) 
    return [lon1,lat1]

newlist = pd.DataFrame(list(map(wgs_to_grid,poi['wgslon'],poi['wgslat'])))
poi['lon'] = newlist[0]
poi['lat'] = newlist[1]


poi['loncent'] = poi['lon']+0.5
poi['latcent'] = poi['lat']+0.5

poi['lonupright'] = poi['lon']+1
poi['latupright'] = poi['lat']+1

['name', 'type', 'tel', 'locationx', 'locationy', 'tag', 'addr',
       'province', 'city', 'citycode', 'district', 'street', 'adcode',
       'typecode', 'address', 'cityname', 'number', 'gpsx', 'gpsy', 'bdx',
       'lonupright', 'latupright']

poi.groupby(['lon', 'lat', 'loncent', 'latcent','lonupright', 'latupright','typelabel'])['typelabel'].count()

p = poi[['name','type','locationx','locationy','district','street', 'adcode','typecode','gpsx','gpsy', 'bdx','bdy','wgslon','wgslat','lon','lat','loncent','latcent','lonupright', 'latupright', 'isin', 'typelabel']]

p.to_excel('E:/Desktop/jinan/jinanlabel.xlsx',encoding = 'utf8')


#########merge




p = pd.read_csv('E:/Desktop/jinan/jinanlabel.csv')
p = p[['name','type','district','typecode','lon','lat','loncent','latcent','lonupright', 'latupright','typelabel']]


f = pd.read_csv('E:/Desktop/jinan/final.csv')

f1 = f
conc = f1.groupby(['lon','lat'])['n'].sum().reset_index()
conc.columns = ['lon','lat','count']
#ptype
for i in [0,1,2]:
    for j in ['M','F']:
        s = 'ptype'+str(i)+'gender'+str(j)
        ff = f1[(f1.ptype==i)&(f1.gender == j)].groupby(['lon','lat'])['n'].sum().reset_index()
        conc = conc.merge(ff,on = ['lon','lat'],how = 'left')
        conc = conc.rename(columns={'n':s})
for i in [0,1,2]:       
    for j in ['Y','N']:
        s = 'ptype'+str(i)+'iscore'+str(j)
        ff = f1[(f1.ptype==i)&(f1.iscore == j)].groupby(['lon','lat'])['n'].sum().reset_index()
        conc = conc.merge(ff,on = ['lon','lat'],how = 'left')
        conc = conc.rename(columns={'n':s})
        
for i in [0,1,2]:       
    for j in ['70+','65-69','60-64','55-59','50-54','45-49','40-44','35-39','30-34','25-29','19-24','16-18','13-15','7-12','0-6']:
        s = 'ptype'+str(i)+'age'+str(j)
        ff = f1[(f1.ptype==i)&(f1.age == j)].groupby(['lon','lat'])['n'].sum().reset_index()
        conc = conc.merge(ff,on = ['lon','lat'],how = 'left')
        conc = conc.rename(columns={'n':s})

conc.to_csv('E:/Desktop/jinan/profile_label.csv')



p1 = p.groupby(['lon', 'lat', 'loncent', 'latcent','lonupright', 'latupright','typelabel'])['name'].count()
p1 = p1.reset_index()
p1.columns = ['lon', 'lat', 'loncent', 'latcent','lonupright', 'latupright','typelabel','count']

for i in ['car','stay','shop','rest','trans','edu','hos','others']:
    p1[i] = 0
    p1.loc[p1.typelabel==i,i] = p1.loc[p1.typelabel==i,'count']

p1 = p1.groupby(['lon', 'lat'])['car','stay','shop','rest','trans','edu','hos','others'].sum()
p1 = p1.reset_index()

p1.to_csv('E:/Desktop/jinan/poi_label.csv')


x = pd.merge(conc,p1,on = ['lon','lat'],how = 'left')
#x = x[~x['ptype'].isnull()]
x.to_csv('E:/Desktop/jinan/prof_poi.csv')

