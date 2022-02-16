#!/bin/bash
if [ -f plantwatch.db ]; then
   rm plantwatch.db
fi
sqlite3 plantwatch.db  "CREATE TABLE addresses(blockid TEXT NOT NULL PRIMARY KEY, plz INTEGER, place TEXT, street TEXT, federalstate TEXT);"

sqlite3 plantwatch.db  "CREATE TABLE blocks(plantid TEXT, blockid TEXT NOT NULL PRIMARY KEY, blockdescription TEXT, federalstate TEXT, energysource TEXT, initialop INTEGER, chp TEXT, blockname TEXT, netpower REAL, state TEXT, endop INT, company TEXT, reserveyear INT, FOREIGN KEY (blockid) REFERENCES addresses(blockid) ON DELETE CASCADE);"

sqlite3 plantwatch.db  "CREATE TABLE plants(plantid TEXT NOT NULL PRIMARY KEY, plantname TEXT, federalstate TEXT, energysource TEXT, chp TEXT, latestexpanded INT, initialop INT, totalpower REAL, state TEXT, blockcount INT,  company TEXT, plz TEXT, place TEXT, street TEXT, number TEXT, latitude REAL, longitude REAL, activepower REAL, energy_2015 INTEGER,  energy_2016 INTEGER,  energy_2017 INTEGER,  energy_2018 INTEGER,  energy_2019 INTEGER, energy_2020 INTEGER, energy_2021 INTEGER, co2_2007 INTEGER,  co2_2008 INTEGER,  co2_2009 INTEGER,  co2_2010 INTEGER,  co2_2011 INTEGER,  co2_2012 INTEGER,  co2_2013 INTEGER,  co2_2014 INTEGER,  co2_2015 INTEGER,  co2_2016 INTEGER,  co2_2017 INTEGER,  co2_2018 INTEGER, co2_2019 INTEGER, FOREIGN KEY (plantid) REFERENCES blocks(plantid) ON DELETE CASCADE);"

sqlite3 plantwatch.db "CREATE TABLE power(powerid INTEGER NOT NULL PRIMARY KEY, producedat TIMESTAMP NOT NULL, blockid TEXT NOT NULL, power INTEGER NOT NULL, FOREIGN KEY (blockid) REFERENCES blocks(blockid) ON DELETE CASCADE);"

sqlite3 plantwatch.db "CREATE TABLE month(monthid INTEGER NOT NULL PRIMARY KEY, year INT, month INT, blockid TEXT NOT NULL, power INTEGER NOT NULL, FOREIGN KEY (blockid) REFERENCES blocks(blockid) ON DELETE CASCADE);"

sqlite3 plantwatch.db "CREATE TABLE monthp(monthpid INTEGER NOT NULL PRIMARY KEY, year INT, month INT, plantid TEXT NOT NULL, power INTEGER NOT NULL, FOREIGN KEY (plantid) REFERENCES plants(plantid) ON DELETE CASCADE);"

sqlite3 plantwatch.db "CREATE TABLE yearly(yid INTEGER NOT NULL PRIMARY KEY, year INTEGER NOT NULL, plantid TEXT NOT NULL, power INTEGER NOT NULL, FOREIGN KEY (plantid) REFERENCES plants(plantid) ON DELETE CASCADE);"

sqlite3 plantwatch.db "CREATE TABLE mtp(mtpid INTEGER NOT NULL PRIMARY KEY, plantid TEXT NOT NULL, power INTEGER NOT NULL, producedat TIM̀ESTAMP NOT NULL, FOREIGN KEY (plantid) REFERENCES plants(plantid) ON DELETE CASCADE);"

sqlite3 plantwatch.db  "CREATE TABLE pollutions(pollutionsid INTEGER NOT NULL, year INTEGER, plantid  TEXT NOT NULL, pollutant TEXT NOT NULL, releasesto TEXT NOT NULL, amount REAL, potency INTEGER NOT NULL, unit2 TEXT NOT NULL, amount2 REAL, pollutant2 TEXT, PRIMARY KEY(plantid, releasesto, pollutant, year), FOREIGN KEY (plantid) REFERENCES plants(plantid) ON DELETE CASCADE);"

echo -e '.separator "," \n.import stammdaten_nh.csv addresses  \n.import plants_new_nh.csv plants \n.import blocks_new_nh.csv blocks\n. import monthly.csv month\n. import yearly_pg.csv yearly\n. import monthlyp_pg.csv monthp \n.import pollutants_pg.csv pollutions\n. import mt_pg.csv mtp' | sqlite3 plantwatch.db

#\n. import produced_power_pg.csv power

# 	year 	plantid 	pollutant 	releases_to 	amount 	potency 	unit_2 	amount_2
# plz 	ort 	strasse 	hausnr 	geo_lat_wgs84 	geo_long_wgs84
