#!/bin/bash
if [ -f plantwatch.db ]; then
   rm plantwatch.db
fi
sqlite3 plantwatch.db  "CREATE TABLE addresses(blockid TEXT NOT NULL PRIMARY KEY, federalstate TEXT, place TEXT, plz INTEGER, street TEXT);"
sqlite3 plantwatch.db  "CREATE TABLE blocks(plantid TEXT, blockid TEXT NOT NULL PRIMARY KEY, federalstate TEXT, energysource TEXT, initialop INTEGER, chp TEXT, blockname TEXT, netpower REAL, state TEXT, endop TEXT, company TEXT, FOREIGN KEY (blockid) REFERENCES addresses(blockid) ON DELETE CASCADE);"
sqlite3 plantwatch.db  "CREATE TABLE plants(plantid TEXT NOT NULL PRIMARY KEY, plantname TEXT, federalstate TEXT, energysource TEXT, chp TEXT, latestexpanded INT, initialop INT, totalpower REAL, state TEXT, blockcount INT,  company TEXT, FOREIGN KEY (plantid) REFERENCES blocks(plantid) ON DELETE CASCADE);"
sqlite3 plantwatch.db  "CREATE TABLE pollutions(plantid TEXT NOT NULL, releases_to TEXT, pollutant TEXT NOT NULL, amount REAL, potency INT, unit_2 TEXT, year INT NOT NULL, PRIMARY KEY(plantid, releases_to, pollutant, year), FOREIGN KEY (plantid) REFERENCES plants(plantid) ON DELETE CASCADE);"
echo -e '.separator "," \n.import stammdaten_nh.csv addresses  \n.import plants_nh.csv plants \n.import blocks_nh.csv blocks \n.import pollutions_nh.csv pollutions ' | sqlite3 plantwatch.db
