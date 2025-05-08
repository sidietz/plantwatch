OIL = "Mineralölprodukte"
ENERGY_SOURCE = "Energieträger"
YEARLY_PRD = "Jahresproduktion [TWh]"
NETOP = "Nennleistung [GW]"

SORT_CRITERIA_BLOCKS = ([('blockname', 'Name'), ('netpower', 'Nennleistung'),
                         ('initialop', 'Inbetriebnahme')], "netpower")
SORT_CRITERIA_PLANTS = ([('plantid', 'PlantID'),
                         ('plantname', 'Name'),
                         ('totalpower', 'Gesamtleistung'),
                         ('initialop', 'Inbetriebnahme'),
                         ('latestexpanded', 'Zuletzt erweitert'),
                         ('co2_2023', 'CO2 Ausstoß'),
                         ('energy_2023', 'Energie')], "co2_2023")
SORT_CRITERIA_PLANTS_OLD = ([('plantname', 'Name'),
                             ('totalpower', 'Gesamtleistung'),
                             ('initialop', 'Inbetriebnahme'),
                             ('latestexpanded', 'Zuletzt erweitert')],
                            "totalpower")


SLIDER_1 = "1950;2030"
SLIDER_2p = "300;4500"
SLIDER_2b = "250;1500"

HOURS_IN_YEAR = 365 * 24


SL_1 = [1950, 2030, 1950, 2030, 5]
SL_2b = [250, 1500, 0, 1500, 250]
SL_2p = [250, 4500, 0, 4500, 250]

HOURS_IN_YEAR = 365 * 24
PRTR_YEARS = list(range(2007, 2024))
ENERGY_YEARS = list(range(2015, 2025))
YEARS = ENERGY_YEARS
YEAR = ENERGY_YEARS[-1]
LATEST_YEAR = ENERGY_YEARS[-1]

FULL_HOURS = "Volllaststunden [" + str(YEAR) + "]"

FEDERAL_STATES = ['Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg',
                  'Bremen', 'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern',
                  'Niedersachsen', 'Nordrhein-Westfalen', 'Rheinland-Pfalz',
                  'Saarland', 'Sachsen', 'Sachsen-Anhalt',
                  'Schleswig-Holstein', 'Thüringen']
SOURCES_LIST = ['Erdgas', 'Braunkohle', "Steinkohle", "Kernenergie", OIL]
OPSTATES = ['in Betrieb', 'Kapazitätsreserve', 'Netzreserve', 'Strommarktrückkehr', 'bnBm','KVBG', 'vorläufig stillgelegt', 'stillgelegt']


#
#

#STATES = ['in Betrieb', 'Kapazitätsreserve', 'Netzreserve', 'Strommarktrückkehr', 'vorläufig stillgelegt', 'stillgelegt §13b EnWG', 'stillgelegt KVBG', 'stillgelegt']
#ACTIVE_STATES = ['in Betrieb', 'Kapazitätsreserve', 'Netzreserve', 'Strommarktrückkehr', 'vorläufig stillgelegt']

ACTIVE_OPS = OPSTATES[0:5]
DEFAULT_OPSTATES = ACTIVE_OPS
#['in Betrieb', 'Gesetzlich an Stilllegung gehindert', 'Sicherheitsbereitschaft', 'Netzreserve', 'Sonderfall', 'Kohlestromvermarktungsverbot']
DEFAULT_OPS = DEFAULT_OPSTATES
SELECT_CHP = [("Nein", "keine Kraft-Wärme-Kopplung"),
              ("Ja", "Kraft-Wärme-Kopplung"), ("", "unbekannt")]
SELECT_CHP_LIST = ["Ja", "Nein", ""]
SOURCES_DICT = {'Erdgas': 1220, 'Braunkohle': 6625, "Steinkohle": 3000,
                    "Kernenergie": 0, OIL: 1000}
FULL_YEAR = 8760

PLANT_COLOR_MAPPING = {"Steinkohle": "table-danger", "Braunkohle": "table-warning",
                       "Erdgas": "table-success", "Kernenergie": "table-info",
                       OIL: "table-secondary"}
HEADER_BLOCKS = ['Kraftwerk','Block', 'Krafwerksname', 'Blockname',
                 'Inbetriebnahme', 'Abschaltung', 'KWK', 'Status',
                 'Bundesland', 'Nennleistung [in MW]']
SOURCES_PLANTS = [ENERGY_SOURCE, "Anzahl", NETOP, YEARLY_PRD, "CO2 [Mio. t]",
                  "Volllaststunden [h]", "Auslastung [%]", "Effizienz [g CO2/kWh]"]
SOURCES_BLOCKS = [ENERGY_SOURCE, "Anzahl", NETOP, YEARLY_PRD, "Volllaststunden [h]",
                  "Auslastung 2023 [%]", "Auslastung 2023 [%]"]


SOURCES_BLOCKS_OLD = [ENERGY_SOURCE, "Anzahl", NETOP, YEARLY_PRD,
                      "Volllaststunden [" + str(YEAR) + "]",
                      "Auslastung [" + str(YEAR) + "] [%]",
                      "Auslastung [" + str(LATEST_YEAR) + "] [%]"]

try:
    with open('/home/oberam/etc/api_key.txt') as f:
        API_KEY = f.read().strip()
except FileNotFoundError:
    API_KEY = ""
