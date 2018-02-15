#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from .models import *
from django.db.models import Sum
from django.shortcuts import render
from django.db.models import Q
from django.forms.models import model_to_dict
from .forms import *
from functools import reduce
from collections import OrderedDict


FEDERAL_STATES = ['Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg', 'Bremen', 'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern', 'Niedersachsen', 'Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland', 'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']
SOURCES_LIST = ['Erdgas', 'Braunkohle', "Steinkohle", "Kernenergie"]
SORT_CRITERIA =[('netpower', 'Nennleistung'), ('initialop', 'Inbetriebnahme')]
OPSTATES = ['Sonderfall', 'Sicherheitsbereitschaft', 'Gesetzlich an Stilllegung gehindert', 'vorläufig stillgelegt', 'stillgelegt', 'in Betrieb']
SELECT_CHP = [("Nein", "keine Kraft-Wärme-Kopplung"), ("Ja", "Kraft-Wärme-Kopplung"), ("", "unbekannt")]
SELECT_CHP_LIST = ["Ja", "Nein", ""]
SOURCES_DICT = {'Erdgas': 1220, 'Braunkohle': 6625, "Steinkohle": 3000, "Kernenergie": 6700}


def filter_and(queryset, filtered, filters):
    for afilter in filters:
        queryset = filter_queryset(queryset, filtered, afilter)
    return queryset


def filter_or(queryset, filtered, filters):
    # Thanks to https://stackoverflow.com/questions/852414/how-to-dynamically-compose-an-or-query-filter-in-django
    query = reduce(lambda q, value: q | Q(**{filtered: value}), filters, Q())
    queryset = queryset.all().filter(query)
    return queryset


def filter_queryset(queryset, filtered, afilter):
    param = {filtered: afilter}
    new_queryset = queryset.all().filter(**param)
    return new_queryset


def forge_sources_dict(block_list):
    sources_dict = {}
    whole_power = 0
    for source in SOURCES_LIST:
        tmp = filter_or(block_list, "energysource", [source])
        factor = SOURCES_DICT[source]
        # print(tmp)
        raw_power = tmp.all().aggregate(Sum('netpower'))['netpower__sum'] or 0
        power = round(raw_power, 2)
        anual_power = round((raw_power * factor) / (10**6), 2)
        whole_power += anual_power
        count = tmp.all().count()
        sources_dict[source] = [count, power, anual_power]
    power = block_list.all().aggregate(Sum('netpower'))['netpower__sum'] or 0
    power = round(power, 2)
    count = block_list.all().count()
    whole_power = round(whole_power, 2)
    sources_dict["Summe"] = [count, power, whole_power]
    return sources_dict


def create_low_up(lowup):
    return lowup.split(';')


'''
def initialize_fields(form_list):
    form_dict = {}
    for form in form_list:
        form_dict[form[0]] = 
    return
'''

'''

    form_list = [['sort_criteria', 'getlist', 'sort_by', 'netpower'],
    ['search_federalstate', 'getlist', 'select_federalstate', []],
    ['search_power', 'getlist', 'select_powersource', []],
    ['search_opstate', 'getlist', 'select_opstate', []],
    ['search_chp', 'getlist', 'select_chp', []],
    ['slider1', 'get', 'slider1', "1960;2020"],
    ['sort_method', 'get', 'sort_method', sort_method]]
'''


def blocks(request):

    sort_criteria = "initialop"
    sort_method = ""
    search_federalstate = []
    search_power = []
    search_opstate = []
    search_chp = []
    slider1 = "1960;2020"

    if request.method == 'POST':
        form = BlocksForm(request.POST)
        sort_criteria = request.POST.get('sort_by', "netpower")
        search_federalstate = request.POST.getlist('select_federalstate', [])
        search_power = request.POST.getlist('select_powersource', [])
        search_opstate = request.POST.getlist('select_opstate', [])
        search_chp = request.POST.getlist('select_chp', [])
        slider1 = request.POST.get('slider1', "1960;2020")
        sort_method = request.POST.get('sort_method', sort_method)
    else:
        form = BlocksForm()

    form.fields['sort_by'].choices = SORT_CRITERIA
    form.fields['sort_by'].initial = sort_criteria or "netpower"
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
    form.fields['select_opstate'].initial = search_opstate or ["in Betrieb", "Sonderfall", "Gesetzlich an Stilllegung gehindert"]
    form.fields['select_opstate'].label = "Filtere nach Betriebszustand:"

    form.fields['slider1'].initial = "1960;2020"
    form.fields['slider1'].label = "Filtere nach Zeitraum"
    lower, upper = create_low_up(slider1)

    if not search_power:
        search_power = SOURCES_LIST
    if not search_opstate:
        search_opstate = ["in Betrieb", "Sonderfall", "Gesetzlich an Stilllegung gehindert"]
    if not search_chp:
        search_chp = ["Nein", "Ja", ""]
    if not search_federalstate:
        search_federalstate = FEDERAL_STATES

    block_list = Blocks.objects.order_by(sort_method + sort_criteria)
    block_list = filter_or(block_list, "energysource", search_power)
    block_list = filter_or(block_list, "state", search_opstate)

    if search_federalstate:
        block_list = filter_or(block_list, "federalstate", search_federalstate)

    block_list = filter_or(block_list, "chp", search_chp)
    block_list = block_list.filter(initialop__range=(lower, upper))

    sources_dict = forge_sources_dict(block_list)

    block_list = block_list[::1]
    block_tmp_dict = list(map(model_to_dict, block_list))
    block_dict = create_blocks_dict(block_tmp_dict)

    header_list = ['Kraftwerk','Block', 'Name', 'Inbetriebnahme', 'Abschaltung', 'KWK', 'Status', 'Bundesland', 'Nennleistung [in MW]']
    sources_header = ["Energieträger", "Anzahl", "Nennleistung [in MW]", "Jahresproduktion [in TWh]"]
    context = {
        'header_list': header_list,
        'upper': upper,
        'lower': lower,
        'form': form,
        'block_dict': block_dict,
        'sources_dict': sources_dict,
        'sources_header': sources_header,
        'range': range(2),
    }
    return render(request, 'plantmaster/blocks.html', context)


