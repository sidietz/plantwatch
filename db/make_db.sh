#!/bin/bash
if [ -f plantwatch.db ]; then
   rm plantwatch.db
fi
sqlite3 plantwatch.db  "CREATE TABLE addresses(blockid TEXT NOT NULL PRIMARY KEY, plz INTEGER, place TEXT, street TEXT, street_number TEXT, federalstate TEXT);"

sqlite3 plantwatch.db  "CREATE TABLE blocks(blockid TEXT NOT NULL PRIMARY KEY, plantid TEXT, blockname TEXT, federalstate TEXT, energysource TEXT, initialop INTEGER, chp TEXT, netpower REAL, state TEXT, endop INT, company TEXT, FOREIGN KEY (blockid) REFERENCES addresses(blockid) ON DELETE CASCADE);"

sqlite3 plantwatch.db "CREATE TABLE month(monthid INTEGER NOT NULL PRIMARY KEY, year INT, month INT, blockid TEXT NOT NULL, power INTEGER NOT NULL, FOREIGN KEY (blockid) REFERENCES blocks(blockid) ON DELETE CASCADE);"

#plantid 	blockid 	blockname 	federalstate 	energysource 	initialop 	chp 	power 	state 	endop 	company 	reserveyear

sqlite3 plantwatch.db  "CREATE TABLE plants(plantid TEXT NOT NULL PRIMARY KEY, plantname TEXT, federalstate TEXT, energysource TEXT, chp TEXT, latestexpanded INT, initialop INT, totalpower REAL, state TEXT, blockcount INT,  company TEXT, plz TEXT, place TEXT, street TEXT, number TEXT, latitude REAL, longitude REAL, activepower REAL, energy_2015 INTEGER,  energy_2016 INTEGER,  energy_2017 INTEGER,  energy_2018 INTEGER,  energy_2019 INTEGER, energy_2020 INTEGER, energy_2021 INTEGER, energy_2022 INTEGER, energy_2023 INTEGER, energy_2024 INTEGER, co2_2007 INTEGER,  co2_2008 INTEGER,  co2_2009 INTEGER,  co2_2010 INTEGER,  co2_2011 INTEGER,  co2_2012 INTEGER,  co2_2013 INTEGER,  co2_2014 INTEGER,  co2_2015 INTEGER,  co2_2016 INTEGER,  co2_2017 INTEGER,  co2_2018 INTEGER, co2_2019 INTEGER, co2_2020 INTEGER, co2_2021 INTEGER, co2_2022 INTEGER, co2_2023 INTEGER, revenue REAL, profit REAL, FOREIGN KEY (plantid) REFERENCES blocks(plantid) ON DELETE CASCADE);"

sqlite3 plantwatch.db "CREATE TABLE power(powerid INTEGER NOT NULL PRIMARY KEY, producedat TIMESTAMP NOT NULL, blockid TEXT NOT NULL, power INTEGER NOT NULL, FOREIGN KEY (blockid) REFERENCES blocks(blockid) ON DELETE CASCADE);"


sqlite3 plantwatch.db "CREATE TABLE yearly(yid INTEGER NOT NULL PRIMARY KEY, year INTEGER NOT NULL, plantid TEXT NOT NULL, power INTEGER NOT NULL, FOREIGN KEY (plantid) REFERENCES plants(plantid) ON DELETE CASCADE);"

sqlite3 plantwatch.db "CREATE TABLE mtp(mtpid INTEGER NOT NULL PRIMARY KEY, plantid TEXT NOT NULL, power INTEGER NOT NULL, producedat TIM̀ESTAMP NOT NULL, FOREIGN KEY (plantid) REFERENCES plants(plantid) ON DELETE CASCADE);"

sqlite3 plantwatch.db  "CREATE TABLE pollutions(pollutionsid INTEGER NOT NULL, year INTEGER, plantid  TEXT NOT NULL, pollutant TEXT NOT NULL, releasesto TEXT NOT NULL, amount REAL, potency INTEGER NOT NULL, unit2 TEXT NOT NULL, amount2 REAL, pollutant2 TEXT, PRIMARY KEY(plantid, releasesto, pollutant, year), FOREIGN KEY (plantid) REFERENCES plants(plantid) ON DELETE CASCADE);"

echo -e '.separator "," \n.import stammdaten_nh_new.csv addresses  \n.import plants_with_profit.csv plants \n.import blocks_new_nh.csv blocks\n.import yearly_pg.csv yearly\n. import monthly.csv month\n. import pollutants_pg.csv pollutions' | sqlite3 plantwatch.db

#\n. import produced_power_pg.csv power

# 	year 	plantid 	pollutant 	releases_to 	amount 	potency 	unit_2 	amount_2
# plz 	ort 	strasse 	hausnr 	geo_lat_wgs84 	geo_long_wgs84


#
#sqlite3 plantwatch.db  "CREATE TABLE blocks(plantid TEXT, blockid TEXT NOT NULL PRIMARY KEY, blockdescription TEXT, federalstate TEXT, energysource TEXT, initialop INTEGER, chp TEXT, blockname TEXT, netpower REAL, state TEXT, endop INT, company TEXT, reserveyear INT, FOREIGN KEY (blockid) REFERENCES addresses(blockid) ON DELETE CASCADE);"

#sqlite3 plantwatch.db "CREATE TABLE month(monthid INTEGER NOT NULL PRIMARY KEY, year INT, month INT, blockid TEXT NOT NULL, power INTEGER NOT NULL, FOREIGN KEY (blockid) REFERENCES blocks(blockid) ON DELETE CASCADE);"

#sqlite3 plantwatch.db "CREATE TABLE monthp(monthpid INTEGER NOT NULL PRIMARY KEY, year INT, month INT, plantid TEXT NOT NULL, power INTEGER NOT NULL, FOREIGN KEY (plantid) REFERENCES plants(plantid) ON DELETE CASCADE);"

#echo -e '.separator "," \n.import stammdaten_nh_new.csv addresses  \n.import plants_nh_new.csv plants \n.import blocks_new_nh.csv blocks\n. import monthly.csv month\n. import yearly_pg.csv yearly\n. import monthlyp_pg.csv monthp \n.import pollutants_pg.csv pollutions\n. import mt_pg.csv mtp' | sqlite3 plantwat

#blocks entry
#06-05-100-0853075|BNA0990|KW West|Nordrhein-Westfalen|Steinkohle|1970|Nein|322.0|stillgelegt|2017.0||
