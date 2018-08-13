
----------------
create table temp_wfs_uidfil as
select distinct spppp.uid from
(select sppp.uid,max(sppp.dt) as dtt from
(select spp.uid,spp.date,sum(spp.dwelltime) as dt from
 (select sp.uid,sp.date,
case when hour(sp.stime) < 7 and hour(sp.etime) between 7 and 22 then cast(unix_timestamp(sp.etime)-unix_timestamp(concat_ws(' ',to_date(sp.etime),'07:00:00')) as bigint)
when hour(sp.stime) between 7 and 22 and hour(sp.etime) between 7 and 22 then cast(unix_timestamp(sp.etime)-unix_timestamp(sp.stime) as bigint)
when hour(sp.stime) between 7 and 10 and hour(sp.etime) > 22 then cast(unix_timestamp(concat_ws(' ',to_date(sp.etime),'22:00:00'))-unix_timestamp(sp.stime) as bigint) else 0 end as dwelltime
from stay_month sp
where from_unixtime(unix_timestamp(sp.stime),'yyyyMM') = 201710 and sp.city = 'V0310000' and sp.is_core = 'N'
) spp
group by spp.uid,spp.date
)sppp
group by sppp.uid,sppp.date
) spppp
where spppp.dtt > 10800;

--------------------
create table temp_wfs_dsn_uidsm as
select a.uid,a.date, a.area,b.area_desc, b.prov_id, a.grid_id, a.ptype, a.stime, a.etime, a.gw,a.arpu,a.brand,a.type,
case when a.gender='01' then 'M'
when a.gender = '02' then 'F'
end as gender,
case when a.age in ('01','02') then '0-12'
when a.age in ('03','04') then '13-18'
when a.age in ('05','06') then '19-29'
when a.age in ('07','08') then '30-39'
when a.age in ('09','10') then '40-49'
when a.age in ('11','12') then '50-59'
when a.age in ('13','14') then '60-69'
when a.age = '15' then '70+' end as age
from area_code b
inner join
(select sm.uid,sm.date,sm.city, ua.area, sm.grid_id, ua.gender, ua.age,ua.arpu,ua.brand,ua.type, sm.ptype, sm.stime, sm.etime, ua.gw
from stay_month sm
inner join temp_wfs_uidfil ssm
on ssm.uid = sm.uid
inner join
(select us.uid,us.date,us.area,us.gender, us.age,us.arpu,us.brand,us.type,us.gw,us.city from user_attribute us ) ua
on ssm.uid = ua.uid
where from_unixtime(unix_timestamp(sm.stime),'yyyyMM') = 201710 and sm.city = 'V0310000' and ua.date = 20171001 and ua.city = 'V0310000'
) a
on a.area = b.area_id
;

------------------------------------
create table temp_wfs_dsn_spsm
select distinct  t.area
    from
     (select x.uid,x.date, x.age, x.gender, x.area,x.area_desc,x.prov_id, x.grid_id, x.ptype, x.gw,x.arpu,x.brand,x.type,u.lcode,u.ltime,s.weighted_centroid_lon as lon, s.weighted_centroid_lat as lat
    from temp_wfs_dsn_uidsm x
    inner join stay_poi s
    on x.uid = s.uid and x.grid_id = s.final_grid_id
    inner join
        (select ul.uid,ul.lcode,ul.ltime from user_label_info ul
        where ul.date = 20171001) u
    on s.uid = u.uid
    ) t
;

-----------------------------------


