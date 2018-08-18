# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 13:23:08 2018

@author: wfsha
"""

import pandas as pd
import random
import numpy as np
import time
import sys
#sys.getsizeof()



print('startread:',time.asctime())
poi = pd.read_excel('E:/Desktop/jinan/jinanlabel.xlsx')
poi = poi[['name','lon','lat']]
label = pd.read_csv('E:/Desktop/jinan/prof_poi.csv')
print('endread:',time.asctime())
grid = label[['lon','lat']]
grid = grid.drop_duplicates()
#--------------------------------
df = label
df750 = []
for i in df.index:
    for j in range(df['lon'][i]-1,df['lon'][i]+1+1):
        for k in range(df['lat'][i]-1,df['lat'][i]+1+1):
            df750.append([df['lon'][i],df['lat'][i],j,k])
df750=pd.DataFrame(df750,columns = ['ln','lt','lon','lat'])
df750 = df750.merge(label,on=['lon','lat'],how='left')
df750 = df750.groupby(['ln','lt'])[label.columns[4:-1]].sum().reset_index()
df750.columns = ['lon','lat'] + list('750'+label.columns[4:-1])
    
la = label.merge(df750,on=['lon','lat'],how='left')
    
    
df1250 = []
for i in df.index:
    for j in range(df['lon'][i]-2,df['lon'][i]+2+1):
        for k in range(df['lat'][i]-2,df['lat'][i]+2+1):
            df1250.append([df['lon'][i],df['lat'][i],j,k])
df1250=pd.DataFrame(df1250,columns = ['ln','lt','lon','lat'])

df1250 = pd.merge(df1250,label,on = ['lon','lat'],how = 'left')
df1250 = df1250.groupby(['ln','lt'])[label.columns[4:-1]].sum().reset_index()
df1250.columns = ['lon','lat'] + list('1250'+label.columns[4:-1])
la = la.merge(df1250,on=['lon','lat'],how='left')
la.to_csv('E:/Desktop/jinan/label2507501250.csv')

##-------------------------------------------

la = pd.read_csv('E:/Desktop/jinan/label2507501250.csv')

poi = pd.read_excel('E:/Desktop/jinan/jinanlabel.xlsx')
poi = poi[['name','lon','lat']]

name = ['孟鑫']

def isin(s):
    tf = False
    for i in name:
        a = (i in s)
        tf = (tf or a)
    return tf
 


           
targ = poi.loc[list(map(isin,poi.name)),['lon','lat']]
targ = targ.drop_duplicates()
n = len(targ)

grid = la[['lon','lat']]
grid = grid.drop_duplicates()         
grid['ss'] = 0
for i in targ.index:
    grid.loc[(grid.lon == targ['lon'][i])&(grid.lat == targ['lat'][i]),'ss'] = 1
grid[grid.ss==0]  
grid = grid[['lon','lat']]

sample = grid.sample(n)

print('endprepare:',time.asctime())



def zz(df,la):
    la['l'] = 0  
    for i in df.index:
       la.loc[(la['lon']==df['lon'][i])&(la['lat']==df['lat'][i]),'l'] = 1
    la = la[la.l==1]
    return la
  
print('starttarget:',time.asctime())
target = zz(targ,la)
target.pop('l')
target.to_csv('E:/Desktop/jinan/modelf/mengxin/target.csv')

print('startsample:',time.asctime())
#sampl 
for i in range(9999):
    samp = grid.sample(n)
    sampl = zz(samp,la)
    sampl.pop('l')
    sampl.to_csv('E:/Desktop/jinan/modelf/mengxin/sample%s.csv'%i)

print('endsample:',time.asctime())



