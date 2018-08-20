create table temp_lc_201808142_jn as
select
sp2.date, sp2.ptype, sp2.city,
floor((sp2.weighted_centroid_lat - m.slat)/m.mlat) as lat,
floor((sp2.weighted_centroid_lon - m.slon)/m.mlon) as lon,
sp2.is_core, sp2.gender, sp2.age,
cast(sum(sp2.gw) as bigint) as n,
cast(row_number() over(partition by 1) / 100000 as int) + 1 as slides
from (
select city_code, min(ext_min_x) as slon, min(ext_min_y) as slat,
avg(ext_max_x-ext_min_x) as mlon, avg(ext_max_y-ext_min_y) as mlat
from ss_grid_wgs84
where city_code = 'V0370100'
group by city_code
) m inner join (
select sp.uid, sp.date, sp.ptype, sp.city, sp.weighted_centroid_lat, sp.weighted_centroid_lon, u.gw,
case when u.gender='01' then 'M'
  when u.gender='02' then 'F' end as gender,
case when u.age = '01' then '0-6'
when u.age = '02' then '7-12'
when u.age = '03' then '13-15'
when u.age = '04' then '16-18'
when u.age = '05' then '19-24'
when u.age = '06' then '25-29'
when u.age = '07' then '30-34'
when u.age = '08' then '35-39'
when u.age = '09' then '40-44'
when u.age = '10' then '45-49'
when u.age = '11' then '50-54'
when u.age = '12' then '55-59'
when u.age = '13' then '60-64'
when u.age = '14' then '65-69'
when u.age = '15' then '70+'
end as age,
case when u.area = sp.city then "L" else "N" end as local,
case when u.area = sp.city then u.weight else 1 end as weight,sp.is_core
from stay_poi sp inner join user_attribute u
on sp.uid = u.uid and sp.city = u.city and sp.date = u.date
where sp.city = 'V0370100' and u.city = 'V0370100' and sp.date = 20180401
) sp2
on m.city_code = sp2.city
group by sp2.date, sp2.ptype, sp2.city, sp2.is_core, sp2.gender, sp2.age,
floor((sp2.weighted_centroid_lat - m.slat)/m.mlat),
floor((sp2.weighted_centroid_lon - m.slon)/m.mlon)
;

--------------------------

select cast(sum(x.gw) as bigint) as n, x.ptype, x.age, x.is_core
from
(select a.uid, sum(a.ptype) as ptype, a.is_core,
case when u.age = '01' then 'F'
when u.age = '02' then 'F'
when u.age = '03' then 'F'
when u.age = '04' then 'F'
when u.age = '05' then 'F'
when u.age = '06' then 'T'
when u.age = '07' then 'T'
when u.age = '08' then 'T'
when u.age = '09' then 'T'
when u.age = '10' then 'T'
when u.age = '11' then 'T'
when u.age = '12' then 'F'
when u.age = '13' then 'F'
when u.age = '14' then 'F'
when u.age = '15' then 'F'
end as age,
u.gw
from stay_poi a
inner join user_attribute u
on a.uid = u.uid
where a.ptype in (1,2) and a.city = 'V0370100' and u.city = 'V0370100' and a.date = 20180401 and u.date=20180401
group by a.uid, a.is_core,
case when u.age = '01' then 'F'
when u.age = '02' then 'F'
when u.age = '03' then 'F'
when u.age = '04' then 'F'
when u.age = '05' then 'F'
when u.age = '06' then 'T'
when u.age = '07' then 'T'
when u.age = '08' then 'T'
when u.age = '09' then 'T'
when u.age = '10' then 'T'
when u.age = '11' then 'T'
when u.age = '12' then 'F'
when u.age = '13' then 'F'
when u.age = '14' then 'F'
when u.age = '15' then 'F'
end, u.gw) x
group by x.age, x.is_core, x.ptype
;


