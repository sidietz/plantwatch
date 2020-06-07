#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .forms import BlocksForm
from .models import Blocks, Plants, Power, Addresses, Month, Pollutions, Monthp, Mtp, Yearly

from django.db.models import Sum, Min, Avg, Max, Count
from django.db.models import Q, F, When, Case, FloatField
from django.db.models import OuterRef, Subquery

from django.forms.models import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import ListView

from functools import reduce
from datetime import date, datetime
import calendar
import json
import random


from .helpers import *
from .constants import *
from .builders import *

def blocks(request):
    form, search_power, search_opstate, search_federalstate, search_chp, sort_method, sort_criteria, sliders = initialize_form(request)
    slider = sliders

    block_list = Blocks.objects.filter(initialop__range=(slider[0][0], slider[0][1])).filter(netpower__range=(slider[1][0], slider[1][1])).filter(federalstate__in=search_federalstate).filter(state__in=search_opstate).filter(chp__in=search_chp).order_by(sort_method + sort_criteria)

    sources_dict = forge_sources_dict(block_list, "netpower")

    block_list = block_list[::1]
    block_tmp_dict = list(map(model_to_dict, block_list))
    value_list = ["blockname", "blockdescription", "initialop", "endop", "chp", "state", "federalstate", "netpower"]
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

def impressum(request):
    return render(request, "plantmaster/impressum.html", {})

class PlantsList(ListView):
    model = Plants
    context_object_name = 'plants'

    form = ""
    slider = ""

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['form'] = self.form
        context['slider'] = self.slider
        sources_dict = forge_sources_plant(context['plants'])
        header_list = ['Kraftwerk', 'Name', 'Unternehmen', 'Inbetrieb-nahme', 'zuletzt erweitert', 'Status', 'Bundesland', 'Gesamt-leistung [MW]', 'Energie [TWh]', 'CO2 Ausstoß [Mio. t]', 'Auslastung [%]', 'Effizienz [g/kWh]']
        context['sources_dict'] = sources_dict
        context['sources_header'] = SOURCES_PLANTS
        context['header_list'] = header_list
        return context

    def post(self, request, *args, **kwargs):
        #self.status_form = StatusForm(self.request.POST or None)
        form, search_power, search_opstate, search_federalstate, search_chp, sort_method, sort_criteria, slider = initialize_form(self.request, SORT_CRITERIA=SORT_CRITERIA_PLANTS, plants=True)
        #queryset = queryset.filter(initialop__range=(slider[0][0], slider[0][1])).filter(totalpower__range=(slider[1][0], slider[1][1])).filter(federalstate__in=search_federalstate).filter(state__in=search_opstate).filter(chp__in=search_chp).filter(energysource__in=search_power).order_by(sort_method + sort_criteria)

        return super(PlantsList, self).get(request, *args, **kwargs)

    def get_queryset(self):
        form, search_power, search_opstate, search_federalstate, search_chp, sort_method, sort_criteria, slider = initialize_form(self.request, SORT_CRITERIA=SORT_CRITERIA_PLANTS, plants=True)
        self.form = form
        self.slider = slider

        plants = Plants.objects.order_by('-totalpower').filter(initialop__range=(slider[0][0], slider[0][1])).filter(totalpower__range=(slider[1][0], slider[1][1])).filter(federalstate__in=search_federalstate).filter(state__in=search_opstate).filter(chp__in=search_chp).filter(energysource__in=search_power).order_by(sort_method + sort_criteria)
        return annotate_plants(plants)


def plants(request):
    start = datetime.now()
    form, search_power, search_opstate, search_federalstate, search_chp, sort_method, sort_criteria, slider = initialize_form(request, SORT_CRITERIA=SORT_CRITERIA_PLANTS, plants=True)
    tmp = Plants.objects.filter(initialop__range=(slider[0][0], slider[0][1])).filter(totalpower__range=(slider[1][0], slider[1][1])).filter(federalstate__in=search_federalstate).filter(state__in=search_opstate).filter(chp__in=search_chp).filter(energysource__in=search_power).order_by(sort_method + sort_criteria)
    plc = tmp.count()

    power_type = "totalpower"
    # power_type = "activepower"
    #TODO: make activepower work
    
    tmp3 = annotate_plants(tmp)

    plant_list = tmp3.order_by(sort_method + sort_criteria)

    p, q, z = 1, 2, 3
    q = [1, 2, 3]

    filter_dict = {"energysource": search_power, "state": search_opstate, "federalstate": search_federalstate}
    sources_dict = forge_sources_plant(plant_list)

    block_list = []
    block_dict = {}

    value_list = ["plantname", "initialop", "latestexpanded", "state", "federalstate", "totalpower", "energy", "workload", "efficency"]
    key_list = ["energysource", "plantid", "plantid"]

    header_list = ['Kraftwerk', 'Name', 'Unternehmen', 'Inbetrieb-nahme', 'zuletzt erweitert', 'Status', 'Bundesland', 'Gesamt-leistung [MW]', 'Energie [TWh]', 'CO2 Ausstoß [Mio. t]', 'Auslastung [%]', 'Effizienz [g/kWh]']
    sources_header = SOURCES_PLANTS
    slider_list = slider

    end = datetime.now()
    diff = end - start
    res = [start, end, diff]

    res = []
    context = {
        'header_list': header_list,
        'slider': slider_list,
        'form': form,
        'plant_mapper': PLANT_COLOR_MAPPING,
        'block_dict': {},
        'sources_dict': sources_dict,
        'sources_header': sources_header,
        'plant_list': plant_list,
        'range': range(2),
        'q': q,
        'p': p,
        'z': z,
        'res': res,
    }
    return render(request, 'plantmaster/plants.html', context)

