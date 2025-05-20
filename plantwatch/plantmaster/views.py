#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .forms import BlocksForm
from .models import Blocks, Plants, Power, Addresses, Pollutions, Yearly #, Monthp, Mtp, Month

from django.db.models import Sum, Min, Avg, Max, Count
from django.db.models import Q, F, When, Case, FloatField
from django.db.models import OuterRef, Subquery

from django.forms.models import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import ListView, DetailView

from functools import reduce
from datetime import date, datetime
import calendar
import json
import random



from .constants import API_KEY, YEARS, PRTR_YEARS, SORT_CRITERIA_PLANTS, SORT_CRITERIA_BLOCKS,\
                        SOURCES_PLANTS, SOURCES_BLOCKS, DEFAULT_OPSTATES
from .builders import initialize_form, get_ss, get_pollutant_dict, get_elist, get_pollutants_any_year,\
                        annotate_plants, forge_sources_plant, forge_sources_dict, query_for_month_many,\
                        get_chart_data_m, get_chart_data_whole_y, get_chart_data_b,\
                        get_percentages_from_yearprod2, get_percentages_from_yearprod3

from .helpers import get_pollutants_from_yearprod3, get_pollutants_chart_data


class BlocksList(ListView):
    model = Blocks
    context_object_name = 'blocks'

    form = ""
    slider = ""

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['form'] = self.form
        context['slider'] = self.slider
        sources_dict = forge_sources_dict(context['blocks'], 'netpower')
        header_list = ['Kraftwerk', 'Block', 'Name', 'Unternehmen', 'Inbetrieb-nahme',
                       'Abschaltung', 'KWK', 'Status', 'Bundesland', 'Nennleistung [MW]']
        context['sources_dict'] = sources_dict
        context['sources_header'] = SOURCES_BLOCKS
        context['header_list'] = header_list
        return context

    def post(self, request, *args, **kwargs):
        form, search_power, search_opstate, search_federalstate, search_chp, sort_method,\
        sort_criteria, slider = initialize_form(self.request, default=SORT_CRITERIA_BLOCKS)

        return super(BlocksList, self).get(request, *args, **kwargs)

    def get_queryset(self):
        form, search_power, search_opstate, search_federalstate, search_chp, sort_method, sort_criteria, slider = initialize_form(self.request, default=SORT_CRITERIA_BLOCKS)
        self.form = form
        self.slider = slider

        blocks = Blocks.objects.filter(initialop__range=(slider[0][0], slider[0][1])).filter(netpower__range=(slider[1][0], slider[1][1])).filter(federalstate__in=search_federalstate).filter(state__in=search_opstate).filter(chp__in=search_chp).filter(energysource__in=search_power).order_by(sort_method + sort_criteria)
        return blocks


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
        header_list = ['Kraftwerk', 'Name', 'Unternehmen', 'Inbetrieb-nahme', 'zuletzt erweitert', 'Status', 'Bundesland', 'Gesamt-leistung [MW]', 'Energie [TWh]', 'CO2 Ausstoß [Mio. t]', 'Auslastung [%]', 'Effizienz [g/kWh]', 'Umsatz [Mio. €]', 'Profit [Mio. €]']
        context['sources_dict'] = sources_dict
        context['sources_header'] = SOURCES_PLANTS
        context['header_list'] = header_list
        comp_plant = self.request.GET.get('plant', '')
        context['plantid'] = context['plants']
        context['comp_plant'] = comp_plant
        return context

    def post(self, request, *args, **kwargs):
        form, search_power, search_opstate, search_federalstate, search_chp, sort_method,\
            sort_criteria, slider = initialize_form(self.request, default=SORT_CRITERIA_PLANTS, plants=True)

        return super(PlantsList, self).get(request, *args, **kwargs)

    def get_queryset(self):
        form, search_power, search_opstate, search_federalstate, search_chp, sort_method, sort_criteria, slider = initialize_form(self.request, default=SORT_CRITERIA_PLANTS, plants=True)
        self.form = form
        self.slider = slider

        if sort_method == '-':
            plants = Plants.objects.filter(initialop__range=(slider[0][0], slider[0][1]))\
                                                        .filter(totalpower__range=(slider[1][0], slider[1][1])).filter(federalstate__in=search_federalstate).filter(state__in=search_opstate)\
                                                        .filter(chp__in=search_chp).filter(energysource__in=search_power)\
                                                        .order_by(F(sort_criteria).desc(nulls_last=True))
        else:
            plants = Plants.objects.filter(initialop__range=(slider[0][0], slider[0][1]))\
                                                        .filter(totalpower__range=(slider[1][0], slider[1][1])).filter(federalstate__in=search_federalstate).filter(state__in=search_opstate)\
                                                        .filter(chp__in=search_chp).filter(energysource__in=search_power)\
                                                        .order_by(F(sort_criteria).asc(nulls_last=True))

        return annotate_plants(plants)


