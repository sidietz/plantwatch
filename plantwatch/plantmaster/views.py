#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .models import Blocks, Plants
from django.db.models import Sum, Min
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, F
from django.forms.models import model_to_dict
from .forms import BlocksForm
from functools import reduce


FEDERAL_STATES = ['Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg', 'Bremen', 'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern', 'Niedersachsen', 'Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland', 'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']
SOURCES_LIST = ['Erdgas', 'Braunkohle', "Steinkohle", "Kernenergie"]
SORT_CRITERIA_BLOCKS = ([('netpower', 'Nennleistung'), ('initialop', 'Inbetriebnahme')], "initialop")
SORT_CRITERIA_PLANTS = ([('totalpower', 'Gesamtleistung'),('initialop', 'Inbetriebnahme'), ('latestexpanded', 'Zuletzt erweitert')], "initialop")
OPSTATES = ['in Betrieb', 'Gesetzlich an Stilllegung gehindert', 'Netzreserve',  'Sicherheitsbereitschaft', 'Sonderfall', 'vorläufig stillgelegt', 'stillgelegt']
DEFAULT_OPSTATES = ['in Betrieb', 'Gesetzlich an Stilllegung gehindert', 'Netzreserve',  'Sicherheitsbereitschaft', 'Sonderfall']
SELECT_CHP = [("Nein", "keine Kraft-Wärme-Kopplung"), ("Ja", "Kraft-Wärme-Kopplung"), ("", "unbekannt")]
SELECT_CHP_LIST = ["Ja", "Nein", ""]
SOURCES_DICT = {'Erdgas': 1220, 'Braunkohle': 6625, "Steinkohle": 3000, "Kernenergie": 6700}
FULL_YEAR = 8760
SLIDER_1 = "1950;2020"
SLIDER_2p = "300;4500"
SLIDER_2b = "250;1500"
PLANT_COLOR_MAPPING = {"Steinkohle": "table-danger", "Braunkohle": "table-warning", "Erdgas": "table-success", "Kernenergie": "table-secondary"}
HEADER_BLOCKS = ['Kraftwerk','Block', 'Name', 'Inbetriebnahme', 'Abschaltung', 'KWK', 'Status', 'Bundesland', 'Nennleistung [in MW]']
SOURCES_BLOCKS = ["Energieträger", "Anzahl", "Nennleistung [in MW]", "Jahresproduktion [in TWh]", "Volllaststunden [pro Jahr]"]

SL_1 = [1950, 2020, 1950, 2020, 5]
SL_2b = [250, 1500, 0, 1500, 250]
SL_2p = [300, 4500, 0, 4500, 300]


def filter_and(queryset, filtered, filters):
    for afilter in filters:
        queryset = filter_queryset(queryset, filtered, afilter)
    return queryset


def filter_or(queryset, filtered, filters):
    """Chain or filters
    Thanks to https://stackoverflow.com/questions/852414/how-to-dynamically-compose-an-or-query-filter-in-django"""
    query = reduce(lambda q, value: q | Q(**{filtered: value}), filters, Q())
    queryset = queryset.all().filter(query)
    return queryset


def filter_queryset(queryset, filtered, afilter):
    param = {filtered: afilter}
    new_queryset = queryset.all().filter(**param)
    return new_queryset


def forge_sources_dict(block_list, power_type):

    sources_dict = {}
    whole_power = 0
    factors = []
    for source in SOURCES_LIST:
        tmp = filter_or(block_list, "energysource", [source])
        factor = SOURCES_DICT[source]
        factors.append(factor)
        raw_power = tmp.all().aggregate(Sum(power_type))[power_type + '__sum'] or 0
        power = round(raw_power, 2)
        anual_power = round((raw_power * factor) / (10**6), 2)
        whole_power += anual_power
        count = tmp.all().count()
        sources_dict[source] = [count, power, anual_power, factor]
    power = block_list.all().aggregate(Sum(power_type))[power_type + '__sum'] or 1
    power = round(power, 2)
    count = block_list.all().count()
    whole_power = round(whole_power, 2)
    sources_dict["Summe"] = [count, power, whole_power, round(whole_power * 1000000 / power)]
    return sources_dict


def handle_sliders(sliders):
    new_sliders = list(map(handle_slider, sliders))
    return new_sliders