def block(request, blockid):
    block = get_object_or_404(Blocks, blockid=blockid)

    address = get_object_or_404(Addresses, blockid=blockid)
    plant_id = block.plantid.plantid
    error = True if not plant_id else False

    data_list = [plant_id, block.blockid, block.blockname, block.blockdescription, block.company, address.plz, address.place, address.street, address.federalstate, block.netpower]
    header_list = ['PlantID', 'BlockID', 'Plantname', 'Blockname', 'Unternehmen', 'PLZ', 'Ort', 'Anschrift', 'Bundesland', 'Nennleistung']
    context = {
        'data_list': zip(header_list, data_list),
        'plant_id': plant_id,
        'error': error
    }
    return render(request, "plantmaster/block.html", context)

def random_plant(request):
    i = Plants.objects.filter(state__in=DEFAULT_OPSTATES).filter(totalpower__gte=300).filter(Q(energysource="Steinkohle") | Q(energysource="Braunkohle")).all()
    #j = i.filter(totalpower__range(300,5000))
    #items = list(map(lambda x: x.plantid, i))
    l = len(i)

    # change 3 to how many random it/06-05-300-0326774/ems you want
    random_item = i[random.randint(0, l - 1)] #random.sample(i, 1)
    # if you want only a single random item
    return redirect('plant', random_item.plantid)


class PlantList(ListView):
    model = Blocks
    context_object_name = 'blocks'
    template_name = "plantmaster/plant_list.html"

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)

        plant = Plants.objects.get(pk=self.plantid)

        data_list = [plant.plantid, plant.plantname, plant.company, plant.blockcount, plant.latestexpanded, plant.totalpower, plant.activepower]
        header_list = ['BlockID', 'Kraftwerksname', 'Blockname', 'Inbetriebnahme', 'Abschaltung', 'KWK', 'Status', 'Bundesland', 'Nennleistung [in MW]']
        pl_list = ['KraftwerkID', 'Kraftwerkname', 'Unternehmen', 'Blockzahl', 'zuletzt erweitert', 'Gesamtleistung', 'Aktive Leistung']
        pol_header_list = ['Schadstoff', 'Jahr', 'Wert', 'Einheit']


        ss = get_ss(plant)

        pollutants_dict = get_pollutant_dict(self.plantid, blocks)
        elist = get_elist(self.plantid, plant)

        pollutions2 = get_pollutants_any_year(self.plantid, "Air")
        pollutions3 = get_pollutants_any_year(self.plantid, "Water")

        context['plant_id'] = self.plantid
        context['data_list'] = zip(pl_list, data_list)
        context['header_list'] = header_list
        context['rto1'] = 'Luft'
        context['rto2'] = 'Wasser'
        context['ss'] = ss
        context['API'] = API_KEY
        context['pollutions2'] = pollutions2
        context['pollutions3'] = pollutions3

        context['pollutants_dict'] = pollutants_dict
        context['pol_header_list'] = pol_header_list

        context['elist'] = elist

        return context

    def get_queryset(self):
        self.plantid = self.kwargs['plantid']
        return Blocks.objects.filter(plantid=self.plantid).order_by('initialop')

