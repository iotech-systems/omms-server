
--DROP SCHEMA config;
--CREATE SCHEMA config AUTHORIZATION sbms_rest_api;

DROP TABLE IF EXISTS config.circuits;
CREATE TABLE config.circuits (
	circuit_dbid serial4 NOT NULL,
	circuit_tag varchar(32) NOT NULL,
	building_tag varchar(32) NOT NULL,
	max_amps int4 NOT NULL,
	CONSTRAINT circuit_tag_uq UNIQUE (circuit_tag, building_tag)
);

DROP TABLE IF EXISTS config.meter_alarms;
CREATE TABLE config.meter_alarms (
	fk_meter_dbid int4 NOT NULL,
	reg_name varchar(32) NOT NULL,
	reg_unit varchar(32) NOT NULL,
	reg_val numeric(8, 2) NOT NULL,
	dtc timestamp NOT NULL DEFAULT now()
);

DROP TABLE IF EXISTS config.meter_registers;
CREATE TABLE config.meter_registers (
	reg_dbid int4 NOT NULL,
	reg_name varchar(32) NOT NULL,
	CONSTRAINT meter_registers_un UNIQUE (reg_name)
);

DROP TABLE IF EXISTS config.meter_types;
CREATE TABLE config.meter_types (
	meter_type_dbid int4 NOT NULL,
	meter_type_name varchar(32) NOT NULL,
	meter_type_descr varchar(128) NULL
);

DROP TABLE IF EXISTS config.meters;
CREATE TABLE config.meters (
	meter_dbid serial4 NOT NULL,
	edge_name varchar(32) NOT NULL,
	bus_type varchar(32) NOT NULL,
	bus_address int4 NOT NULL,
	meter_type varchar(16) NOT NULL,
	meter_maker varchar(64) NOT NULL,
	meter_model varchar(64) NOT NULL,
	circuit_tag varchar(32) NULL,
	dts_created timestamp NOT NULL DEFAULT now(),
	CONSTRAINT meters_unique UNIQUE (edge_name, bus_type, bus_address)
);

DROP TABLE IF EXISTS config.org;
CREATE TABLE config.org (
	entity_dbid serial NOT NULL,
	entity_parent_dbid int4 NOT NULL DEFAULT 0,
	entity_tag varchar(32) NOT NULL,
	entity_type varchar(32) NOT NULL,
	entity_desc varchar(128) NULL,
	CONSTRAINT entity_tag_uq UNIQUE (entity_tag)
);

DROP TABLE IF EXISTS config.clients;
CREATE TABLE config.clients (
	client_dbid serial NOT NULL,
	client_tag varchar(32) NOT NULL,
	client_name varchar(64) NOT NULL
);

DROP TABLE IF EXISTS config.client_to_circuits;
CREATE TABLE config.client_to_circuits (
	client_tag varchar(32) NOT NULL,
	circuit_tag varchar(32) NOT NULL
);
