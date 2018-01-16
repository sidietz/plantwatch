#!/bin/bash
if [ -f plantwatch.db ]; then
   rm plantwatch.db
fi
sqlite3 plantwatch.db  "CREATE TABLE blocks(    KraftwerkID TEXT,    BlockID TEXT NOT NULL PRIMARY KEY,    company TEXT,    blockname TEXT, federalstate TEXT,    initialop INTEGER,    state TEXT,     energysource Text,    netpower REAL);"
sqlite3 plantwatch.db  "CREATE TABLE addresses( BlockID TEXT NOT NULL PRIMARY KEY, PLZ TEXT, place INTEGER, street TEXT, federalstate TEXT, blockinfo Text, FOREIGN KEY (BlockID) REFERENCES blocks(BlockID) ON DELETE CASCADE);"
echo -e '.separator "," \n.import blocks_nh.csv blocks \n.import stammdaten_nh.csv addresses' | sqlite3 plantwatch.db