def plant(request, plantid):

    plant = get_object_or_404(Plants, plantid=plantid)
    blocks = Blocks.objects.filter(plantid=plantid)

    monthp = Monthp.objects.filter(plantid=plantid, year=YEAR).aggregate(Sum('power'))
    energies = [get_energy_for_plant(plantid, x) for x in PRTR_YEARS]

    ss3 = get_ss(plant)

    pollutants_dict = get_pollutant_dict(plantid, blocks)
    elist = get_elist(plantid, plant)

    pol_list = ["year", "amount2", "unit2"]
    pk_list = ["year", "pollutant", "amount2"]
    pol_header_list = ['Schadstoff', 'Jahr', 'Wert', 'Einheit']

    blocks_list = blocks.order_by("initialop" + "")
    plantname = plant.plantname
    block_count = plant.blockcount
    le = plant.latestexpanded
    tp = plant.totalpower    

    blocks_tmp_dict = list(map(model_to_dict, blocks_list))
    value_list = ["blockname", "blockdescription", "initialop", "endop", "chp", "state", "federalstate", "netpower"]
    key_list = ["energysource", "blockid", "plantid"]
    blocks_of_plant = create_blocks_dict(blocks_tmp_dict, value_list, key_list)

    blocks_header_list = ['BlockID', 'Kraftwerksname', 'Blockname', 'Inbetriebnahme', 'Abschaltung', 'KWK', 'Status', 'Bundesland', 'Nennleistung [in MW]']
    data_list = [plantid, plantname, plant.company, block_count, le, tp, plant.activepower]
    header_list = ['KraftwerkID', 'Kraftwerkname', 'Unternehmen', 'Blockzahl', 'zuletzt erweitert', 'Gesamtleistung', 'Aktive Leistung']

    pollutions2 = get_pollutants_any_year(plantid, "Air")
    pollutions3 = get_pollutants_any_year(plantid, "Water")

    context = {
        'data_list': zip(header_list, data_list),
        'header_list': blocks_header_list,
        'blocks_of_plant': blocks_of_plant,
        'pollutants_dict': pollutants_dict,
        'pol_header_list': pol_header_list,
        'plant_id': plantid,
        'ss': ss3,
        'elist': elist,
        'energies': energies,
        'API': API_KEY,
        'pollutions2': pollutions2,
        'pollutions3': pollutions3,
        'rtos': ['Luft', "Wasser"],
        'rto1': 'Luft',
        'rto2': 'Wasser'
    }
    return render(request, "plantmaster/plant.html", context)


def plant2(request, plantid):

    plant = get_object_or_404(Plants, plantid=plantid)
    blocks = Blocks.objects.filter(plantid=plantid).order_by("initialop" + "")
    blocks_list = blocks #blocks.order_by("initialop" + "")
    plantname = plant.plantname
    block_count = plant.blockcount
    le = plant.latestexpanded
    tp = plant.totalpower

    power, minp, maxp, avg = 0, 0, 0, 0
    powers = [minp, maxp, avg]
    powers2 = []
    #q = query(blocks[0])

    pivblock = blocks[0]

    #pag = q.aggregate(Sum('power'))
    d = len(blocks)

    m1 = list(range(1,13))
    q = 0
    blocknames = blocks_list#list(map(lambda x: x.blockid, blocks))

    percentages = []
    yearprod = []
    
    powers3 = 0

    guage = []
    chart_dict = {}

    m1 = list(range(1,13))
    
    try:
        
        power = query_for_month_many(blocknames, "2018", "1")

        #powers = get_aggs(q)
        #powers = json.dumps(get_aggs(q))

        powers3 = get_chart_data_m(blocknames, YEARS)
        yearprod = get_chart_data_whole_y(blocknames, YEARS)

        percentages = get_percentages_from_yearprod2(yearprod, blocks)

        if power == 0:
            percentages2 = []
        else:
            percentages2 = get_percentages_from_yearprod3(plant)
            guage = [[str(percentages2[0][-1]), percentages2[1][-1]]]

        years = YEARS[::-1]
        diaglist = [get_chart_data_b(blocknames, x) for x in years]

        #print(diaglist)



        for idx, diag in enumerate(diaglist):
            chart_dict[years[idx]] = diag

        #chartnums = list(range(0, len(diaglist)))

        #print(chart_dict)

        powers2 = diaglist[2]

        # = ["2018"] + list(map(lambda x: query_for_month(pivblock, "2018", x), m1))
        #powers2 = [query_for_month(q, "2018", "1")]
        
        d = len(powers)
    except TypeError:
        d = d

    #Entry.objects.filter(pub_date__date=datetime.date(2005, 1, 1))

    


    mhd = {}

    blocks_tmp_dict = list(map(model_to_dict, blocks_list))
    value_list = ["blockname", "blockdescription", "initialop", "endop", "chp", "state", "federalstate", "netpower"]
    key_list = ["energysource", "blockid", "plantid"]
    blocks_of_plant = create_blocks_dict(blocks_tmp_dict, value_list, key_list)

    blocks_header_list = ['BlockID', 'Kraftwerksname', 'Blockname', 'Inbetriebnahme', 'Abschaltung', 'KWK', 'Status', 'Bundesland', 'Nennleistung [in MW]']
    data_list = [plantid, plantname, block_count, le, tp]
    header_list = ['KraftwerkID', 'Kraftwerkname', 'Blockzahl', 'zuletzt erweitert', 'Gesamtleistung']
    context = {
        'data_list': zip(header_list, data_list),
        'header_list': blocks_header_list,
        'blocks_of_plant': blocks_of_plant,
        'blocknames': blocknames,
        'power' : power,
        'yearprod' : yearprod,
        'percentages': percentages,
        'percentages2': percentages2,
        'powers2' : powers2,
        'powers3' : powers3,
        'charts': chart_dict,
        'guage': guage,
        'plant_id': plantid,
        'q' : q,
        'd' : d,
    }
    return render(request, "plantmaster/plant2.html", context)


