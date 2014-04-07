# -*- coding:utf8 -*-
__author__ = 'Marcos'

import requests
import json
import pprint
import time

_BASE_URL = 'http://www.comicvine.com/api/search/?format=json'
BASE_URL = 'http://beta.comicvine.com/api/'
# API_KEY = '0b88f28cd72df0efcd040404ac5ad0a1567b5748'
API_KEY = 'a2d0f4dd961f53ab00b83c50f359a8ebab8123e7'
RESPONSE_FORMAT = 'json'

class APISearch2(object):

    def __init__(self, resource):
        self.resource = resource
        self.base_url = BASE_URL
        self.api_key = API_KEY

    def _clean_filter(self, filter_, value):
        return '{}:{}'.format(filter_, '+'.join(str(value).split()))

    def changeResource(resource):
        self.resource = resource

    def urlMount(self, offset=0, limit=100, format_='json', field_list=None, **filters):
        url = '{base}{res}/?api_key={key}&format={frmt}&limit={lim}&offset={off}'.format(
            base=self.base_url, key=self.api_key, frmt=format_, lim=limit,
            res=self.resource, off=offset)
        if hasattr(field_list, '__iter__'):
            url += '&field_list={}'.format(','.join(field_list))
        if len(filters):
            url += '&filter='
            for filter_, value in filters.items():
                url += self._clean_filter(filter_, value) + ','
        print url.strip(',')
        return url.strip(',')


    def _request(self, url):
        return requests.get(url)

    def _JSONparser(self, response):
        return response.json()

    def search(self, offset=0, limit=100, format_='json', field_list=None, **filters):
        url = self.urlMount(offset, limit, format_, field_list, **filters)
        response = self._request(url)
        # return response
        if response.status_code == 200:
            if format_ == 'json':
                return self._JSONparser(response).get('results', None)
        return None

    def detailed_search(self, api_datial_url, field_list=None):
        url = '{}?api_key={}&format=json'.format(api_datial_url, self.api_key)

        if hasattr(field_list, '__iter__'):
            url += '&field_list={}'.format(','.join(field_list))
        return self._JSONparser(self._request(url)).get('results', None)
