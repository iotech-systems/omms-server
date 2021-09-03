-- DROP SCHEMA streams;
CREATE SCHEMA streams AUTHORIZATION postgres;

-- Drop table
-- DROP TABLE streams.alarms;
CREATE TABLE streams.alarms (
	alarm_dbid serial NOT NULL,
	fk_meter_dbid int4 NOT NULL,
	reading_dts_utc timestamp NOT NULL,
	"level" varchar(16) NOT NULL,
	status int4 NOT NULL DEFAULT 0,
	alarm_tag varchar(32) NOT NULL,
	alarm_msg varchar(512) NOT NULL,
	row_ins_dts timestamp NOT NULL DEFAULT now()
);

-- Drop table
-- DROP TABLE streams.basic_pwr_stats;
CREATE TABLE streams.basic_pwr_stats (
	fk_meter_dbid int4 NOT NULL,
	reading_dts_utc timestamp NOT NULL,
	grid_freq_hz numeric(4, 2) NULL,
	line_volts numeric(6, 2) NULL,
	l1_volts numeric(6, 2) NULL,
	l2_volts numeric(6, 2) NULL,
	l3_volts numeric(6, 2) NULL,
	total_amps numeric(6, 2) NULL,
	l1_amps numeric(6, 2) NULL,
	l2_amps numeric(6, 2) NULL,
	l3_amps numeric(6, 2) NULL,
	total_active_pwr numeric(8, 2) NULL,
	l1_active_pwr numeric(8, 2) NULL,
	l2_active_pwr numeric(8, 2) NULL,
	l3_active_pwr numeric(8, 2) NULL,
	total_pwr_factor numeric(8, 2) NULL,
	l1_pwr_factor numeric(8, 2) NULL,
	l2_pwr_factor numeric(8, 2) NULL,
	l3_pwr_factor numeric(8, 2) NULL,
	row_ins_dts_utc timestamp NOT NULL DEFAULT now()
);

-- Drop table
-- DROP TABLE streams.kwhrs;
CREATE TABLE streams.kwhrs (
	fk_meter_dbid int4 NOT NULL,
	reading_dts_utc timestamp NOT NULL,
	total numeric(10, 2) NOT NULL,
	l1 numeric(10, 2) NULL,
	l2 numeric(10, 2) NULL,
	l3 numeric(10, 2) NULL,
	row_ins_dts timestamp NOT NULL DEFAULT now()
);
