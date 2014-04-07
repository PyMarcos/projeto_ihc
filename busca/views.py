# -*- coding:utf8 -*-
import pprint
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import urllib
import urllib2
import json
from django.views.generic.base import View
from busca.forms import CharSearchForm, SearchForm
from south.introspection_plugins import django_audit_log
from busca.api_connector import APISearch2
from models import Busca
import string
import collections

key = "a2d0f4dd961f53ab00b83c50f359a8ebab8123e7"
limite = '5'
genero = ''
#nome = "Spider"
nome_real = ''
publisher = ''
ordenar = ''
identificador = ''



def req(tipo, nome):
    url = 'http://api.comicvine.com/' + tipo + '/?api_key=' + key + '&limit=' + limite +'&format=json&filter=name:'+nome
    resp = urllib2.Request(url)
    response = urllib2.urlopen(resp).read()
    data = json.loads(response)
    return data

def req_(url):
    resp = urllib2.Request(url)
    response = urllib2.urlopen(resp).read()
    data = json.loads(response)
    return data

def busca(request):
    personagens = req("characters")
    filmes = req("movies")
    series = req("series")
    historias = req("stories")
    return render(request,
                  'busca.html',
                  {'personagens':personagens,
                   'filmes':filmes,
                   'series':series,
                   'historias':historias}
    )


def get_hero(detail_url):
    pers = req("characters")
    url  = detail_url + '?api_key=' + key
    url += '&field_list=name,teams,real_name,id,character_enemies,'
    url += 'character_friends,image,aliases,deck,publisher,creators,gender,'
    url += 'origin,powers,team_enemies,team_friends,volumes,movies,birth&format=json'
    return req_(url)


def personagem(request):
    pers = req("characters")
    url  = pers["results"][0]["api_detail_url"] + '?api_key=' + key
    url += '&field_list=name,teams,real_name,id,character_enemies,'
    url += 'character_friends,image,aliases,deck,publisher,creators,gender,'
    url += 'origin,powers,team_enemies,team_friends,volumes,movies,birth&format=json'
    data = req_(url)
    return render(request, 'detalhes_personagem.html', {'personagem':data})

def filme(request):
    filme = req("movies")
    url = pers["results"][0]["api_detail_url"] + '?api_key=' + key + '&field_list=name&format=json'
    data = req_(url)
    return render(request, 'detalhes_filme.html', {'filme':data})

def serie(request):
    filme = req("series")
    url = pers["results"][0]["api_detail_url"] + '?api_key=' + key + '&field_list=name&format=json'
    data = req_(url)
    return render(request, 'detalhes_serie.html', {'serie':data})

def historia(request):
    filme = req("storie")
    url = pers["results"][0]["api_detail_url"] + '?api_key=' + key + '&field_list=name&format=json'
    data = req_(url)
    return render(request, 'detalhes_historia.html', {'historia':data})


class SearchChar(View):

    def get(self, request):
        context = {'form': SearchForm()}
        return render(request, 'search.html', context)

    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST)
        if form.is_valid():
            api = APISearch2('characters')
            name = form.cleaned_data.get('search_string')
            results = api.search(field_list=('name','image', 'deck', 'api_detail_url'), name=name)

            context = {'chars': results}
            return render(request, 'ihc/herois.html', context)
        context = {'form': form}
        return render(request, 'search.html', context)

class Search(View):

    def get(self, request):
        form = SearchForm()
        context = {'form': form}
        return render(request, 'search.html', context)


class Index(View):

    def get(self, request):
        return render(request, 'ihc/index.html', {})


class Heroes(View):

    def get(self, request):
        FIELDS = (
            'name', 'deck', 'image', 'api_detail_url'
        )
        results = collections.OrderedDict()

        for letter in string.ascii_lowercase:
            results[letter] = APISearch2('characters').search(limit=4, field_list=FIELDS, name=letter)

        batman = APISearch2('characters').search(limit=1, field_list=FIELDS, name='batman')[0]
        superman = APISearch2('characters').search(limit=1, field_list=FIELDS, name='superman')[0]
        hulk = APISearch2('characters').search(limit=1, field_list=FIELDS, name='hulk')[0]

        return render(request, 'ihc/personagens.html', {'results': results,
                                                        'batman': batman,
                                                        'superman': superman,
                                                        'hul': hulk})

class Hero(View):

    def get(self, request, *args, **kwargs):

        FIELDS = (
            'name', 'deck', 'publisher', 'image', 'creators', 'movies', 'series',
            'birth', 'character_friends', 'gender', 'origin', 'powers', 'story_arcs_credits',
            'real_name', 'team_friends', 'team_enemies'
        )

        search = APISearch2(None).detailed_search(kwargs.get('detail_url'), field_list=FIELDS)
        print search['real_name']

        return render(request, 'ihc/heroi.html', {'hero': search})


class Login(View):

    def get(self, request):
        return render(request, 'login.html', {})


class Characters(View):
    def get(self, request):

        FIELDS = (
            'name', 'deck', 'image'
        )
        results = dict()

        for letter in string.ascii_lowercase:
            results[letter] = APISearch2('characters').search(limit=4, field_list=FIELDS, name=letter)

        return render(request, 'personagens.html', {'results': results})