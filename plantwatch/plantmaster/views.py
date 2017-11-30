from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Blocks
from .models import Addresses
from django.db.models import Sum
from django.shortcuts import render
from django.db.models import Q


def filter_and(queryset, filtered, filters):
    #print(queryset)
    for afilter in filters:
        queryset = filter_queryset(queryset, filtered, afilter)
        #print(queryset.all().count())
    return queryset


def filter_or(queryset, filtered, filters):
    param0 = {filtered: filters[0]}
    param1 = {filtered: filters[1]}
    param2 = {filtered: filters[2]}
    queryset = queryset.all().filter(Q(**param0) | Q(**param1) | Q(**param2))
    return queryset


def filter_queryset(queryset, filtered, afilter):
    #print(filtered, afilter)
    param = {filtered: afilter}
    new_queryset = queryset.all().filter(**param)
    return new_queryset


def get_queries(code):
    queries_l = ["", "Erdgas", "Steinkohle", "", "", "", "Braunkohle"]
    queries = []
    k = 0
    offset_counter = 0
    checked = []
    for i in [6, 2, 1]:
        tmp = code - i
        if tmp >= 0:
            checked.insert(0, "checked")
            queries.append(queries_l[i])
            code -= i
        else:
            checked.insert(0, " ")
            k += 1

    #print(queries)
    while k>0:
        queries.insert(offset_counter, queries[0])
        offset_counter += 1
        k -= 1
    #print(queries)
    return checked, queries


def index(request):
    return HttpResponse("test")


def blocks(request, lower=1960, upper=2020, code=123):
    #print(code)
    checked, queries = get_queries(code)
    #print(queries)
    states = ["in Betrieb", "Sonderfall", "Gesetzlich an Stilllegung gehindert"]
    block_list = Blocks.objects.order_by('-netpower')
    block_list = filter_or(block_list, "energysource", queries)
    block_list = filter_or(block_list, "state", states)
    block_list = block_list.filter(initialop__range=(lower, upper))
    power = block_list.all().aggregate(Sum('netpower'))['netpower__sum']
    count = block_list.all().count()
    header_list = ['BlockId', 'Name', 'Inbetriebnahme', 'Status', 'Nennleistung']
    # template = loader.get_template('plantmaster/blocks.html')
    context = {
        'header_list': header_list,
        'block_list': block_list,
        'power': power,
        'count': count,
        'upper': upper,
        'lower': lower,
        'checked': checked
    }
    #print(context)
    return render(request, 'plantmaster/blocks.html', context)


def block(request, blockid):
    block = Blocks.objects.get(blockid=blockid)
    address = Addresses.objects.get(blockid=blockid)
    data_list = [address.blockid.blockname, address.plz, address.place, address.street, address.state, block.netpower]
    #print(data_list)
    header_list = ['Name', 'PLZ', 'Ort', 'Anschrift', 'Bundesland', 'Nennleistung']
    template = loader.get_template('plantmaster/block.html')
    context = {
        'data_list': zip(header_list, data_list),
    }
    return HttpResponse(template.render(context, request))
