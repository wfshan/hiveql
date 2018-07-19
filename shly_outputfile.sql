#####nonptype
###tourist_persona
select a.gender, a.age, a.prov_id, cast(sum(a.gw) as bigint) as w, count(1) as n
from (select tmp.uid, tmp.gender, tmp.age, tmp.prov_id, tmp.gw from temp_wfs_shlypool20180713 tmp
) a
group by a.gender, a.age, a.prov_id;
###五省每个景区停留时长spot_dwelltime
select tmp.gender,tmp.age,cast(sum(unix_timestamp(tmp.etime)-unix_timestamp(tmp.stime)) as bigint) as dwelltime,tmp.spot,tmp.prov_id, count(1) as n
from temp_wfs_shlypool20180713 tmp
group by tmp.prov_id,tmp.spot,tmp.gender,tmp.age;
#####景区游客spot_tourist
select a.gender, a.age, a.spot,a.prov_id, cast(sum(a.gw) as bigint) as w, count(1) as n
from (select tmp.uid, tmp.spot, tmp.gender, tmp.age,tmp.prov_id, tmp.gw from temp_wfs_shlypool20180713 tmp
) a
group by a.gender, a.age,a.spot, a.prov_id;


#######ptype != 1
############tourist_persona
select a.gender, a.age, a.prov_id, cast(sum(a.gw) as bigint) as w, count(1) as n
from (select tmp.uid, tmp.gender, tmp.age, tmp.prov_id, tmp.gw from temp_wfs_shlypool20180713 tmp
where tmp.ptype != 1) a
group by a.gender, a.age, a.prov_id;

#五省每个景区停留时长spot_dwelltime
select tmp.gender,tmp.age,cast(sum(unix_timestamp(tmp.etime)-unix_timestamp(tmp.stime)) as bigint) as dwelltime,tmp.spot,tmp.prov_id,count(1) as n
from temp_wfs_shlypool20180713 tmp
where tmp.ptype != 1
group by tmp.prov_id,tmp.spot,tmp.gender,tmp.age;

#景区游客spot_tourist
select a.gender, a.age, a.spot,a.prov_id, cast(sum(a.gw) as bigint) as w, count(1) as n
from (select tmp.uid, tmp.spot, tmp.gender, tmp.age,tmp.prov_id, tmp.gw from temp_wfs_shlypool20180713 tmp
where tmp.ptype != 1) a
group by a.gender, a.age,a.spot, a.prov_id;

#########住宿热力图staynight_map
select tmp.age,tmp.gender,tmp.lon, tmp.lat, tmp.prov_id, count(1) as n, cast(sum(tmp.gw) as bigint) as w
from temp_wfs_shlypool20180713 tmp
where tmp.ptype = 1
group by tmp.age,tmp.gender,tmp.lon, tmp.lat, tmp.prov_id;


##########################################################################################3


#####################stay_fre<10  nonptype
###tourist_persona
select a.gender, a.age, a.prov_id, cast(sum(a.gw) as bigint) as w, count(1) as n
from (select tmp.uid, tmp.gender, tmp.age, tmp.prov_id, tmp.gw from temp_wfs_shlypool20180717 tmp
) a
group by a.gender, a.age, a.prov_id;
#######景区游客spot_tourist
select a.gender, a.age, a.spot,a.prov_id, cast(sum(a.gw) as bigint) as w, count(1) as n
from (select tmp.uid, tmp.spot, tmp.gender, tmp.age,tmp.prov_id, tmp.gw from temp_wfs_shlypool20180717 tmp
) a
group by a.gender, a.age,a.spot, a.prov_id;
#########五省每个景区停留时长spot_dwelltime
select tmp.gender,tmp.age,cast(sum(unix_timestamp(tmp.etime)-unix_timestamp(tmp.stime)) as bigint) as dwelltime,tmp.spot,tmp.prov_id, count(1) as n
from temp_wfs_shlypool20180717 tmp
group by tmp.prov_id,tmp.spot,tmp.gender,tmp.age;

#####################stay_fre<10  ptype != 1
###tourist_persona
select a.gender, a.age, a.prov_id, cast(sum(a.gw) as bigint) as w, count(1) as n
from (select tmp.uid, tmp.gender, tmp.age, tmp.prov_id, tmp.gw from temp_wfs_shlypool20180717 tmp
where tmp.ptype != 1) a
group by a.gender, a.age, a.prov_id;


#######景区游客spot_tourist
select a.gender, a.age, a.spot,a.prov_id, cast(sum(a.gw) as bigint) as w, count(1) as n
from (select tmp.uid, tmp.spot, tmp.gender, tmp.age,tmp.prov_id, tmp.gw from temp_wfs_shlypool20180717 tmp
where tmp.ptype != 1) a
group by a.gender, a.age,a.spot, a.prov_id;


#########五省每个景区停留时长spot_dwelltime
select tmp.gender,tmp.age,cast(sum(unix_timestamp(tmp.etime)-unix_timestamp(tmp.stime)) as bigint) as dwelltime,tmp.spot,tmp.prov_id,count(1) as n
from temp_wfs_shlypool20180717 tmp
where tmp.ptype != 1
group by tmp.prov_id,tmp.spot,tmp.gender,tmp.age;

#########住宿热力图staynight_map
select tmp.age,tmp.gender,tmp.lon, tmp.lat, tmp.prov_id, count(1) as n, cast(sum(tmp.gw) as bigint) as w
from temp_wfs_shlypool20180717 tmp
where tmp.ptype = 1
group by tmp.age,tmp.gender,tmp.lon, tmp.lat, tmp.prov_id;
