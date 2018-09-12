import pandas as pd
import json
from coordTransform_utils import wgs84_to_bd09

def run():
    data = pd.read_csv('E:/Desktop/grid_count/beijinggrid2.csv')
    result = []
    counter = 0
    for (bdlon, bdlat), coord_group in data.groupby(['bdlon', 'bdlat']):
        item = dict({'city': '北京'})
        box = dict({'type': 'Polygon', 'coordinates': []})
        box['coordinates'] = [[
            [bdlon, bdlat],
            [bdlon+0.002928871, bdlat],
            [bdlon, bdlat+0.002253563],
            [bdlon+0.002928871, bdlat+0.002253563]
        ]]
        center = dict({'type': 'Point', 'coordinates': []})
        center['coordinates'] = [bdlon+0.002928871/2, bdlat+0.002253563/2]
        item['box'] = box
        item['center'] = center
        for pt, pt_group in coord_group.groupby('ptype'):
            if pt == 1:
                item['rd'] = lt_label(pt_group)
            elif pt == 2:
                item['wd'] = lt_label(pt_group)
        counter+=1
        print(counter,bdlon, bdlat)
        result.append(item)
    json.dump(result, open('bj_lt.json', 'w', encoding='utf-8'), ensure_ascii=False)


def lt_label(group):
    ltd = dict({'age': [], 'os': [], 'pb': [], 'pt': []})
    ltd['mc'] = group[group['gender'] == 'M']['gw'].sum()
    ltd['wc'] = group[group['gender'] == 'F']['gw'].sum()
    ltd['c'] = ltd['mc'] + ltd['wc']

    for ag, c in group.groupby(['age'])['gw'].sum().to_dict().items():
        ltd['age'].append({'l': ag, 'c': c})
    for osg, c in group.groupby(['os'])['gw'].sum().to_dict().items():
        ltd['os'].append({'l': osg, 'c': c})
    for bg, c in group.groupby(['brand'])['gw'].sum().to_dict().items():
        ltd['pb'].append({'l': bg, 'c': c})
    for tg, c in group.groupby(['type'])['gw'].sum().to_dict().items():
        ltd['pt'].append({'l': tg, 'c': c})

    return ltd


if __name__ == '__main__':
    run()

    
 #########################################################pre-process

fp1 = pd.read_csv('E:/Desktop/grid_count/pslide/pslide.csv')
fp1 = fp1[['age','gender','brand','type','ptype','lon','lat','gw']]
f = pd.read_csv('E:/desktop/grid_count/beijinggrid2.csv')
f = f[['age','gender','brand','type','ptype','lon','lat','gw']]


fp = fp1[(fp1.ptype == 1)]
num1 = 8023484
 #(ptype=1,workage=T,iscore=Y)
s = sum(fp.gw)
fx = num1/s
fp.ptype = 2
fp.gw = fp.gw*fx

final = pd.concat([f,fp],axis = 0)
sum(final[(final.ptype == 1)].gw)
final.to_csv('E:/Desktop/grid_count/final.csv')
f4 = pd.read_csv('E:/desktop/grid_count/final.csv')

#f4[['lon','lat','ptype','gw']] = f4[['lon','lat','ptype','gw']].apply(pd.to_numeric)
f4['os'] = '0'
f4.loc[(f4.brand == '苹果'),'os'] = 'I'
f4.loc[~(f4.brand == '苹果')&~(f4.brand.isnull()),'os'] = 'A'
f4.loc[f4.brand=='苹果','brand'] = 'IPHONE'
f4.loc[f4.brand=='欧珀','brand'] = 'OPPO'
f4.loc[f4.brand=='维沃','brand'] = 'VIVO'
f4.loc[f4.brand=='万普拉斯','brand'] = 'OnePlus'
f4.loc[f4.brand=='XIAOTIANCAI','brand'] = '小天才'
f4.loc[f4.age=='007-12','age'] = '7-12'
f4.loc[f4.age=='000-6','age'] = '0-6'
#北京
def grid_to_wgs(lon,lat):
    slon = 115.423411
    slat= 39.44275803
    mlon= 0.002928871
    mlat= 0.002253563
    wgslon = lon * mlon + slon + 0.5*mlon
    wgslat = lat * mlat + slat + 0.5*mlat
    return [wgslon,wgslat]


newlist = pd.DataFrame(list(map(grid_to_wgs,f4['lon'],f4['lat'])))
newlist = pd.DataFrame(list(map(wgs84_to_bd09,newlist[0],newlist[1])))
f4['bdlon'] = newlist[0]
f4['bdlat'] = newlist[1]



def isin(s):
    s = str(s)
    if '?' in s:
        s2 =  ''.join(s.split('?'))
    else:
        s2 = s
    return s2

ftype = pd.DataFrame(list(map(isin,f4['type'])))
f4['type'] = ftype
#f4.columns = ['lon', 'lat', 'age', 'gender', 'brand', 'type', 'ptype', 'gw', 'os','bdlon', 'bdlat']
f4.to_csv('E:/Desktop/grid_count/beijinggrid3.csv') 
