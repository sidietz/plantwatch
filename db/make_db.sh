#!/bin/bash
if [ -f plantwatch.db ]; then
   rm plantwatch.db
fi
sqlite3 plantwatch.db  "CREATE TABLE addresses(blockid TEXT NOT NULL PRIMARY KEY, federalstate TEXT, place TEXT, plz INTEGER, street TEXT);"

sqlite3 plantwatch.db  "CREATE TABLE blocks(plantid TEXT, blockid TEXT NOT NULL PRIMARY KEY, blockdescription TEXT, federalstate TEXT, energysource TEXT, initialop INTEGER, chp TEXT, blockname TEXT, netpower REAL, state TEXT, endop TEXT, company TEXT, FOREIGN KEY (blockid) REFERENCES addresses(blockid) ON DELETE CASCADE);"

sqlite3 plantwatch.db  "CREATE TABLE plants(plantid TEXT NOT NULL PRIMARY KEY, plantname TEXT, federalstate TEXT, energysource TEXT, chp TEXT, latestexpanded INT, initialop INT, totalpower REAL, state TEXT, blockcount INT,  company TEXT, plz TEXT, place TEXT, street TEXT, number TEXT, latitude REAL, longitude REAL, FOREIGN KEY (plantid) REFERENCES blocks(plantid) ON DELETE CASCADE);"

sqlite3 plantwatch.db "CREATE TABLE power(powerid INTEGER NOT NULL PRIMARY KEY, producedat TIMESTAMP NOT NULL, blockid TEXT NOT NULL, power INTEGER NOT NULL, FOREIGN KEY (blockid) REFERENCES blocks(blockid) ON DELETE CASCADE);"

sqlite3 plantwatch.db "CREATE TABLE month(monthid INTEGER NOT NULL PRIMARY KEY, year INT, month INT, blockid TEXT NOT NULL, power INTEGER NOT NULL, FOREIGN KEY (blockid) REFERENCES blocks(blockid) ON DELETE CASCADE);"

sqlite3 plantwatch.db  "CREATE TABLE pollutions(pollutionsid INTEGER NOT NULL, year INTEGER, plantid  TEXT NOT NULL, pollutant TEXT NOT NULL, releasesto TEXT NOT NULL, amount REAL, potency INTEGER NOT NULL, unit2 TEXT NOT NULL, amount2 REAL, PRIMARY KEY(plantid, releasesto, pollutant, year), FOREIGN KEY (plantid) REFERENCES plants(plantid) ON DELETE CASCADE);"

echo -e '.separator "," \n.import stammdaten_nh.csv addresses  \n.import plants_nh.csv plants \n.import blocks_nh.csv blocks\n. import produced_power_pg.csv power\n. import monthly.csv month \n.import pollutants_pg.csv pollutions ' | sqlite3 plantwatch.db

# 	year 	plantid 	pollutant 	releases_to 	amount 	potency 	unit_2 	amount_2
# plz 	ort 	strasse 	hausnr 	geo_lat_wgs84 	geo_long_wgs84
