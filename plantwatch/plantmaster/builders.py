from django.db.models import Sum, Min, Avg, Max, Count
from django.db.models import Q, F, When, Case, FloatField

from django.forms.models import model_to_dict

import re
from functools import reduce

from .forms import BlocksForm
from .models import Blocks, Plants, Power, Addresses, Month, Pollutions, Monthp, Mtp, Yearly
from .helpers import divide_safe, get_ss, get_pollutants_any_year, query_for_month_many, get_chart_data_m, get_chart_data_whole_y, get_chart_data_b, get_percentages_from_yearprod2, get_percentages_from_yearprod3, handle_slider, handle_slider_1, handle_slider_2, calc_workload, get_pollutants, get_co2_for_plant_by_year, get_energy_for_plant, get_co2_for_plant_by_years
from .constants import API_KEY, SORT_CRITERIA_BLOCKS, SLIDER_1, SLIDER_2p, SLIDER_2b, DEFAULT_OPSTATES, SELECT_CHP, SELECT_CHP_LIST, FEDERAL_STATES, SOURCES_LIST, OPSTATES, HOURS_IN_YEAR, YEAR, LATEST_YEAR, YEARS, ACTIVE_OPS

def fill_field(form, by, entries):

    if len(entries) == 3:
        form.fields[by].choices = entries[2]
    form.fields[by].initial = entries[0]
    form.fields[by].label = entries[1]
    return

def initialize_form(request, sort_criteria_default=SORT_CRITERIA_BLOCKS, plants=False):
    slider1 = SLIDER_1

    if plants:
        sl2 = SLIDER_2p
    else:
        sl2 = SLIDER_2b
    slider2 = sl2
    sort_criteria = sort_criteria_default[1]
    sort_method = "-"
    search_federalstate = []
    search_power = ['Braunkohle', "Steinkohle", "Kernenergie", "Mineralölprodukte", "Erdgas"]
    search_opstate = DEFAULT_OPSTATES
    search_chp = []

    if request.method == 'POST':
        form = BlocksForm(request.POST)
        sort_criteria = request.POST.get('sort_by', sort_criteria_default[1])
        search_federalstate = request.POST.getlist('select_federalstate', [])
        search_power = request.POST.getlist('select_powersource', [])
        search_opstate = request.POST.getlist('select_opstate', DEFAULT_OPSTATES)
        search_chp = request.POST.getlist('select_chp', [])
        slider1 = request.POST.get('slider1', SLIDER_1)
        slider2 = request.POST.get('slider2', sl2)
        sort_method = request.POST.get('sort_method', sort_method)
    else:
        form = BlocksForm()

    fill_field(form, 'sort_by', [sort_criteria or sort_criteria_default[1], "Sortiere nach:", sort_criteria_default[0]])
    fill_field(form, 'sort_method', [sort_method, "aufsteigend oder absteigend?", [('-', 'absteigend'), ('', 'aufsteigend')]])
    fill_field(form, 'select_chp', [search_chp or SELECT_CHP_LIST, "Filtere nach Kraft-Wärme-Kopplung:", SELECT_CHP])
    fill_field(form, 'select_federalstate', [search_federalstate, "Filtere nach Bundesland:", list(zip(FEDERAL_STATES, FEDERAL_STATES))])
    fill_field(form, 'select_powersource', [search_power or SOURCES_LIST, "Filtere nach Energieträger:", list(zip(SOURCES_LIST, SOURCES_LIST))])
    fill_field(form, 'select_opstate', [search_opstate or ['in Betrieb', 'Gesetzlich an Stilllegung gehindert', 'Netzreserve', 'Sicherheitsbereitschaft', 'Sonderfall'], "Filtere nach Betriebszustand:", list(zip(OPSTATES, OPSTATES))])
    fill_field(form, 'slider1', [slider1, "Filtere nach Zeitraum"])
    fill_field(form, 'slider2', [slider2, "Filtere nach Nennleistung"])

    if not search_power:
        search_power = SOURCES_LIST
    if not search_opstate:
        search_opstate = ["in Betrieb", "Sonderfall", "Gesetzlich an Stilllegung gehindert"]
    if not search_chp:
        search_chp = ["Nein", "Ja", ""]
    if not search_federalstate:
        search_federalstate = FEDERAL_STATES

    slider_1 = handle_slider_1(re.escape(slider1))
    slider_2 = handle_slider_2(re.escape(slider2), plants)
    return form, search_power, search_opstate, search_federalstate, search_chp, sort_method, sort_criteria, [slider_1, slider_2]