def create_blocks_dict(block_tmp_dict):
    block_dict = {}
    value_list = ["blockname", "initialop", "endop", "chp", "state", "federalstate", "netpower"]
    for entry in block_tmp_dict:
        key = (entry["energysource"], entry["blockid"], entry["plantid"])
        value = []
        for element in value_list:
            value.append(entry[element])
        block_dict[key] = value
    return block_dict


def block(request, blockid):
    address = Addresses.objects.get(blockid=blockid)
    block = Blocks.objects.get(blockid=blockid)
    try:
        plant_id = block.plantid.plantid
    except Plants.DoesNotExist:
        plant_id = None
    data_list = [plant_id, block.blockname, address.plz, address.place, address.street, address.federalstate, block.netpower]

    header_list = ['PlantID', 'Name', 'PLZ', 'Ort', 'Anschrift', 'Bundesland', 'Nennleistung']
    context = {
        'data_list': zip(header_list, data_list),
        'plant_id': plant_id,
    }
    return render(request, "plantmaster/block.html", context)


def impressum(request):
    return render(request, "plantmaster/impressum.html", {})


def plants(request):
    context = {
    }
    return render(request, "plantmaster/plants.html", context)


def create_plant_dict(blocks_tmp_dict):
    blocks_of_plant = OrderedDict
    for ablock in blocks_tmp_dict:
        key = ablock["blockid"]
        value = create_blocks_dict(ablock)
        blocks_of_plant[key] = value
    return blocks_of_plant


'''
def create_blocks_tmp_dict(blocks_list):
    blocks_tmp_dict = []
    for ablock in blocks_list:
        print(ablock)
        blocks_tmp_dict.append(list(map(model_to_dict, ablock)))
    return blocks_tmp_dict
'''


def plant(request, plantid):
    try:
        plant = Plants.objects.get(plantid=plantid)
        blocks = plant.blocks_set.all()
        blocks_list = blocks.order_by("initialop" + "")
        plantname = plant.plantname
        block_count = plant.blockcount
        le = plant.latestexpanded
        tp = plant.totalpower
    except Plants.DoesNotExist:
        try:
            blocks = Blocks.objects.get(plantid=plantid)
            plantname = blocks.blockname
            block_count = 1
            le = blocks.initialop
            tp = blocks.netpower
            blocks_list = [blocks]
        except:
            blocks = Blocks.objects.filter(plantid=plantid).all()
            plantname = blocks.first().blockname
            blocks_list = blocks.order_by("initialop" + "")
            block_count = len(blocks_list)
            le = 1990
            tp = 500

    blocks_tmp_dict = list(map(model_to_dict, blocks_list))
    blocks_of_plant = create_blocks_dict(blocks_tmp_dict)

    blocks_header_list = ['BlockID', 'Name', 'Inbetriebnahme', 'Abschaltung', 'KWK', 'Status', 'Bundesland', 'Nennleistung [in MW]']
    data_list = [plantid, plantname, block_count, le, tp]
    header_list = ['KraftwerkID', 'Kraftwerkname', 'Blockzahl', 'zuletzt erweitert', 'Gesamtleistung']
    context = {
        'data_list': zip(header_list, data_list),
        'header_list': blocks_header_list,
        'blocks_of_plant': blocks_of_plant
    }
    return render(request, "plantmaster/plant.html", context)