class BlockView(DetailView):

    model = Blocks

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        block = self.object
        address = get_object_or_404(Addresses, blockid=block.blockid)
        try:
            myplantid = block.plantid.plantid
        except:
            myplantid = ""
        data_list = [myplantid, block.blockid, block.blockname, block.company, address.plz, address.place,
                        (address.street or "") + " " + (address.street_number or ""), address.federalstate, block.netpower]
        header_list = ['KraftwerkID', 'BlockID', 'Blockname', 'Unternehmen', 'PLZ',
                        'Ort', 'Anschrift', 'Bundesland', 'Nennleistung']
        context['data_list'] = zip(header_list, data_list)
        return context


class PlantList(ListView):
    model = Blocks
    context_object_name = 'blocks'
    template_name = "plantmaster/plant_list.html"

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)

        plant = get_object_or_404(Plants, pk=self.plantid)

        data_list = [plant.plantid, plant.plantname, plant.company, plant.blockcount,
                        plant.latestexpanded, plant.totalpower, plant.activepower]
        header_list = ['BlockID', 'Kraftwerksname', 'Blockname', 'Inbetriebnahme',
                        'Abschaltung', 'KWK', 'Status', 'Bundesland', 'Nennleistung [in MW]']
        pl_list = ['KraftwerkID', 'Kraftwerkname', 'Unternehmen', 'Blockzahl',
                    'zuletzt erweitert', 'Gesamtleistung', 'Aktive Leistung']
        pol_header_list = ['Schadstoff', 'Jahr', 'Wert', 'Einheit']


        ss = get_ss(plant)

        pollutants_dict = get_pollutant_dict(self.plantid, context['blocks'])
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
        context['plantid'] = self.plantid
        comp_plant = self.request.GET.get('plant', '')
        context['comp_plant'] = comp_plant
        return context

    def get_queryset(self):
        self.plantid = self.kwargs['plantid']
        return Blocks.objects.filter(plantid=self.plantid).order_by('initialop')


class PlantList2(ListView):
    model = Blocks
    context_object_name = 'blocks'
    template_name = "plantmaster/plant_list2.html"

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)

        plant = get_object_or_404(Plants, pk=self.plantid)
        blocks = Blocks.objects.filter(plantid=self.plantid).order_by("initialop" + "")


        data_list = [plant.plantid, plant.plantname, plant.company, plant.blockcount,
                        plant.latestexpanded, plant.totalpower, plant.activepower]
        header_list = ['BlockID', 'Kraftwerksname', 'Blockname', 'Inbetriebnahme',
                        'Abschaltung', 'KWK', 'Status', 'Bundesland', 'Nennleistung [in MW]']
        pl_list = ['KraftwerkID', 'Kraftwerkname', 'Unternehmen', 'Blockzahl',
                    'zuletzt erweitert', 'Gesamtleistung', 'Aktive Leistung']
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

        blocknames = blocks
        guage, percentages, yearprod = [], [], []
        chart_dict = {}

        try:
            power = query_for_month_many(blocknames, "2022", "1")

            powers3 = get_chart_data_m(blocknames, YEARS)
            yearprod = get_chart_data_whole_y(blocknames, YEARS)

            years = YEARS[::-1]
            diaglist = [get_chart_data_b(blocknames, x) for x in years]

            for idx, diag in enumerate(diaglist):
                chart_dict[years[idx]] = diag

            powers2 = diaglist[2]
            percentages = get_percentages_from_yearprod2(yearprod, blocks)

            if power == 0:
                percentages2 = []
            else:
                percentages2 = get_percentages_from_yearprod3(plant)
                guage = [[str(percentages2[0][-1]), percentages2[1][-1]]]
        except KeyError:
            pass

        context['yearprod'] = yearprod
        context['percentages'] = percentages
        context['percentages2'] = percentages2
        context['powers2'] = powers2
        context['powers3'] = powers3
        context['charts'] = chart_dict
        context['guage'] = guage

        return context

    def get_queryset(self):
        self.plantid = self.kwargs['plantid']
        return Blocks.objects.filter(plantid=self.plantid).order_by('initialop')

