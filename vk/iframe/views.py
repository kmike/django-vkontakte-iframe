#coding: utf-8
from django.http import HttpResponse
from django.utils import simplejson as json
from django.db.transaction import commit_on_success
from vk.iframe.models import Country, City

@commit_on_success
def load_countries(request):
    if request.is_ajax():
        countries = json.loads(request.POST.get('countries', ''))
        for country in countries:
            Country.objects.get_or_create(id=country['cid'],
                                          defaults=dict(title=country['title']))
        return HttpResponse('OK')
    return HttpResponse('')

@commit_on_success
def load_cities(request, country_id):
    if request.is_ajax():
        cities = json.loads(request.POST.get('cities', ''))
        for city in cities:
            City.objects.get_or_create(id=city['cid'],
                                       defaults=dict(
                                           title=city['title'],
                                           country_id = country_id
                                       ))
        return HttpResponse('OK')
    return HttpResponse('')