--------------------
create table temp_lc_201808142_jn_ptype1 as
select
sp2.date, sp2.ptype, sp2.city,
floor((sp2.weighted_centroid_lat - m.slat)/m.mlat) as lat,
floor((sp2.weighted_centroid_lon - m.slon)/m.mlon) as lon,
sp2.is_core, sp2.gender, sp2.age,
cast(sum(sp2.gw) as bigint) as n,
cast(row_number() over(partition by 1) / 100000 as int) + 1 as slides
from (
select city_code, min(ext_min_x) as slon, min(ext_min_y) as slat,
avg(ext_max_x-ext_min_x) as mlon, avg(ext_max_y-ext_min_y) as mlat
from ss_grid_wgs84
where city_code = 'V0370100'
group by city_code
) m inner join
(
select sp.uid, sp.date, sp.ptype, sp.city, sp.weighted_centroid_lat, sp.weighted_centroid_lon, u.gw,sp.is_core,
case when u.gender='01' then 'M'
  when u.gender='02' then 'F' end as gender,
case when u.age = '01' then '0-6'
when u.age = '02' then '7-12'
when u.age = '03' then '13-15'
when u.age = '04' then '16-18'
when u.age = '05' then '19-24'
when u.age = '06' then '25-29'
when u.age = '07' then '30-34'
when u.age = '08' then '35-39'
when u.age = '09' then '40-44'
when u.age = '10' then '45-49'
when u.age = '11' then '50-54'
when u.age = '12' then '55-59'
when u.age = '13' then '60-64'
when u.age = '14' then '65-69'
when u.age = '15' then '70+'
end as age,
case when u.area = sp.city then "L" else "N" end as local,
case when u.area = sp.city then u.weight else 1 end as weight
from stay_poi sp inner join user_attribute u
on sp.uid = u.uid and sp.city = u.city and sp.date = u.date
where sp.city = 'V0370100' and u.city = 'V0370100' and sp.date = 20180401 and sp.is_core = 'Y'
) sp2
on m.city_code = sp2.city
inner join
(select distinct x.uid from
(select a.uid, sum(a.ptype) as ptype, a.is_core,
case when u.age = '01' then 'F'
when u.age = '02' then 'F'
when u.age = '03' then 'F'
when u.age = '04' then 'F'
when u.age = '05' then 'F'
when u.age = '06' then 'T'
when u.age = '07' then 'T'
when u.age = '08' then 'T'
when u.age = '09' then 'T'
when u.age = '10' then 'T'
when u.age = '11' then 'T'
when u.age = '12' then 'F'
when u.age = '13' then 'F'
when u.age = '14' then 'F'
when u.age = '15' then 'F'
end as age,
u.gw
from stay_poi a
inner join user_attribute u
on a.uid = u.uid
where a.ptype in (1,2) and a.city = 'V0370100' and u.city = 'V0370100' and a.date = 20180401 and u.date=20180401
group by a.uid, a.is_core,
case when u.age = '01' then 'F'
when u.age = '02' then 'F'
when u.age = '03' then 'F'
when u.age = '04' then 'F'
when u.age = '05' then 'F'
when u.age = '06' then 'T'
when u.age = '07' then 'T'
when u.age = '08' then 'T'
when u.age = '09' then 'T'
when u.age = '10' then 'T'
when u.age = '11' then 'T'
when u.age = '12' then 'F'
when u.age = '13' then 'F'
when u.age = '14' then 'F'
when u.age = '15' then 'F'
end, u.gw
) x
where x.ptype = 1 and x.age = 'T' and x.is_core = 'Y'
) xx
on sp2.uid = xx.uid
group by sp2.date, sp2.ptype, sp2.city, sp2.is_core, sp2.gender, sp2.age,
floor((sp2.weighted_centroid_lat - m.slat)/m.mlat),
floor((sp2.weighted_centroid_lon - m.slon)/m.mlon)
;




select t.ptype,t.lat,t.lon,t.is_core,t.gender,t.age,t.n from temp_lc_201808142_jn t  where slides =1;
