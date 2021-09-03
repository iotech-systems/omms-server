
"""
CREATE TABLE streams.basic_stats_1phase (
	fk_meter_dbid int4 NOT NULL,
	reading_dts_utc timestamp NOT NULL,
	grid_freq_hz numeric(6, 2) NULL,
	voltage numeric(6, 2) NULL,
	amps numeric(6, 2) NULL,
	active_pwr numeric(8, 2) NULL,
	reactive_pwr numeric(8, 2) NULL,
	row_ins_dts_utc timestamp NOT NULL DEFAULT now()
);
"""
import datetime


class basic_stats_1phase(object):

   def __init__(self):
      self.fk_meter_dbid: int = 0
      self.reading_dts_utc: datetime.datetime
      self.grid_freq_hz: float
      self.voltage: float
      self.amps: float
      self.active_pwr: float
      self.reactive_pwr: float
      self.row_ins_dts_utc: float
