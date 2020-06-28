from .models import Pollutions, Month, Yearly
from django.db.models import Sum, Min, Avg, Max, Count

from django.core.exceptions import ObjectDoesNotExist

from .constants import HOURS_IN_YEAR, PRTR_YEARS, SL_1, SL_2p, SL_2b, YEARS


def divide_safe(n, d):
    return n / d if d else 0


def calc_workload(energy, power):
    return divide_safe(energy, (power * HOURS_IN_YEAR) * 100)


def calc_efficency(co2, energy):
    return divide_safe(co2, energy) * 10**3


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
    return new_slider


def query_for_month_many(blocks, year, month):
    q = Month.objects.filter(blockid__in=blocks)
    power = q.filter(year=year, month=month)\
                    .aggregate(Sum("power"))['power__sum']
    return power or 0


def query_for_year(blockid, year):
    q = Month.objects.filter(blockid=blockid)
    power = q.filter(year=year).aggregate(Sum("power"))['power__sum']
    return power or 0


def get_aggs(q):
    minimum = q.aggregate(Min("power"))['power__min']
    maximum = q.aggregate(Max("power"))['power__max']
    avg = q.aggregate(Avg("power"))['power__avg']
    return ["power", minimum, maximum, avg]


def get_for_year(q, year):
    power = q.filter(producedat__year=year)

    return power


def gen_row_m(blocknames, year):
    m1 = list(range(1, 13))
    return list(map(lambda x: query_for_month_many(blocknames, year, x), m1))


def gen_row_y(blocknames, year):
    return list(map(lambda x: query_for_year(x, year), blocknames))


def get_chart_data_m(blocknames, years):
    powers = []
    for i in years:
        p = [i] + gen_row_m(blocknames, i)
        powers.append(p)
    return powers


def get_chart_data_b(blocknames, year):
    powers = []
    for block in blocknames:
        p = [block.blockid] + gen_row_m([block], year)
        powers.append(p)
    return powers


def get_chart_data_whole_y2(blocknames, year):
    powers = []
    for block in blocknames:
        p = [block.blockid] + gen_row_y([block], year)
        powers.append(p)
    return powers


def get_chart_data_whole_y(blocknames, years):
    head = ["x"] + years
    powers = [head]
    for block in blocknames:
        p = [block.blockid] + [gen_row_y([block], year) for year in years]
        powers.append(p)
    return powers


def get_chart_data_y(blocknames, years):

    powers = []
    for i in years:
        p = [i] + gen_row_y(blocknames, i)
        powers.append(p)
    return powers


def get_percentages_from_yearprod3(plant):

    energies = [get_energy_for_plant(plant, x, raw=True) for x in YEARS]
    workloads = [divide_safe(e,
                        (plant.totalpower * HOURS_IN_YEAR)) * 100 for e in energies]
    workloads.insert(0, plant.plantid)
    result = [workloads]

    head = ['x'] + YEARS
    result.insert(0, head)

    return result


def get_percentages_from_yearprod2(yearprod, blocks):

    data = yearprod[1:]
    blocks_str = [x[0] for x in data]
    vals = [x[1:] for x in data]

    block_power = [block.netpower for block in blocks]
    percentage = [[[value[0] * 100 / (HOURS_IN_YEAR * block_power[idx])]
                    for value in entry] for idx, entry in enumerate(vals)]
    blocks_percs = [[[blocks_str[idx]] + entry] for idx,
                        entry in enumerate(percentage)]

    result = [x[0] for x in blocks_percs]
    blocks_str.insert(0, 'x')

    head = yearprod[0]
    result.insert(0, head)

    return result


def get_energy_for_plant(plantid, year, raw=False):
    try:
        tmp = Yearly.objects.filter(plantid=plantid, year=year)\
                                .aggregate(Sum('power'))['power__sum'] or 0
    except KeyError:
        tmp = 0.001

    if raw:
        return tmp
    else:
        return tmp / 10**6 or 0


def get_co2_for_plant_by_years(plantid, years):
    pols = Pollutions.objects.filter(plantid=plantid, releasesto="Air",
                                        pollutant="CO2", year__in=years).order_by("year")
    co2s = list(map(lambda x: x.amount2, pols))

    return co2s


def get_co2_for_plant_by_year(plantid, year):
    try:
        co2 = Pollutions.objects.get(plantid=plantid, releasesto="Air",
                                        pollutant="CO2", year=year).amount2
    except ObjectDoesNotExist:
        co2 = 0
    return co2


def get_company(company):

    tmp = company.replace("Kraftwerk", "").strip()
    tmp = tmp.replace("Stadtwerke", "").strip()

    cl = tmp.split(" ")
    l = len(cl)
    if l == 1:
        return company
    elif l > 1:
        return "" if "niper" in company else "RWE Power" if "RWE" in company else cl[0]
    else:
        return ""


def get_plantname(plantname):
    tmp = plantname.replace("HKW", "").strip()  # or replace("Kraftwerk", "").strip()?
    l = len(tmp)

    if l < 4:
        return tmp if "GKM" in tmp else ""
    else:
        return tmp


def get_co2(plantid):
    for year in PRTR_YEARS[::-1]:
        try:
            q = Pollutions.objects.get(plantid=plantid, year=year,
                                        releasesto='Air', pollutant="CO2")
            break
        except ObjectDoesNotExist:
            pass
    return q


def get_pollutants(plantid, year=''):
    #TODO: fix to display least recent pollutant year instead of fixed year
    if year:
        return Pollutions.objects.filter(plantid=plantid, year=year, releasesto='Air')\
                                    .order_by("-exponent", "-amount")

    for year in PRTR_YEARS[::-1]:
        q = Pollutions.objects.filter(plantid=plantid, year=year, releasesto='Air')\
                                        .order_by("-exponent", "-amount")
        if q.exists():
            return year, q


def get_pollutants_any_year(plantid, to):
    q = Pollutions.objects.filter(plantid=plantid, releasesto=to).order_by("-exponent", "pollutant2", "year", "-amount")
    return q


def get_ss(plant):
    pltn, comp = get_plantname(plant.plantname), get_company(plant.company)
    ks = " Kraftwerk " if "raftwerk" not in pltn else pltn
    ss3 = comp + ks + pltn
    ss3 = plant.plantname.replace("Werk", "")\
                            if "P&L" in plant.plantname else ss3
    ss3 = ss3.replace(" ", "+")
    ss3 = ss3.replace("&", "%26")
    return ss3
