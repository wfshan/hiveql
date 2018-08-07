--上海'V0310000'20180501
--table
create table temp_bgy_20180805pf_sh as
select tt.uid,tt.gender, tt.age, tt.area, tt.ptype, tt.gw,tt.lat,tt.lon,tt.is_core,
cast(row_number() over(partition by 1) / 100000 as int) + 1 as slides
from
(select t.uid,t.gender, t.age, t.area, t.ptype, t.gw,t.is_core,
floor((t.lat - m.slat)/m.mlat) as lat,
floor((t.lon - m.slon)/m.mlon) as lon
from (
select city_code, min(ext_min_x) as slon, min(ext_min_y) as slat,
avg(ext_max_x-ext_min_x) as mlon, avg(ext_max_y-ext_min_y) as mlat
from ss_grid_wgs84
where city_code = 'V0310000'
group by city_code
) m inner join (
select x.uid, x.age, x.gender, x.area, x.prov_id, x.grid_id, x.ptype, x.gw,x.is_core,
s.weighted_centroid_lon as lon, s.weighted_centroid_lat as lat
from (
select a.uid, a.area, b.prov_id, a.grid_id, a.ptype, a.gw,a.is_core,
case when a.gender='01' then 'M'
when a.gender = '02' then 'F'
end as gender,
case when a.age = '01' then '0-6'
when a.age = '02' then '7-12'
when a.age = '03' then '13-15'
when a.age = '04' then '16-18'
when a.age = '05' then '19-24'
when a.age = '06' then '25-29'
when a.age = '07' then '30-34'
when a.age = '08' then '35-39'
when a.age = '09' then '40-44'
when a.age = '10' then '45-49'
when a.age = '11' then '50-54'
when a.age = '12' then '55-59'
when a.age = '13' then '60-64'
when a.age = '14' then '65-69'
when a.age = '15' then '70+'
end as age
from area_code b
inner join (select sm.uid,sm.is_core, ua.area, sm.grid_id, ua.gender, ua.age, sm.ptype, ua.gw
from stay_month sm
inner join user_attribute ua
on sm.uid = ua.uid
where sm.date = 20180501 and sm.city = 'V0310000' and ua.date = 20180501 and ua.city = 'V0310000'
group by sm.uid, ua.area, sm.grid_id, ua.gender, ua.age, sm.ptype, ua.gw,sm.is_core) a
on a.area = b.area_id
) x
inner join stay_poi s
on x.uid = s.uid and x.grid_id = s.final_grid_id
where s.date = 20180501 and s.city = 'V0310000'
) t ) tt
group by tt.uid,tt.gender, tt.age, tt.area, tt.ptype, tt.gw,tt.lat,tt.lon,tt.is_core
;

--test
select sum(t.gw) from temp_bgy_20180805pf_sh t
where t.is_core = 'Y' and t.ptype = 1
group by t.uid;


--1250*1250,3 spot
select t.gender,t.age,t.ptype,t.is_core,t.lat,t.lon,sum(t.gw) from temp_bgy_20180805pf_sh t
where t.lon in(183,184,185,186,187,149,150,151,152,153,328,329,330,331,332,111,112,113,114,115,211,212,213,214,215,202,203,204,205,206) and t.lat in(269,270,271,272,273,49,50,51,52,53,129,130,131,132,133,97,98,99,100,101,202,203,204,205,206)
group by t.gender,t.age,t.ptype,t.is_core,t.lat,t.lon;
