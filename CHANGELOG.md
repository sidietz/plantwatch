# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).
## [0.0.13a] - 2019-05-18
### Fixed
- various bug fixes
## [0.0.13] - 2018-12-27
### Added
- slider to filter by net/total power

### Changed
- updated data to 2018-11-19
- gas fired and nuclear power plants are not shown by default anymore
- plants with a power output below a certain cutoff value are not shown by default anymore

### Fixed
- calculation of summary in plants, consistency between plants and blocks
- minor fixes in impressum

### Removed
- some dead code
- some unneeded files

## [0.0.12a] - 2018-03-14
### Changed
- slider in plants now represents operation begin (initial op), again.

### Fixed
- calculation of summary in plants, consistency between plants and blocks
- minor fixes in impressum

## [0.0.12] - 2018-03-08
### Changed
- minor database / model changes

### Removed
- lots of dead code

### Fixed
- inconsisties between plants and blocks lowered
- duplicated values in dataset removed
- plant summary now takes user's search requests into account

## [0.0.11a] - 2018-03-05
### Fixed
- release critcal bugs
- catch any database errors and deliver 404 errors
- fix inconsisties and errors related to one plant having exactly one block or blocks which do not have a plant at all

## [0.0.11] - 2018-03-05
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
- some bugs in Changelog
- README should now correctly show the landscape badget

## [0.0.10] - 2018-02-15
### Added
- plants accessable by blocks
- README

### Changed
- blocks overview now shows the annual total production of the selected plants.
- blocks allows the user to switch not only to the detailed block, but to the plant as well. 

### Fixed
- some ui and ui consistency improvements
- some localization improvements

## [0.0.9e] - 2018-01-25
### Added
- deploy script to toggle settings.py.

### Changed
- eval() part has been rewritten.

### Removed
- every use of eval() has been removed.

### Security
- vulnerability to eval() threats fixed.

## [0.0.9d] - 2018-01-24
### Added
- option to search by operating state.
- option to search by chp.

### Changed
- plants fired by more than one energy source are now contained as well.

### Fixed
- search did not contain all plants.

## [0.0.9c] - 2018-01-21
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

## [0.0.9b] - 2018-01-16
### Added
- nuclear power plants.
- nav bar, impressium
- option to sort by 'initial operation' or 'power'

### Changed
- filter by energysource has been changed from js based to django form based.

### Removed
- lots of dead js code.
