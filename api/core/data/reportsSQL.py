
class reportsSQL(object):

   @staticmethod
   def meter_kwhrs(startDate: str, endDate: str, meterDBID: str):
      # drop table vars;
      return f"""drop table if exists vars;
         create temp table vars (vname varchar(16) not null unique, kwhrs float);
         insert into vars values ('s_kwhrs', 0.0), ('e_kwhrs', 0.0);
         -- set start kwhrs --
         update vars set kwhrs = (select k.total_kwhrs from streams.kwhrs k 
            where k.reading_dts_utc > cast('{startDate} 00:00:01' as timestamp) 
               and k.reading_dts_utc < cast('{endDate} 23:59:59' as timestamp)
               and k.fk_meter_dbid in ({meterDBID}) order by k.reading_dts_utc asc limit 1) 
            where vname = 's_kwhrs';
         -- set end kwhrs --
         update vars set kwhrs = (select k.total_kwhrs from streams.kwhrs k 
            where k.reading_dts_utc > cast('{startDate} 00:00:01' as timestamp) 
               and k.reading_dts_utc < cast('{endDate} 23:59:59' as timestamp)
               and k.fk_meter_dbid in ({meterDBID}) order by k.reading_dts_utc desc limit 1) 
            where vname = 'e_kwhrs';
         -- select row as json --
         select row_to_json(t) from (select {meterDBID} mdbid,
            (select m.circuit_tag from config.meters m where m.meter_dbid = {meterDBID}) ctag,
            '{startDate}' sdts, '{endDate}' edts, ((select kwhrs from vars where vname = 'e_kwhrs')
               - (select kwhrs from vars where vname = 's_kwhrs')) as kwhrs) t;"""

   @staticmethod
   def client_kwhrs(sDate: str, eDate: str, cltDBID: int):
      pass
