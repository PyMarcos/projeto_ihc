# -*- coding:utf8 -*-
__author__ = 'Marcos'

from django import forms

class CharSearchForm(forms.Form):
    char_name = forms.CharField(max_length=100, label='Nome do personagem')


class SearchForm(forms.Form):
    _CHOICES = (('movies', u'filmes'),
                ('characters', u'personagens'),
                ('stories', u'histórias'),
                ('series', u'series'))

    search_string = forms.CharField(max_length=150, label='buscar por:')
    search_types = forms.MultipleChoiceField(required=False,
        widget=forms.CheckboxSelectMultiple, choices=_CHOICES, label="buscar em:")