def handle_slider(slider):
    new_slider = list(map(int, slider.split(';')))
    return new_slider


def handle_slider_1(slider):
    new_slider = handle_slider(slider)
    new_slider.extend(SL_1[2:])
    return new_slider


def handle_slider_2(slider, is_plants):
    new_slider = handle_slider(slider)
    if is_plants:
        new_slider.extend(SL_2p[2:])
    else:
        new_slider.extend(SL_2b[2:])
    # raise TypeError(new_slider)
    return new_slider


def initialize_form(request, SORT_CRITERIA=SORT_CRITERIA_BLOCKS, plants=False):
    slider1 = SLIDER_1

    if plants:
        sl2 = SLIDER_2p
    else:
        sl2 = SLIDER_2b
    slider2 = sl2
    sort_criteria = SORT_CRITERIA[1]
    sort_method = ""
    search_federalstate = []
    search_power = ['Braunkohle', "Steinkohle", "Kernenergie"]
    search_opstate = DEFAULT_OPSTATES
    search_chp = []

    if request.method == 'POST':
        form = BlocksForm(request.POST)
        sort_criteria = request.POST.get('sort_by', SORT_CRITERIA[1])
        search_federalstate = request.POST.getlist('select_federalstate', [])
        search_power = request.POST.getlist('select_powersource', [])
        search_opstate = request.POST.getlist('select_opstate', DEFAULT_OPSTATES)
        search_chp = request.POST.getlist('select_chp', [])
        slider1 = request.POST.get('slider1', SLIDER_1)
        slider2 = request.POST.get('slider2', sl2)
        sort_method = request.POST.get('sort_method', sort_method)
    else:
        form = BlocksForm()

    form.fields['sort_by'].choices = SORT_CRITERIA[0]
    form.fields['sort_by'].initial = sort_criteria or SORT_CRITERIA[1]
    form.fields['sort_by'].label = "Sortiere nach:"

    form.fields['sort_method'].choices = [('-', 'absteigend'), ('', 'aufsteigend')]
    form.fields['sort_method'].initial = sort_method
    form.fields['sort_method'].label = "aufsteigend oder absteigend?"

    form.fields['select_chp'].choices = SELECT_CHP
    form.fields['select_chp'].initial = search_chp or SELECT_CHP_LIST
    form.fields['select_chp'].label = "Filtere nach Kraft-Wärme-Kopplung:"

    form.fields['select_federalstate'].choices = list(zip(FEDERAL_STATES, FEDERAL_STATES))
    form.fields['select_federalstate'].initial = search_federalstate  # or FEDERAL_STATES
    form.fields['select_federalstate'].label = "Filtere nach Bundesland:"

    form.fields['select_powersource'].choices = list(zip(SOURCES_LIST, SOURCES_LIST))
    form.fields['select_powersource'].initial = search_power or SOURCES_LIST
    form.fields['select_powersource'].label = "Filtere nach Energieträger:"

    form.fields['select_opstate'].choices = list(zip(OPSTATES, OPSTATES))
    form.fields['select_opstate'].initial = search_opstate or ['in Betrieb', 'Gesetzlich an Stilllegung gehindert',
                                                               'Netzreserve', 'Sicherheitsbereitschaft', 'Sonderfall']
    form.fields['select_opstate'].label = "Filtere nach Betriebszustand:"

    form.fields['slider1'].initial = slider1
    form.fields['slider1'].label = "Filtere nach Zeitraum"

    form.fields['slider2'].initial = slider2
    form.fields['slider2'].label = "Filtere nach Nennleistung"

    if not search_power:
        search_power = SOURCES_LIST
    if not search_opstate:
        search_opstate = ["in Betrieb", "Sonderfall", "Gesetzlich an Stilllegung gehindert"]
    if not search_chp:
        search_chp = ["Nein", "Ja", ""]
    if not search_federalstate:
        search_federalstate = FEDERAL_STATES

    slider_1 = handle_slider_1(slider1)
    slider_2 = handle_slider_2(slider2, plants)
    # raise TypeError(slider_2)
    return form, search_power, search_opstate, search_federalstate, search_chp, sort_method, sort_criteria, [slider_1,
                                                                                                             slider_2]


