all:
	#!/bin/bash
	sqlite3 plantwatch.db  "CREATE TABLE blocks(    KraftwerkID TEXT,    BlockID TEXT NOT NULL PRIMARY KEY,    company TEXT,    blockname TEXT,    initialop INTEGER,    state TEXT,    energysource Text,    netpower REAL);"
	sqlite3 plantwatch.db  "CREATE TABLE addresses( BlockID TEXT NOT NULL PRIMARY KEY, PLZ TEXT, place INTEGER, street TEXT, federalstate TEXT, blockinfo Text, FOREIGN KEY (BlockID) REFERENCES blocks(BlockID) ON DELETE CASCADE);"
	sqlite3 plantwatch.db ".mode csv" << EOF
	sqlite3 plantwatch.db ".import blocks_3_nh.csv blocks"
	sqlite3 plantwatch.db ".import stammdaten_nh.csv addresses"
	EOF
