import requests
import json


class ApiClient :

    #marche seulement en partage de coo
    def get(self, url, params=None, headers=None):
        r = requests.get(url, params=params, headers=headers)
        return r.status_code, r.content, r.headers, r.cookies


    def post(self, url, params=None, headers=None, query=None):
        r = requests.post(url, params=params, headers=headers, data=query)
        return r.status_code, r.content, r.headers, r.cookies

    def put(self, url, params=None, headers=None, query=None):
        r = requests.put(url, params=params, headers=headers, data=query)
        return r.status_code, r.content, r.headers, r.cookies

    def delete(self, url, params=None, headers=None, query=None):
        r = requests.delete(url, params=params, headers=headers, data=query)
        return r.status_code, r.content, r.headers, r.cookies
        