def create_block_list(block_list, filter_dict):
    for filter_tag, filtered in filter_dict.items():
        block_list = filter_or(block_list, filter_tag, filtered)
    return block_list


def efficiency(request):
    form, search_power, search_opstate, search_federalstate, search_chp, sort_method, sort_criteria, sliders = initialize_form(
        request)

    #  lower, upper = create_low_up(slider1)

    block_list = Blocks.objects.order_by(sort_method + sort_criteria)
    filter_dict = {"energysource": search_power, "state": search_opstate, "federalstate": search_federalstate,
                   "chp": search_chp}
    block_list = create_block_list(block_list, filter_dict)

    block_list = block_list.filter(initialop__range=sliders[0][0:1])
    block_list = block_list.filter(fullload__is_null=False)
    block_list = block_list.filter(pollutions__pollutant="CO2")
    block_list = block_list.filter(pollutions__pollutant="CO2")
    block_list.annotate(production=(F('blocks__netpower') * F('') * FULL_YEAR))
    block_list.annotate(efficiency=(F('')))

    sources_dict = forge_sources_dict(block_list, "netpower")

    block_list = block_list[::1]
    block_tmp_dict = list(map(model_to_dict, block_list))
    value_list = ["blockname", "initialop", "endop", "chp", "state", "federalstate", "fullload", "netpower"]
    key_list = ["energysource", "blockid", "plantid"]
    block_dict = create_blocks_dict(block_tmp_dict, value_list, key_list)

    header_list = ['Kraftwerk', 'Block', 'Name', 'Inbetriebnahme', 'Abschaltung', 'KWK', 'Status', 'Bundesland',
                   'Volllast [in %]', 'Nennleistung [in MW]']
    sources_header = ["Energieträger", "Anzahl", "Nennleistung [in MW]", "Jahresproduktion [in TWh]",
                      "Volllaststunden [pro Jahr]"]
    context = {
        'header_list': header_list,
        'form': form,
        'block_dict': block_dict,
        'sources_dict': sources_dict,
        'sources_header': sources_header,
        'plant_mapper': PLANT_COLOR_MAPPING,
        'range': range(2),
    }
    return render(request, 'plantmaster/blocks.html', context)


def blocks(request):
    form, search_power, search_opstate, search_federalstate, search_chp, sort_method, sort_criteria, sliders = initialize_form(request)
    # slider = list(map(create_low_up, sliders))
    slider = sliders

    block_list = Blocks.objects.order_by(sort_method + sort_criteria)
    filter_dict = {"energysource": search_power, "state": search_opstate, "federalstate": search_federalstate, "chp": search_chp}
    block_list = create_block_list(block_list, filter_dict)

    # print(block_list)

    block_list = block_list.filter(initialop__range=(slider[0][0], slider[0][1]))
    block_list = block_list.filter(netpower__range=(slider[1][0], slider[1][1]))

    # print(block_list)

    sources_dict = forge_sources_dict(block_list, "netpower")

    block_list = block_list[::1]
    block_tmp_dict = list(map(model_to_dict, block_list))
    value_list = ["blockname", "initialop", "endop", "chp", "state", "federalstate", "netpower"]
    key_list = ["energysource", "blockid", "plantid"]
    block_dict = create_blocks_dict(block_tmp_dict, value_list, key_list)

    header_list = HEADER_BLOCKS
    sources_header = SOURCES_BLOCKS
    context = {
        'header_list': header_list,
        'slider': slider,
        'form': form,
        'block_dict': block_dict,
        'sources_dict': sources_dict,
        'sources_header': sources_header,
        'plant_mapper': PLANT_COLOR_MAPPING,
        'range': range(2),
    }
    return render(request, 'plantmaster/blocks.html', context)


def create_blocks_dict(block_tmp_dict, value_list, key_list):
    block_dict = {}
    # print(key_list)
    for entry in block_tmp_dict:
        key = []
        for a_key in key_list:
            key.append(entry[a_key])
        value = []
        for element in value_list:
            value.append(entry[element])
            block_dict[tuple(key)] = value
    return block_dict


