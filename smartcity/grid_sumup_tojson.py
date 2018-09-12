import pandas as pd
import json


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
