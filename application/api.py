import requests
import json


class ApiClient :

    #marche seulement en partage de coo
    def get(self, url, data=None):
        r = requests.get(url)
        return r.status_code, r.content, r.headers, r.cookies


    def post(self, url, data):
        r = requests.post(url, data=data)
        return r.status_code, r.content, r.headers, r.cookies,

    def put(self, url, data):
        r = requests.put(url, data=data)
        return r.status_code, r.content, r.headers, r.cookies,

    def delete(self, url, data):
        r = requests.delete(url, data=data)
        return r.status_code, r.content, r.headers, r.cookies,
        