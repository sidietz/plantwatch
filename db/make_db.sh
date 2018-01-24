#!/bin/bash
if [ -f plantwatch.db ]; then
   rm plantwatch.db
fi
sqlite3 plantwatch.db  "CREATE TABLE blocks(KraftwerkID TEXT, BlockID TEXT NOT NULL PRIMARY KEY, federalstate TEXT, energysource TEXT, initialop INTEGER, chp TEXT, blockname TEXT, netpower REAL, state TEXT, endop TEXT, company TEXT);"
sqlite3 plantwatch.db  "CREATE TABLE addresses(BlockID TEXT NOT NULL PRIMARY KEY, federalstate TEXT, place TEXT, PLZ INTEGER, street TEXT, FOREIGN KEY (BlockID) REFERENCES blocks(BlockID) ON DELETE CASCADE);"
echo -e '.separator "," \n.import blocks_nh.csv blocks \n.import stammdaten_nh.csv addresses' | sqlite3 plantwatch.db
