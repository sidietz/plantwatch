# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.1.14-e] - 2020-06-06
### Changed
- endop to int

### Fixed
- this and subsequent versions adhere to semver more accurately 
- headers of blocks table
- co2 for plants table

## [0.1.14d] - 2020-06-06
### Changed
- update dependencies

### Fixed
- filtering by energy source
- workload for plants is now based on totalpower, which fixes inconsistencies

## [0.1.14c] - 2020-06-06
### Changed
- update README

## [0.1.14b] - 2020-06-05
### Fixed
- active workload for retired blocks
- active workload for blocks with missing data

## [0.1.14a] - 2020-06-04
### Fixed
- active workload for retired blocks

## [0.1.14] - 2020-06-04
### Added
- active power and active workload for plants and blocks
- reserveyear for blocks

## [0.1.13] - 2020-05-31
### Fixed
- performance

### Removed
- plants slow

## [0.1.12c] - 2020-05-28
### Changed
- debug stuff is not displayed in html, when not present

### Fixed
- typos
- performance a little
- models

## [0.1.12b] - 2020-05-27
### Fixed
- plants not being sorted correctly
- plants not being filtered correctly

## [0.1.12a] - 2020-05-25
### Added
- plants slow

### Changed
- datasource for workload

## [0.1.12] - 2020-05-24
### Added
- workload for plants

## [0.1.11c] - 2020-05-24
### Added
- workload of previous year

## [0.1.11b] - 2020-05-24
### Fixed
- workload

## [0.1.11a] - 2020-05-24
### Changed
- refactor code
- update CHANGELOG
- update README

### Fixed
- workload

## [0.1.11] - 2020-05-23
### Added
- guage chart for workload

### Changed
- update CHANGELOG

## [0.1.10a] - 2020-05-23
### Chanced
- remove debug stuff
- modularize stuff
- increase verbosity if no data is available

### Fixed
- various divison by zero related bugs

## [0.1.10] - 2020-05-22
### Added
- energy, workload and efficiency to plant list
- documentation about known bug

### Changed
- summary table to show correct not guessed data
- power unit in summary table from MW to GW
- prtr data is now consistently rounded to three (3) decimal places

## [0.1.9] - 2020-05-22
### Added
- prtr table for all available years

### Changed
- refactoring
- html intendation

### Fixed
- polutans not beeing sorted descending by potency and exponent
- missing prtr data for plant causing HTML 500 errors

## [0.1.8f] - 2020-05-22
### Changed
- clean up html

### Fixed
-  missing prtr co2 data causing charts not to display

## [0.1.8e] - 2020-05-21
### Fixed
-  hotfix prtr table bug

## [0.1.8d] - 2020-05-21
### Added
- prtr data for 2018

### Changed
- refactoring
- prtr year picked from range if most recent year does not exists

### Fixed
- various wrong google maps views
- improve missing prtr value handling

### Removed
- magic values

## [0.1.8c] - 2020-05-21
### Fixed
- various wrong google maps views

## [0.1.8b] - 2020-05-21
### Fixed
- html rendering in chrome

## [0.1.8a] - 2020-05-21
### Fixed
- charts not displaying

## [0.1.8] - 2020-05-21
### Added
- workload by plant over years
- random plant

### Changed
- year range displayed in charts
- links not to use the browser's back functionality, anymore.
- foreign key relationships in models

### Fixed
- html spacing
- random empty rows appearing in tables
- fatal calculation bug resulting in wrong workload data

## [0.1.7a] - 2020-05-20
### Changed
- year range displayed in charts

### Fixed
- plants not showing prtr data if shutdown was after 2015
- various wrong google maps views
- various missing data related bugs

## [0.1.7] - 2020-05-18
### Added
- pollution data for plants
- summary table including energy, co2 emmisions and efficiency

### Changed
- make-db script

### Fix
- url in README

## [0.1.6] - 2020-05-18
### Added
- pollution data for plants
- summary table including energy, co2 emmisions and efficiency