create table temp_wfs_dsn08105 as
select f.uid,f.date,f.gender,f.age,f.area,f.area_desc, f.prov_id, f.grid_id, f.ptype, f.gw,f.lon,f.lat,f.arpu,f.brand,f.type,f.lcode,f.ltime,case
when f.lon = 298 and f.lat = 210 then 'dishini'
when f.lon = 308 and f.lat = 212 then 'dishini'
when f.lon = 311 and f.lat = 204 then 'dishini'
when f.lon = 300 and f.lat = 200 then 'dishini'
when f.lon = 298 and f.lat = 210 then 'dishini'
when f.lon = 299 and f.lat = 206 then 'dishini'
when f.lon = 299 and f.lat = 207 then 'dishini'
when f.lon = 299 and f.lat = 208 then 'dishini'
when f.lon = 299 and f.lat = 209 then 'dishini'
when f.lon = 299 and f.lat = 210 then 'dishini'
when f.lon = 300 and f.lat = 201 then 'dishini'
when f.lon = 300 and f.lat = 202 then 'dishini'
when f.lon = 300 and f.lat = 203 then 'dishini'
when f.lon = 300 and f.lat = 204 then 'dishini'
when f.lon = 300 and f.lat = 205 then 'dishini'
when f.lon = 300 and f.lat = 206 then 'dishini'
when f.lon = 300 and f.lat = 207 then 'dishini'
when f.lon = 300 and f.lat = 208 then 'dishini'
when f.lon = 300 and f.lat = 209 then 'dishini'
when f.lon = 300 and f.lat = 210 then 'dishini'
when f.lon = 301 and f.lat = 201 then 'dishini'
when f.lon = 301 and f.lat = 202 then 'dishini'
when f.lon = 301 and f.lat = 203 then 'dishini'
when f.lon = 301 and f.lat = 204 then 'dishini'
when f.lon = 301 and f.lat = 205 then 'dishini'
when f.lon = 301 and f.lat = 206 then 'dishini'
when f.lon = 301 and f.lat = 207 then 'dishini'
when f.lon = 301 and f.lat = 208 then 'dishini'
when f.lon = 301 and f.lat = 209 then 'dishini'
when f.lon = 301 and f.lat = 210 then 'dishini'
when f.lon = 302 and f.lat = 201 then 'dishini'
when f.lon = 302 and f.lat = 202 then 'dishini'
when f.lon = 302 and f.lat = 203 then 'dishini'
when f.lon = 302 and f.lat = 204 then 'dishini'
when f.lon = 302 and f.lat = 205 then 'dishini'
when f.lon = 302 and f.lat = 206 then 'dishini'
when f.lon = 302 and f.lat = 207 then 'dishini'
when f.lon = 302 and f.lat = 208 then 'dishini'
when f.lon = 302 and f.lat = 209 then 'dishini'
when f.lon = 302 and f.lat = 210 then 'dishini'
when f.lon = 303 and f.lat = 202 then 'dishini'
when f.lon = 303 and f.lat = 203 then 'dishini'
when f.lon = 303 and f.lat = 204 then 'dishini'
when f.lon = 303 and f.lat = 205 then 'dishini'
when f.lon = 303 and f.lat = 206 then 'dishini'
when f.lon = 303 and f.lat = 207 then 'dishini'
when f.lon = 303 and f.lat = 208 then 'dishini'
when f.lon = 303 and f.lat = 209 then 'dishini'
when f.lon = 303 and f.lat = 210 then 'dishini'
when f.lon = 304 and f.lat = 202 then 'dishini'
when f.lon = 304 and f.lat = 203 then 'dishini'
when f.lon = 304 and f.lat = 204 then 'dishini'
when f.lon = 304 and f.lat = 205 then 'dishini'
when f.lon = 304 and f.lat = 206 then 'dishini'
when f.lon = 304 and f.lat = 207 then 'dishini'
when f.lon = 304 and f.lat = 208 then 'dishini'
when f.lon = 304 and f.lat = 209 then 'dishini'
when f.lon = 304 and f.lat = 210 then 'dishini'
when f.lon = 304 and f.lat = 211 then 'dishini'
when f.lon = 305 and f.lat = 202 then 'dishini'
when f.lon = 305 and f.lat = 203 then 'dishini'
when f.lon = 305 and f.lat = 204 then 'dishini'
when f.lon = 305 and f.lat = 205 then 'dishini'
when f.lon = 305 and f.lat = 206 then 'dishini'
when f.lon = 305 and f.lat = 207 then 'dishini'
when f.lon = 305 and f.lat = 208 then 'dishini'
when f.lon = 305 and f.lat = 209 then 'dishini'
when f.lon = 305 and f.lat = 210 then 'dishini'
when f.lon = 305 and f.lat = 211 then 'dishini'
when f.lon = 306 and f.lat = 203 then 'dishini'
when f.lon = 306 and f.lat = 204 then 'dishini'
when f.lon = 306 and f.lat = 205 then 'dishini'
when f.lon = 306 and f.lat = 206 then 'dishini'
when f.lon = 306 and f.lat = 207 then 'dishini'
when f.lon = 306 and f.lat = 208 then 'dishini'
when f.lon = 306 and f.lat = 209 then 'dishini'
when f.lon = 306 and f.lat = 210 then 'dishini'
when f.lon = 306 and f.lat = 211 then 'dishini'
when f.lon = 307 and f.lat = 203 then 'dishini'
when f.lon = 307 and f.lat = 204 then 'dishini'
when f.lon = 307 and f.lat = 205 then 'dishini'
when f.lon = 307 and f.lat = 206 then 'dishini'
when f.lon = 307 and f.lat = 207 then 'dishini'
when f.lon = 307 and f.lat = 208 then 'dishini'
when f.lon = 307 and f.lat = 209 then 'dishini'
when f.lon = 307 and f.lat = 210 then 'dishini'
when f.lon = 307 and f.lat = 211 then 'dishini'
when f.lon = 308 and f.lat = 203 then 'dishini'
when f.lon = 308 and f.lat = 204 then 'dishini'
when f.lon = 308 and f.lat = 205 then 'dishini'
when f.lon = 308 and f.lat = 206 then 'dishini'
when f.lon = 308 and f.lat = 207 then 'dishini'
when f.lon = 308 and f.lat = 208 then 'dishini'
when f.lon = 308 and f.lat = 209 then 'dishini'
when f.lon = 308 and f.lat = 210 then 'dishini'
when f.lon = 308 and f.lat = 211 then 'dishini'
when f.lon = 309 and f.lat = 204 then 'dishini'
when f.lon = 309 and f.lat = 205 then 'dishini'
when f.lon = 309 and f.lat = 206 then 'dishini'
when f.lon = 309 and f.lat = 207 then 'dishini'
when f.lon = 309 and f.lat = 208 then 'dishini'
when f.lon = 309 and f.lat = 209 then 'dishini'
when f.lon = 310 and f.lat = 204 then 'dishini'
when f.lon = 310 and f.lat = 205 then 'dishini'
when f.lon = 310 and f.lat = 206 then 'dishini'
end as spot
from
(
select t.uid,t.date, t.gender, t.age, t.area,t.area_desc, t.prov_id, t.grid_id, t.ptype, t.gw,t.arpu,t.brand,t.type,t.lcode,t.ltime,
floor((t.lat - 30.67559298)/0.0022544689779550493) as lat,
floor((t.lon - 120.85680492)/0.002653328470790916) as lon
from
(select x.uid,x.date, x.age, x.gender, x.area,x.area_desc,x.prov_id, x.grid_id, x.ptype, x.gw,x.arpu,x.brand,x.type,u.lcode,u.ltime,s.weighted_centroid_lon as lon, s.weighted_centroid_lat as lat
from temp_wfs_dsn_uidsm x
inner join stay_poi s
on x.uid = s.uid and x.grid_id = s.final_grid_id
inner join
user_label_info u
on s.uid = u.uid
) t
) f
;

