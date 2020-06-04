DROP IF EXISTS blocks;

create type energy_t as enum('nuclear', 'hardcoal', 'lignite', 'gas', 'oil');

CREATE TABLE plants(
id TEXT PRIMARY KEY,
name TEXT,
federal_state_text TEXT,
energy_source TEXT,
chp_text TEXT,
latestexpanded INT,
 initialop INT,
 totalpower REAL,
 state_text TEXT,
 blockcount INT, -- generated column
company TEXT,
 plz TEXT,
 place TEXT,
 street TEXT,
 number TEXT,
 latitude REAL,
 longitude REAL,
 )
 
-- active blocks generated
-- federal_state enum
-- chp boolean
-- stat state_t
--fuel_type energy_t,

CREATE TABLE blocks(
id TEXT PRIMARY KEY,
plant_id TEXT,
description TEXT,
energy_source TEXT,
chp_text TEXT,
name TEXT,
netpower REAL,
state_text TEXT,
endop TEXT,
company TEXT,
FOREIGN KEY (plant_id) REFERENCES plants (id)
)




sqlite3 plantwatch.db  "CREATE TABLE blocks(plantid TEXT,
blockid TEXT NOT NULL PRIMARY KEY,
blockdescription TEXT,
 
energysource TEXT,
initialop INTEGER,
chp TEXT,
blockname TEXT,
netpower REAL,
state TEXT,
endop TEXT,
company TEXT,
FOREIGN KEY (blockid) REFERENCES addresses(blockid) ON DELETE CASCADE);"



#!/bin/bash
if [ -f plantwatch.db ]; then
   rm plantwatch.db
fi
sqlite3 plantwatch.db  "CREATE TABLE addresses(blockid TEXT NOT NULL PRIMARY KEY, federalstate TEXT, place TEXT, plz INTEGER, street TEXT);"

sqlite3 plantwatch.db  "CREATE TABLE blocks(plantid TEXT, blockid TEXT NOT NULL PRIMARY KEY, blockdescription TEXT, federalstate TEXT, energysource TEXT, initialop INTEGER, chp TEXT, blockname TEXT, netpower REAL, state TEXT, endop TEXT, company TEXT, FOREIGN KEY (blockid) REFERENCES addresses(blockid) ON DELETE CASCADE);"

sqlite3 plantwatch.db  "CREATE TABLE plants(plantid TEXT NOT NULL PRIMARY KEY, plantname TEXT, federalstate TEXT, energysource TEXT, chp TEXT, latestexpanded INT, initialop INT, totalpower REAL, state TEXT, blockcount INT,  company TEXT, plz TEXT, place TEXT, street TEXT, number TEXT, latitude REAL, longitude REAL, FOREIGN KEY (plantid) REFERENCES blocks(plantid) ON DELETE CASCADE);"

sqlite3 plantwatch.db "CREATE TABLE power(powerid INTEGER NOT NULL PRIMARY KEY, producedat TIMESTAMP NOT NULL, blockid TEXT NOT NULL, power INTEGER NOT NULL, FOREIGN KEY (blockid) REFERENCES blocks(blockid) ON DELETE CASCADE);"

sqlite3 plantwatch.db "CREATE TABLE month(monthid INTEGER NOT NULL PRIMARY KEY, year INT, month INT, blockid TEXT NOT NULL, power INTEGER NOT NULL, FOREIGN KEY (blockid) REFERENCES blocks(blockid) ON DELETE CASCADE);"

sqlite3 plantwatch.db "CREATE TABLE monthp(monthpid INTEGER NOT NULL PRIMARY KEY, year INT, month INT, plantid TEXT NOT NULL, power INTEGER NOT NULL, FOREIGN KEY (plantid) REFERENCES plants(plantid) ON DELETE CASCADE);"

sqlite3 plantwatch.db "CREATE TABLE yearly(yid INTEGER NOT NULL PRIMARY KEY, year INTEGER NOT NULL, plantid TEXT NOT NULL, power INTEGER NOT NULL, FOREIGN KEY (plantid) REFERENCES plants(plantid) ON DELETE CASCADE);"

sqlite3 plantwatch.db "CREATE TABLE mtp(mtpid INTEGER NOT NULL PRIMARY KEY, plantid TEXT NOT NULL, power INTEGER NOT NULL, producedat TIM̀ESTAMP NOT NULL, FOREIGN KEY (plantid) REFERENCES plants(plantid) ON DELETE CASCADE);"

sqlite3 plantwatch.db  "CREATE TABLE pollutions(pollutionsid INTEGER NOT NULL, year INTEGER, plantid  TEXT NOT NULL, pollutant TEXT NOT NULL, releasesto TEXT NOT NULL, amount REAL, potency INTEGER NOT NULL, unit2 TEXT NOT NULL, amount2 REAL, pollutant2 TEXT, PRIMARY KEY(plantid, releasesto, pollutant, year), FOREIGN KEY (plantid) REFERENCES plants(plantid) ON DELETE CASCADE);"

echo -e '.separator "," \n.import stammdaten_nh.csv addresses  \n.import plants_nh.csv plants \n.import blocks_nh.csv blocks\n. import monthly.csv month\n. import yearly_pg.csv yearly\n. import monthlyp_pg.csv monthp \n.import pollutants_pg.csv pollutions\n. import mt_pg.csv mtp' | sqlite3 plantwatch.db

#\n. import produced_power_pg.csv power

# 	year 	plantid 	pollutant 	releases_to 	amount 	potency 	unit_2 	amount_2
# plz 	ort 	strasse 	hausnr 	geo_lat_wgs84 	geo_long_wgs84