def forge_sources_dict(block_list, power_type):

    sources_dict = {}
    whole_power, whole_power2 = 0, 0
    factors = []
    for source in SOURCES_LIST:
        tmp = block_list.filter(energysource=source)
        count = tmp.all().count()
        raw_power = tmp.all().aggregate(Sum(power_type))[power_type + '__sum'] or 0
        raw_energy = Month.objects.filter(blockid__in=tmp, year=YEAR, month__in=list(range(1,13))).aggregate(Sum("power"))['power__sum'] or 0
        energy = raw_energy / 10**6

        factor = divide_safe(raw_energy, raw_power)

        raw_energy2 = Month.objects.filter(blockid__in=tmp, year=LATEST_YEAR, month__in=list(range(1,13))).aggregate(Sum("power"))['power__sum'] or 0
        energy2 = raw_energy2 / 10**6
        workload = calc_workload(raw_energy * 10000, raw_power)
        workload2 = calc_workload(raw_energy2 * 10000, raw_power)
        factors.append(factor)
        power = round(raw_power / 1000, 2)
        anual_power = round((raw_power * factor) / (10**6), 2)
        whole_power += energy
        whole_power2 += energy2

        sources_dict[source] = [count, power, round(energy, 2), round(factor, 2), round(workload, 2), round(workload2, 2)]
    power_c = block_list.all().aggregate(Sum(power_type))[power_type + '__sum'] or 1
    power = round(power_c / 1000, 2)
    count = block_list.all().count()
    sources_dict["Summe"] = [count, power, round(whole_power, 2), round(divide_safe(whole_power * 10000, raw_power), 2), round(calc_workload(whole_power * 10**10, power_c), 2), round(calc_workload(whole_power2 * 10**10, power_c), 2)]
    return sources_dict

def forge_sources_plant(annotated_plants):

    sources_dict = {}
    energy, energy2 = 0, 0

    total_power = 0
    total_energy = 0
    total_co2 = 0
    total_count = 0

    for source in SOURCES_LIST:
        # TODO: introduce effective power besides totalpower
        # TODO: show in plant active and inactive plants, separately
        filtered = annotated_plants.filter(energysource=source)
        count = filtered.count()
        effective_power = filtered.aggregate(Sum('totalpower'))['totalpower__sum'] or 0
        energy = filtered.aggregate(Sum('energy_2018'))['energy_2018__sum'] or 0
        co2 = filtered.aggregate(Sum('co2_2018'))['co2_2018__sum'] or 0
        workload = calc_workload(energy, effective_power)
        ophours = divide_safe(energy, effective_power)
        efficiency = divide_safe(co2, energy)

        total_power += effective_power
        total_energy += energy
        total_co2 += co2
        total_count += count
    
        sources_dict[source] = [count, effective_power / 1000, energy / 10**6, co2 / 10**9, ophours, workload * 10000, efficiency]
    
    sources_dict['Summe'] = [total_count, total_power / 1000, total_energy / 10**6, total_co2 / 10**9, divide_safe(total_energy, total_power), calc_workload(total_energy, total_power) * 10000, divide_safe(total_co2, total_energy)]
    return sources_dict

