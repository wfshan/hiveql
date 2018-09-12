create table temp_wfs_beijing_grid_count2 as
select f.age,f.gender,f.brand,f.type,f.ptype,f.lon,f.lat,sum(f.gw) as gw,cast(row_number() over(partition by 1) / 100000 as int)+1 as slides from
(
select case when ua.gender='01' then 'M'
  when ua.gender='02' then 'F' end as gender,
case when ua.age = '01' then '000-6'
when ua.age = '02' then '007-12'
when ua.age = '03' then '13-15'
when ua.age = '04' then '16-18'
when ua.age = '05' then '19-24'
when ua.age = '06' then '25-29'
when ua.age = '07' then '30-34'
when ua.age = '08' then '35-39'
when ua.age = '09' then '40-44'
when ua.age = '10' then '45-49'
when ua.age = '11' then '50-54'
when ua.age = '12' then '55-59'
when ua.age = '13' then '60-64'
when ua.age = '14' then '65-69'
when ua.age = '15' then '70+'
end as age,ua.brand,ua.type,sp.ptype,ua.gw,
floor((sp.weighted_centroid_lat - 39.44275803)/0.002253563) as lat,
floor((sp.weighted_centroid_lon - 115.423411)/0.002928871) as lon
from
(
select u.uid,u.age,u.gender,u.brand,u.type,u.gw from
user_attribute u
where u.city = 'V0110000' and u.date = 20180501
group by u.uid,u.age,u.gender,u.brand,u.type,u.gw
) ua
inner join stay_poi sp
on sp.uid = ua.uid
where sp.city = 'V0110000' and sp.date = 20180501 and sp.ptype in (1,2) and sp.is_core = 'Y'
)f
group by f.age,f.gender,f.brand,f.type,f.ptype,f.lon,f.lat
;
##############################################
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
where a.ptype in (1,2) and a.city = 'V0110000' and u.city = 'V0110000' and a.date = 20180501 and u.date=20180501
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

#########################################

--用以回填
create table temp_wfs_beijing_grid_count3 as
select f.age,f.gender,f.brand,f.type,f.ptype,f.lon,f.lat,sum(f.gw) as gw,cast(row_number() over(partition by 1) / 100000 as int)+1 as slides from
(
select ua.uid,case when ua.gender='01' then 'M'
  when ua.gender='02' then 'F' end as gender,
case when ua.age = '01' then '000-6'
when ua.age = '02' then '007-12'
when ua.age = '03' then '13-15'
when ua.age = '04' then '16-18'
when ua.age = '05' then '19-24'
when ua.age = '06' then '25-29'
when ua.age = '07' then '30-34'
when ua.age = '08' then '35-39'
when ua.age = '09' then '40-44'
when ua.age = '10' then '45-49'
when ua.age = '11' then '50-54'
when ua.age = '12' then '55-59'
when ua.age = '13' then '60-64'
when ua.age = '14' then '65-69'
when ua.age = '15' then '70+'
end as age,ua.brand,ua.type,sp.ptype,ua.gw,
floor((sp.weighted_centroid_lat - 39.44275803)/0.002253563) as lat,
floor((sp.weighted_centroid_lon - 115.423411)/0.002928871) as lon
from
(
select u.uid,u.age,u.gender,u.brand,u.type,u.gw from
user_attribute u
where u.city = 'V0110000' and u.date = 20180501
group by u.uid,u.age,u.gender,u.brand,u.type,u.gw
) ua
inner join stay_poi sp
on sp.uid = ua.uid
where sp.city = 'V0110000' and sp.date = 20180501 and sp.ptype in (1,2) and sp.is_core = 'Y'
)f
inner join
(select x.uid from
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
where a.ptype in (1,2) and a.city = 'V0110000' and u.city = 'V0110000' and a.date = 20180501 and u.date=20180501
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
group by x.uid
) xx
on f.uid = xx.uid
group by f.age,f.gender,f.brand,f.type,f.ptype,f.lon,f.lat
;
