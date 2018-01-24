from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Blocks
from .models import Addresses
from django.db.models import Sum
from django.shortcuts import render
from django.db.models import Q
from django.forms.models import model_to_dict
from .forms import *  # SimpleCheckboxForm, SimpleRadioboxForm
from django.views.decorators.csrf import csrf_exempt


FEDERAL_STATES = ['Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg', 'Bremen', 'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern', 'Niedersachsen', 'Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland', 'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']
SOURCES_LIST = ['Erdgas', 'Braunkohle', "Steinkohle", "Kernenergie"]
SORT_CRITERIA =[('netpower', 'Nennleistung'), ('initialop', 'Inbetriebnahme')]
OPSTATES = ['Sonderfall', 'Sicherheitsbereitschaft', 'Gesetzlich an Stilllegung gehindert', 'vorläufig stillgelegt', 'stillgelegt', 'in Betrieb']
SELECT_CHP = [("Nein", "keine Kraft-Wärme-Kopplung"), ("Ja", "Kraft-Wärme-Kopplung"), ("", "unbekannt")]
SELECT_CHP_LIST = ["Ja", "Nein", ""]


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
    # print(query_text)
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
        # print(tmp)
        power = tmp.all().aggregate(Sum('netpower'))['netpower__sum'] or 0
        power = str(round(power, 2)) + ' MW'
        count = tmp.all().count()
        sources_dict[source] = [count, power]
    power = block_list.all().aggregate(Sum('netpower'))['netpower__sum'] or 0
    power = str(round(power, 2)) + ' MW'
    count = block_list.all().count()
    sources_dict["Summe"] = [count, power]
    return sources_dict


def create_low_up(lowup):
    return lowup.split(';')


# @csrf_exempt
def blocks(request):

    # if request.method == 'POST':
    #    form =
    sort_criteria = "netpower"
    sort_method = "-"
    search_federalstate = []
    search_power = []
    search_opstate = []
    search_chp = []
    slider1 = "1960;2020"
    # print(search_federalstate)
    if request.method == 'POST':
        form = BlocksForm(request.POST)
        # form1 = SimpleRadioboxForm(request.POST)
        # form2 = SimpleCheckboxForm(request.POST)
        sort_criteria = request.POST.get('sort_by', "netpower")
        search_federalstate = request.POST.getlist('select_federalstate', [])
        search_power = request.POST.getlist('select_powersource', [])
        search_opstate = request.POST.getlist('select_opstate', [])
        search_chp = request.POST.getlist('select_chp', [])
        slider1 = request.POST.get('slider1', "1960;2020")
        sort_method = request.POST.get('sort_method', '-')


        # print("Success")
        # render(request, 'index.html', context)
    else:
        form = BlocksForm()
        # form1 = SimpleRadioboxForm()
        # form2 = SimpleCheckboxForm()
        # form2.fields['test'].choices = zip()
        # formset = SimpleFormset(form_kwargs={'choices': ''})
        # print("Failure")

    # print("search federalstate")
    # print(search_federalstate)

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
    # print("test")
    # print(search_opstate)

    if not search_power:
        search_power = SOURCES_LIST
    if not search_opstate:
        search_opstate = ["in Betrieb", "Sonderfall", "Gesetzlich an Stilllegung gehindert"]
    if not search_chp:
        search_chp = ["Nein", "Ja", ""]
    if not search_federalstate:
        search_federalstate = FEDERAL_STATES
    """
    
    states = Blocks.objects.values("state")
    states_l = list(map(lambda x: list(x.values())[0], states))
    states_r = list(set(states_l))
    states_r.sort()
    """
    # feds_r = list(feds_set)
    # print(list(feds))
    # print(SOURCES_LIST)
    # print(search_power)
    queries = search_power
    # print(queries)
    #states = ["in Betrieb", "Sonderfall", "Gesetzlich an Stilllegung gehindert"]
    block_list = Blocks.objects.order_by(sort_method + sort_criteria)
    # print(block_list)
    feds = Blocks.objects.values("state")
    # print(feds)
    feds_l = list(map(lambda x: list(x.values())[0], feds))
    feds_set = set(feds_l)
    feds_r = list(feds_set)
    # print(list(feds))
    # print(feds_r)
    # print("By energy source")
    block_list = filter_or(block_list, "energysource", queries)
    # print(queries)
    # print("By state")
    block_list = filter_or(block_list, "state", search_opstate)
    if search_federalstate:
        # print("By federalstate")
        block_list = filter_or(block_list, "federalstate", search_federalstate)
    # print(block_list)
    block_list = filter_or(block_list, "chp", search_chp)
    block_list = block_list.filter(initialop__range=(lower, upper))

    sources_dict = forge_sources_dict(block_list)
    # print(sources_dict)

    # space
    block_list = block_list[::1]
    block_tmp_dict = list(map(model_to_dict, block_list))
    # print(block_tmp_dict)
    block_dict = create_block_dict(block_tmp_dict)
    # print(block_list)
    # print(block_list[0].id)
    header_list = ['BlockId', 'Name', 'Inbetriebnahme', 'Abschaltung', 'KWK', 'Status', 'Bundesland', 'Nennleistung']
    # template = loader.get_template('plantmaster/blocks.html')
    sources_header = ["Energieträger", "Anzahl", "Nennleistung"]
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
    # options=[('netpower', 'Nennleistung'), ('initialop', 'Inbetriebnahme')]
    # context['form1'] = form1
    # print(context)
    # print(context)
    return render(request, 'plantmaster/blocks.html', context)


def create_block_dict(block_tmp_dict):
    block_dict = {}
    value_list = ["blockname", "initialop", "endop", "chp", "state", "federalstate", "netpower"]
    for entry in block_tmp_dict:
        # print(entry)
        # print(type(entry))
        # print(entry.items())
        key = (entry["energysource"], entry["blockid"])
        value = []
        for element in value_list:
            value.append(entry[element])
        block_dict[key] = value
    # print(block_dict)
    return block_dict



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
