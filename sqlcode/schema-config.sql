
-- DROP SCHEMA config;
CREATE SCHEMA config AUTHORIZATION sbms_admin;

-- Drop table
-- DROP TABLE config.meter_alarms;
CREATE TABLE config.meter_alarms (
	fk_meter_dbid int4 NOT NULL,
	reg_name varchar(32) NOT NULL,
	reg_unit varchar(32) NOT NULL,
	reg_val numeric(8, 2) NOT NULL,
	dtc timestamp NOT NULL DEFAULT now()
);

-- Drop table
-- DROP TABLE config.meter_registers;
CREATE TABLE config.meter_registers (
	reg_dbid int4 NOT NULL,
	reg_name varchar(32) NOT NULL,
	CONSTRAINT meter_registers_un UNIQUE (reg_name)
);

-- Drop table
-- DROP TABLE config.meter_types;
CREATE TABLE config.meter_types (
	meter_type_dbid int4 NOT NULL,
	meter_type_name varchar(32) NOT NULL,
	meter_type_descr varchar(128) NULL
);

-- Drop table
-- DROP TABLE config.meters;
CREATE TABLE config.meters (
	meter_dbid serial NOT NULL,
	edge_name varchar(32) NOT NULL,
	bus_type varchar(32) NOT NULL,
	bus_address int4 NOT NULL,
	meter_type varchar(16) NOT NULL,
	meter_maker varchar(64) NOT NULL,
	meter_model varchar(64) NOT NULL,
	meter_buffer varchar(255) NULL,
	dts_created timestamp NOT NULL DEFAULT now(),
	CONSTRAINT meters_unique UNIQUE (edge_name, bus_type, bus_address)
);
