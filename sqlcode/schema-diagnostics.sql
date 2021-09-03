

-- Drop table
-- DROP TABLE "diagnostics".edge_pings;
CREATE TABLE "diagnostics".edge_pings (
	ip varchar(32) NOT NULL,
	hostname varchar(32) NOT NULL,
	dts_utc timestamp NOT NULL DEFAULT now()
);