### Changed
- make-db script

### Fix
- url in README

## [0.1.5b] - 2020-05-17
### Fix
- url in README

## [0.1.5a] - 2020-05-17
### Removed
- even more csv blobs from repo

## [0.1.5] - 2020-05-17
### Added
- english translation of README
- some fields to plant model
- google maps view of plant
- company in plant page

### Changed
- simplify gitignore

### Removed
- csv blobs from repo

## [0.1.4a] - 2020-05-17
### Changed
- workload chart range from default to 0 up to 100
- filtering to include oil and gas, too
- update dependencies

## [0.1.4] - 2020-05-16
### Added
- pollution data from PRTR
- workload data based on production data from SMARD
- fancy charts

### Changed
- make-db script
- database to be split up auth.db and plantwatch.db
- foreign key relationships in models
- update dependencies
- sorting to sort by netpower or totalpower, respectively

## [0.1.3b] - 2020-05-03
### Added
- blockname column in blocks overview

### Removed
- db from repo

### Fixed
- empty value handling

## [0.1.3a] - 2019-05-18
### Fixed
- various bug fixes

## [0.1.3] - 2018-12-27
### Added
- slider to filter by net/total power

### Changed
- updated data to 2018-11-19
- gas fired and nuclear power plants are not shown by default anymore
- plants with a power output below a certain cutoff value are not shown by default anymore

### Removed
- some dead code
- some unneeded files

### Fixed
- calculation of summary in plants, consistency between plants and blocks
- minor fixes in impressum

## [0.1.2c] - 2018-03-14
### Changed
- slider in plants now represents operation begin (initial op), again.

### Fixed
- calculation of summary in plants, consistency between plants and blocks
- minor fixes in impressum

## [0.1.2b] - 2018-03-08
### Changed
- minor database / model changes

### Removed
- lots of dead code

### Fixed
- inconsisties between plants and blocks lowered
- duplicated values in dataset removed
- plant summary now takes user's search requests into account

## [0.1.2a] - 2018-03-05
### Fixed
- release critcal bugs
- catch any database errors and deliver 404 errors
- fix inconsisties and errors related to one plant having exactly one block or blocks which do not have a plant at all

## [0.1.2] - 2018-03-05
### Added
- landscape config
- plants (complete!)

### Changed
- various landscape smells and errors fixed
- several internal interfaces for better generality

### Removed
- some dead code
- some legacy files
- some unused imports

### Fixed
- some bugs in CHANGELOG
- README should now correctly show the landscape badget

## [0.1.1] - 2018-02-15
### Added
- plants accessable by blocks
- README

### Changed
- blocks overview now shows the annual total production of the selected plants.
- blocks allows the user to switch not only to the detailed block, but to the plant as well. 

### Fixed
- some ui and ui consistency improvements
- some localization improvements

## [0.1.0c] - 2018-01-25
### Added
- deploy script to toggle settings.py.

### Changed
- eval() part has been rewritten.

### Removed
- every use of eval() has been removed.

### Security
- vulnerability to eval() threats fixed.

## [0.1.0b] - 2018-01-24
### Added
- option to search by operating state.
- option to search by chp.

### Changed
- plants fired by more than one energy source are now contained as well.

### Fixed
- search did not contain all plants.

## [0.1.0a] - 2018-01-21
### Added
- CHANGELOG
- option to choose the sort behavior from 'ascending' and 'descending'.
- option to search by federal state.
- table to display a summary

### Changed
- frist column of every table is now bold.
- slider does not automatically changes the search and now reacts to the 'change request' button.

### Removed
- some dead js code.

### Fixed
- tremendous ui improvements.
- changing the slider does not remove the choices in other options

## [0.1.0] - 2018-01-16
### Added
- nuclear power plants.
- nav bar, impressium
- option to sort by 'initial operation' or 'power'

### Changed
- filter by energysource has been changed from js based to django form based.

### Removed
- lots of dead js code.