def block(request, blockid):
    block = get_object_or_404(Blocks, blockid=blockid)

    address = block.blockid
    plant_id = block.plantid
    error = True if not plant_id else False

    data_list = [plant_id, block.blockname, address.plz, address.place, address.street, address.federalstate, block.netpower]
    header_list = ['PlantID', 'Name', 'PLZ', 'Ort', 'Anschrift', 'Bundesland', 'Nennleistung']
    context = {
        'data_list': zip(header_list, data_list),
        'plant_id': plant_id,
        'error': error
    }
    return render(request, "plantmaster/block.html", context)


def impressum(request):
    return render(request, "plantmaster/impressum.html", {})


def plants_2(request):
    form, search_power, search_opstate, search_federalstate, search_chp, sort_method, sort_criteria, slider = initialize_form(request, SORT_CRITERIA=SORT_CRITERIA_PLANTS, plants=True)
    plant_list = Plants.objects.all().filter(initialop__range=(slider[0][0], slider[0][1])).filter(totalpower__range=(slider[1][0], slider[1][1])).order_by(sort_method + sort_criteria)

    filter_dict = {"energysource": search_power, "state": search_opstate, "federalstate": search_federalstate}
    block_list = Blocks.objects.filter(plantid__in=plant_list.values("plantid"))
    # block_list = block_list.filter(initialop__range=(slider[0][0], slider[0][1]))
    # block_list = block_list.filter(netpower__range=(slider[1][0], slider[1][1]))
    block_list = create_block_list(block_list, filter_dict)
    plant_list = create_block_list(plant_list, filter_dict)

    sources_dict = forge_sources_dict(block_list, "netpower")

    plant_list = plant_list[::1]
    plant_tmp_dict = list(map(model_to_dict, plant_list))
    plant_tmp_list = []

    for plant_dict_entry in plant_tmp_dict:
        plant_list_entry = plant_dict_entry
        plantid = plant_dict_entry["plantid"]
        blocks_list = Blocks.objects.all().filter(plantid=plantid)
        initialop = blocks_list.all().aggregate(Min('initialop'))['initialop__min']
        plant_list_entry["initialop"] = initialop
        plant_tmp_list.append(plant_list_entry)

    value_list = ["plantname", "initialop", "latestexpanded", "state", "federalstate", "totalpower"]
    key_list = ["energysource", "plantid", "plantid"]
    block_dict = create_blocks_dict(plant_tmp_dict, value_list, key_list)

    header_list = ['Kraftwerk', 'Name', 'Inbetriebnahme', 'zuletzt erweitert', 'Status', 'Bundesland', 'Gesamtleistung [in MW]']
    sources_header = ["Energieträger", "Anzahl", "Nennleistung [in MW]", "Jahresproduktion [in TWh]"]
    slider_list = slider
    context = {
        'header_list': header_list,
        'slider': slider_list,
        'form': form,
        'plant_mapper': PLANT_COLOR_MAPPING,
        'block_dict': block_dict,
        'sources_dict': sources_dict,
        'sources_header': sources_header,
        'range': range(2),
    }
    return render(request, 'plantmaster/blocks.html', context)


def plant(request, plantid):

    plant = get_object_or_404(Plants, plantid=plantid)
    blocks = Blocks.objects.filter(plantid=plantid)
    blocks_list = blocks.order_by("initialop" + "")
    plantname = plant.plantname
    block_count = plant.blockcount
    le = plant.latestexpanded
    tp = plant.totalpower

    blocks_tmp_dict = list(map(model_to_dict, blocks_list))
    value_list = ["blockname", "initialop", "endop", "chp", "state", "federalstate", "netpower"]
    key_list = ["energysource", "blockid", "plantid"]
    blocks_of_plant = create_blocks_dict(blocks_tmp_dict, value_list, key_list)

    blocks_header_list = ['BlockID', 'Name', 'Inbetriebnahme', 'Abschaltung', 'KWK', 'Status', 'Bundesland', 'Nennleistung [in MW]']
    data_list = [plantid, plantname, block_count, le, tp]
    header_list = ['KraftwerkID', 'Kraftwerkname', 'Blockzahl', 'zuletzt erweitert', 'Gesamtleistung']
    context = {
        'data_list': zip(header_list, data_list),
        'header_list': blocks_header_list,
        'blocks_of_plant': blocks_of_plant
    }
    return render(request, "plantmaster/plant.html", context)