def annotate_plants(plants):

    power_type = "totalpower"
    plants2 = plants.all().annotate(
    eff15=Case(
        When(energy_2015=0, then=0),
        When(co2_2015=0, then=0),
        default=(F('co2_2015') / F('energy_2015')), output_field=FloatField()),
    eff16=Case(
        When(energy_2016=0, then=0),
        When(co2_2016=0, then=0),
        default=(F('co2_2016') / F('energy_2016')), output_field=FloatField()),
    eff17=Case(
        When(energy_2017=0, then=0),
        When(co2_2017=0, then=0),
        default=(F('co2_2017') / F('energy_2017')), output_field=FloatField()),
    eff18=Case(
        When(energy_2018=0, then=0),
        When(co2_2018=0, then=0),
        default=(F('co2_2018') / F('energy_2018')), output_field=FloatField()),
    eff=Case(
        When(energy_2018=0, then=0),
        When(co2_2018=0, then=0),
        default=(F('co2_2018') / F('energy_2018')), output_field=FloatField()),
    workload15=Case(
        When(energy_2015=0, then=0),
        default=(F('energy_2015') / (F(power_type) * HOURS_IN_YEAR) * 100), output_field=FloatField()),
    workload16=Case(
        When(energy_2016=0, then=0),
        default=(F('energy_2016') / (F(power_type) * HOURS_IN_YEAR) * 100), output_field=FloatField()),
    workload17=Case(
        When(energy_2017=0, then=0),
        default=(F('energy_2017') / (F(power_type) * HOURS_IN_YEAR) * 100), output_field=FloatField()),
    workload18=Case(
        When(energy_2018=0, then=0),
        default=(F('energy_2018') / (F(power_type) * HOURS_IN_YEAR) * 100), output_field=FloatField()),
    workload19=Case(
        When(energy_2019=0, then=0),
        default=(F('energy_2019') / (F(power_type) * HOURS_IN_YEAR) * 100), output_field=FloatField()),
    workload=Case(
        When(energy_2019=0, then=0),
        default=(F('energy_2019') / (F(power_type) * HOURS_IN_YEAR) * 100), output_field=FloatField()),
    energy=Case(
        When(energy_2018=0, then=0),
        default=(F('energy_2018') / float(10**6)), output_field=FloatField()),
    co2=Case(
        When(co2_2018=0, then=0),
        default=(F('co2_2018') / float(10**9)), output_field=FloatField()),
    )

    return plants2

def create_blocks_dict(block_tmp_dict, value_list, key_list):
    block_dict = {}

    for entry in block_tmp_dict:
        key = []
        for a_key in key_list:
            key.append(entry[a_key])
        value = []
        for element in value_list:
            value.append(entry[element])
            block_dict[tuple(key)] = value
    return block_dict

def get_pollutant_dict(plantid, blocks):
    try:
        year, pollutions = get_pollutants(plantid)
    except TypeError:
        return {}
    co2 = get_co2_for_plant_by_year(plantid, year)
    energy = get_energy_for_plant(plantid, year)
    pollutants_tmp_dict = list(map(model_to_dict, pollutions))
    pol_list = ["year", "amount2", "unit2"]
    pk_list = ["year", "pollutant", "amount2"]
    pollutants_dict = create_blocks_dict(pollutants_tmp_dict, pol_list, pk_list)
    return pollutants_dict

def get_activepower(blocks):
    powers = []

    for x in YEARS:
        activeblocks = blocks.filter(Q(state__in=ACTIVE_OPS[0:2]) | (Q(state=ACTIVE_OPS[2]) & Q(reserveyear__gt=x) | ((Q(state="stillgelegt") & Q(endop__gt=x)))))
        activepower = activeblocks.aggregate(Sum('netpower'))['netpower__sum'] or 0 # if plant is retired
        powers.append(activepower)

    return powers


def get_elist(plantid, plant):

    elist = []

    blocks = Blocks.objects.filter(plantid=plantid)

    powers = get_activepower(blocks)

    energies = [get_energy_for_plant(plantid, x) for x in YEARS]
    e2s = [get_energy_for_plant(plantid, x, raw=True) for x in YEARS]
    co2s = get_co2_for_plant_by_years(plantid, YEARS)
    co2s = [get_co2_for_plant_by_year(plantid, x) for x in YEARS]
    tmp = list(zip(co2s, energies))
    effs = [divide_safe(x, y) * 10**3 for x, y in tmp]
    workload2 = [divide_safe(e, (plant.totalpower * HOURS_IN_YEAR)) * 100 for e in e2s]
    workload = [divide_safe(e, (p * HOURS_IN_YEAR)) * 100 for (e, p) in zip(e2s, powers)]

    effcols = list(zip(YEARS, energies, co2s, effs, workload, workload2))
    testval = reduce(lambda a, b: a + b, [i for col in effcols for i in col[1:]])

    # all rows empty, so return emptylist
    if testval == 0:
        return elist
    else:
        return [["Jahr", "Energie TWh", "CO2 [Mio. t.]", "g/kWh", "Auslastung aktive Blöcke [%]", "Auslastung gesamt [%]"], effcols]