class PlantList3(ListView):
    model = Blocks
    context_object_name = 'blocks'
    template_name = "plantmaster/plant_list2.html"

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)

        plant = get_object_or_404(Plants, pk=self.plantid)
        blocks = Blocks.objects.filter(plantid=self.plantid).order_by("initialop" + "")


        data_list = [plant.plantid, plant.plantname, plant.company, plant.blockcount,
                        plant.latestexpanded, plant.totalpower, plant.activepower]
        header_list = ['BlockID', 'Kraftwerksname', 'Blockname', 'Inbetriebnahme',
                        'Abschaltung', 'KWK', 'Status', 'Bundesland', 'Nennleistung [in MW]']
        pl_list = ['KraftwerkID', 'Kraftwerkname', 'Unternehmen', 'Blockzahl',
                    'zuletzt erweitert', 'Gesamtleistung', 'Aktive Leistung']
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

        blocknames = blocks
        guage, percentages, yearprod = [], [], []
        chart_dict = {}

        try:
            power = query_for_month_many(blocknames, "2022", "1")

            powers3 = get_chart_data_m(blocknames, YEARS)
            yearprod = get_chart_data_whole_y(blocknames, YEARS)

            years = YEARS[::-1]
            POLS = ["CO2", "NO2", "N2O", "CO", "PM10"]
            diaglist = [get_pollutants_chart_data(self.plantid, pol) for pol in POLS]

            for idx, diag in enumerate(diaglist):
                chart_dict[years[idx]] = diag

            powers2 = diaglist[0]
            percentages = get_percentages_from_yearprod2(yearprod, blocks)

            if power == 0:
                percentages2 = []
            else:
                percentages2 = get_pollutants_from_yearprod3(plant)
                guage = [[str(percentages2[0][-1]), percentages2[1][-1]]]
        except KeyError:
            pass

        context['yearprod'] = yearprod
        context['percentages'] = percentages
        context['percentages2'] = percentages2
        context['powers2'] = powers2
        context['powers3'] = powers3
        context['charts'] = chart_dict
        context['guage'] = guage

        return context

    def get_queryset(self):
        self.plantid = self.kwargs['plantid']
        return Blocks.objects.filter(plantid=self.plantid).order_by('initialop')

class PlantList4(ListView):
    model = Blocks
    context_object_name = 'blocks'
    template_name = "plantmaster/plant_list4.html"

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)

        plant = get_object_or_404(Plants, pk=self.plantid)
        plant2 = get_object_or_404(Plants, pk=self.kwargs['plantid2'])
        data_list = [plant.plantid, plant.plantname, plant.company, plant.blockcount,
                        plant.latestexpanded, plant.totalpower, plant.activepower]
        data_list2 = [plant2.plantid, plant2.plantname, plant2.company, plant2.blockcount,
                        plant2.latestexpanded, plant2.totalpower, plant2.activepower]
        header_list = ['BlockID', 'Kraftwerksname', 'Blockname', 'Inbetriebnahme',
                        'Abschaltung', 'KWK', 'Status', 'Bundesland', 'Nennleistung [in MW]']
        pl_list = ['KraftwerkID', 'Kraftwerkname', 'Unternehmen', 'Blockzahl',
                    'zuletzt erweitert', 'Gesamtleistung', 'Aktive Leistung']
        pol_header_list = ['Schadstoff', 'Jahr', 'Wert', 'Einheit']

        ss = get_ss(plant)

        pollutants_dict = get_pollutant_dict(self.plantid, context['blocks'])
        pollutants_dict2 = get_pollutant_dict(self.kwargs['plantid2'], context['blocks'])
        elist = get_elist(self.plantid, plant)
        elist2 = get_elist(self.kwargs['plantid2'], plant2)

        pollutions2 = get_pollutants_any_year(self.plantid, "Air")
        pollutions3 = get_pollutants_any_year(self.plantid, "Water")
        pollutions4 = get_pollutants_any_year(self.kwargs['plantid2'], "Air")
        pollutions5 = get_pollutants_any_year(self.kwargs['plantid2'], "Water")
        context['plant_id'] = self.plantid
        context['data_list'] = zip(pl_list, data_list)
        context['data_list2'] = zip(pl_list, data_list2)
        context['header_list'] = header_list
        context['rto1'] = 'Luft'
        context['rto2'] = 'Wasser'
        context['ss'] = ss
        context['API'] = API_KEY
        context['pollutions2'] = pollutions2
        context['pollutions3'] = pollutions3
        context['pollutions4'] = pollutions4
        context['pollutions5'] = pollutions5

        context['pollutants_dict'] = pollutants_dict
        context['pollutants_dict2'] = pollutants_dict2
        context['pol_header_list'] = pol_header_list

        context['elist'] = elist
        context['elist2'] = elist2
        context['plantid'] = self.plantid
        comp_plant = self.request.GET.get('plant', '')
        context['comp_plant'] = comp_plant
        return context

    def get_queryset(self):
        self.plantid = self.kwargs['plantid']
        return Blocks.objects.filter(plantid=self.plantid).order_by('initialop')

def random_plant(request):
    i = Plants.objects.filter(state__in=DEFAULT_OPSTATES).filter(totalpower__gte=300)\
                        .filter(Q(energysource="Steinkohle") |
                        Q(energysource="Braunkohle")).all()
    l = len(i)
    random_item = i[random.randint(0, l - 1)]
    return redirect('plant', random_item.plantid)


def impressum(request):
    return render(request, "plantmaster/impressum.html", {})

def compliance(request):
    return render(request, "plantmaster/compliance.html", {})

def widmung(request):
    return render(request, "plantmaster/widmung.html", {})

def enemies(request):
    return render(request, "plantmaster/enemies.html", {})

def friends(request):
    return render(request, "plantmaster/friends.html", {})

def calculations(request):
    return render(request, "plantmaster/calculations.html", {})

def downloads(request):
    return render(request, "plantmaster/downloads.html", {})


