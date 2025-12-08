CREATE TABLE addresses(blockid TEXT NOT NULL PRIMARY KEY, plz INTEGER, place TEXT, street TEXT, street_number TEXT, federalstate TEXT);

CREATE TABLE blocks(blockid TEXT NOT NULL PRIMARY KEY, plantid TEXT, blockname TEXT, federalstate TEXT, energysource TEXT, initialop INTEGER, chp TEXT, netpower REAL, state TEXT, endop INT, company TEXT, FOREIGN KEY (blockid) REFERENCES addresses(blockid) ON DELETE CASCADE);

CREATE TABLE power(powerid INTEGER NOT NULL PRIMARY KEY, producedat TIMESTAMP NOT NULL, blockid TEXT NOT NULL, power BIGINT NOT NULL, FOREIGN KEY (blockid) REFERENCES blocks(blockid) ON DELETE CASCADE);

CREATE TABLE plants(plantid TEXT NOT NULL PRIMARY KEY, plantname TEXT, federalstate TEXT, energysource TEXT, chp TEXT, latestexpanded INT, initialop INT, totalpower REAL, state TEXT, blockcount INT,  company TEXT, plz TEXT, place TEXT, street TEXT, number TEXT, latitude REAL, longitude REAL, activepower REAL, energy_2015 BIGINT,  energy_2016 BIGINT,  energy_2017 BIGINT,  energy_2018 BIGINT,  energy_2019 BIGINT, energy_2020 BIGINT, energy_2021 BIGINT, energy_2022 BIGINT, energy_2023 BIGINT, energy_2024 BIGINT, co2_2007 BIGINT,  co2_2008 BIGINT,  co2_2009 BIGINT,  co2_2010 BIGINT,  co2_2011 BIGINT,  co2_2012 BIGINT,  co2_2013 BIGINT,  co2_2014 BIGINT,  co2_2015 BIGINT,  co2_2016 BIGINT,  co2_2017 BIGINT,  co2_2018 BIGINT, co2_2019 BIGINT, co2_2020 BIGINT, co2_2021 BIGINT, co2_2022 BIGINT, co2_2023 BIGINT, revenue REAL, profit REAL);

CREATE TABLE pollutions(pollutionsid INTEGER NOT NULL, year INTEGER, plantid  TEXT NOT NULL, pollutant TEXT NOT NULL, releasesto TEXT NOT NULL, amount REAL, potency INTEGER NOT NULL, unit2 TEXT NOT NULL, amount2 REAL, pollutant2 TEXT, PRIMARY KEY(plantid, releasesto, pollutant, year), FOREIGN KEY (plantid) REFERENCES plants(plantid) ON DELETE CASCADE);

CREATE TABLE yearly(yid INTEGER NOT NULL PRIMARY KEY, year INTEGER NOT NULL, plantid TEXT NOT NULL, power BIGINT NOT NULL, FOREIGN KEY (plantid) REFERENCES plants(plantid) ON DELETE CASCADE);

CREATE TABLE month(monthid INTEGER NOT NULL PRIMARY KEY, year INT, month INT, blockid TEXT NOT NULL, power BIGINT NOT NULL, FOREIGN KEY (blockid) REFERENCES blocks(blockid) ON DELETE CASCADE);

CREATE TABLE test(tid INTEGER, name TEXT, value REAL, value2 INT, value3 INT, value4 INT, value5 INT, value6 INT, value7 INT, value8 INT );

COPY addresses
FROM '/docker-entrypoint-initdb.d/stammdaten_nh_new.csv'
WITH (FORMAT CSV, DELIMITER ',', NULL '');

COPY plants
FROM '/docker-entrypoint-initdb.d/plants_with_profit.csv'
WITH (FORMAT CSV, DELIMITER ',', NULL '');

COPY blocks
FROM '/docker-entrypoint-initdb.d/blocks_new_nh.csv'
WITH (FORMAT CSV, DELIMITER ',', NULL '');

COPY yearly
FROM '/docker-entrypoint-initdb.d/yearly_pg.csv'
WITH (FORMAT CSV, DELIMITER ',', NULL '');

COPY pollutions
FROM '/docker-entrypoint-initdb.d/pollutants_pg.csv'
WITH (FORMAT CSV, DELIMITER ',', NULL '');

COPY month
FROM '/docker-entrypoint-initdb.d/ml2.csv'
WITH (FORMAT CSV, DELIMITER ',', NULL '');

UPDATE plants SET chp = 'Nein' WHERE chp IS NULL;
CREATE UNIQUE INDEX plants_idx ON plants(plantid);
CREATE INDEX blocks_idx ON blocks(blockid, plantid);

/*
psql plantwatch -c "\copy addresses FROM 'stammdaten_nh_new.csv' WITH (FORMAT CSV)"
psql plantwatch -c "\copy plants FROM 'plants_with_profit.csv' WITH (FORMAT CSV)"
psql plantwatch -c "\copy blocks FROM 'blocks_new_nh.csv' WITH (FORMAT CSV)"
psql plantwatch -c "\copy yearly FROM 'yearly_pg.csv' WITH (FORMAT CSV)"
psql plantwatch -c "\copy pollutions FROM 'pollutants_pg.csv' WITH (FORMAT CSV)"
psql plantwatch -c "\copy month FROM 'ml2.csv' WITH (FORMAT CSV)"
*/
