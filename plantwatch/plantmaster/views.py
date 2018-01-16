from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Blocks
from .models import Addresses
from django.db.models import Sum
from django.shortcuts import render
from django.db.models import Q
from .forms import * # SimpleCheckboxForm, SimpleRadioboxForm
from django.views.decorators.csrf import csrf_exempt


FEDERAL_STATES = ['Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg', 'Bremen', 'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern', 'Niedersachsen', 'Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland', 'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']
SOURCES_LIST = ['Erdgas', 'Braunkohle', "Steinkohle", "Kernenergie"]
SORT_CRITERIA =[('netpower', 'Nennleistung'), ('initialop', 'Inbetriebnahme')]


def filter_and(queryset, filtered, filters):
    # print(queryset)
    for afilter in filters:
        queryset = filter_queryset(queryset, filtered, afilter)
        # print(queryset.all().count())
    return queryset


def filter_or(queryset, filtered, filters):
    query_text = "queryset.all().filter("
    for afilter in filters:
        query_text += "Q("
        query_text += "**" + str({filtered: afilter})
        query_text += ") | "

    query_text = query_text[:-3]
    query_text += ")"
    print(query_text)
    queryset = eval(query_text)
    return queryset


def filter_queryset(queryset, filtered, afilter):
    # print(filtered, afilter)
    param = {filtered: afilter}
    new_queryset = queryset.all().filter(**param)
    return new_queryset


def index(request):
    return HttpResponse("test")


def forge_sources_dict(block_list):
    sources_dict = {}
    for source in SOURCES_LIST:
        tmp = filter_or(block_list, "energysource", [source])
        print(tmp)
        power = tmp.all().aggregate(Sum('netpower'))['netpower__sum'] or 0
        power = str(round(power, 2)) + ' MW'
        count = tmp.all().count()
        sources_dict[source] = [count, power]
    power = block_list.all().aggregate(Sum('netpower'))['netpower__sum'] or 0
    power = str(round(power, 2)) + ' MW'
    count = block_list.all().count()
    sources_dict["Summe"] = [count, power]
    return sources_dict


# @csrf_exempt
def blocks(request, lower=1960, upper=2020):

    # if request.method == 'POST':
    #    form =
    sort_criteria = "netpower"
    search_federalstate = []
    search_power = []
    print(search_federalstate)
    if request.method == 'POST':
        form = BlocksForm(request.POST)
        # form1 = SimpleRadioboxForm(request.POST)
        # form2 = SimpleCheckboxForm(request.POST)
        sort_criteria = request.POST.get('simple_radiobox', "netpower")
        search_federalstate = request.POST.getlist('simple_checkbox', [])
        search_power = request.POST.getlist('power_checkbox', [])
        # print("Success")
        # render(request, 'index.html', context)
    else:
        form = BlocksForm()
        # form1 = SimpleRadioboxForm()
        # form2 = SimpleCheckboxForm()
        # form2.fields['test'].choices = zip()
        # formset = SimpleFormset(form_kwargs={'choices': ''})
        # print("Failure")

    print("search federalstate")
    print(search_federalstate)
    form.fields['simple_checkbox'].choices = list(zip(FEDERAL_STATES, FEDERAL_STATES))
    form.fields['simple_checkbox'].initial = search_federalstate# or FEDERAL_STATES
    form.fields['simple_radiobox'].choices = SORT_CRITERIA
    form.fields['simple_radiobox'].initial = sort_criteria or SORT_CRITERIA
    form.fields['power_checkbox'].initial = search_power or SOURCES_LIST
    form.fields['power_checkbox'].choices = list(zip(SOURCES_LIST, SOURCES_LIST))
    if not search_power:
        search_power = SOURCES_LIST


    print(SOURCES_LIST)
    print(search_power)
    queries = search_power
    print(queries)
    states = ["in Betrieb", "Sonderfall", "Gesetzlich an Stilllegung gehindert"]
    block_list = Blocks.objects.order_by('-' + sort_criteria)
    print(block_list)
    # feds = Blocks.objects.values("federalstate")
    # print(feds)
    # feds_l = list(map(lambda x: list(x.values())[0], feds))
    # feds_set = set(feds_l)
    # feds_r = list(feds_set)
    # print(list(feds))
    # print(feds_r)
    print("By energy source")
    block_list = filter_or(block_list, "energysource", queries)
    print(queries)
    print("By state")
    block_list = filter_or(block_list, "state", states)
    if search_federalstate:
        print("By federalstate")
        block_list = filter_or(block_list, "federalstate", search_federalstate)
    # print(block_list)
    block_list = block_list.filter(initialop__range=(lower, upper))

    sources_dict = forge_sources_dict(block_list)
    print(sources_dict)

    header_list = ['BlockId', 'Name', 'Inbetriebnahme', 'Status', 'Bundesland', 'Nennleistung']
    # template = loader.get_template('plantmaster/blocks.html')
    sources_header = ["Energieträger", "Anzahl", "Nennleistung"]
    context = {
        'header_list': header_list,
        'upper': upper,
        'lower': lower,
        'form': form,
        'block_list': block_list,
        'sources_dict': sources_dict,
        'sources_header': sources_header
    }
    # options=[('netpower', 'Nennleistung'), ('initialop', 'Inbetriebnahme')]
    # context['form1'] = form1
    # print(context)
    # print(context)
    return render(request, 'plantmaster/blocks.html', context)


def block(request, blockid):
    block = Blocks.objects.get(blockid=blockid)
    address = Addresses.objects.get(blockid=blockid)
    data_list = [address.blockid.blockname, address.plz, address.place, address.street, address.federalstate, block.netpower]
    # print(data_list)
    header_list = ['Name', 'PLZ', 'Ort', 'Anschrift', 'Bundesland', 'Nennleistung']
    context = {
        'data_list': zip(header_list, data_list),
    }
    return render(request, "plantmaster/block.html", context)


def impressum(request):
    return render(request, "plantmaster/impressum.html", {})


# def plants(request):
#    return render(request, "plantmaster/plants.html", {})


def plants(request):
    context = {}
    return render(request, "plantmaster/plants.html", context)


def plant(request, plantid):
    return render(request, "plantmaster/plant.html", {})