-----------------------

#人数
select  tt.date,tt.age,tt.gender,tt.area_desc,sum(tt.gw) as gw from
(select t.uid,t.date,t.age,t.gender,t.area_desc,t.gw from temp_wfs_dsn08105 t
where t.spot = 'dishini'
group by t.date,t.uid,t.gender,t.age,t.area_desc,t.gw) tt
group by tt.date,tt.age,tt.gender,tt.area_desc;

#花费
select  tt.age,tt.gender,tt.area_desc,avg(tt.arpu) as arpu from
(select t.uid,t.age,t.gender,t.area_desc,t.arpu from temp_wfs_dsn08105 t
where t.spot = 'dishini'
group by t.uid,t.gender,t.age,t.area_desc,t.arpu) tt
group by tt.age,tt.gender,tt.area_desc;

#手机品牌
select tt.date,tt.age,tt.gender,tt.area_desc,tt.brand, sum(tt.gw) as count from
(select t.uid,t.date,t.age,t.gender,t.area_desc,t.brand,t.gw from temp_wfs_dsn08105 t
where t.spot = 'dishini'
group by t.uid,t.date,t.gender,t.age,t.area_desc,t.brand,t.gw) tt
group by  tt.date,tt.age,tt.gender,tt.brand,tt.area_desc;


#浏览偏好
create table temp_wfs_dsn_pref2 as
select tt.date,tt.age,tt.gender,tt.area_desc,tt.lcode,sum(tt.gw) as sumgw,sum(tt.ltime) as sumltime,cast(row_number() over(partition by 1) / 100000 as int) + 1 as slides from
(select t.age,t.date,t.gender,t.area_desc,t.gw,t.lcode,t.ltime from temp_wfs_dsn08105 t
where t.spot = 'dishini'
group by t.date,t.uid,t.gender,t.age,t.area_desc,t.gw,t.lcode,t.ltime) tt
group by tt.date,tt.gender,tt.age,tt.area_desc,tt.lcode;
