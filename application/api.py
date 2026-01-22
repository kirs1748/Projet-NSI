import requests
import json


class ApiClient :

    #marche seulement en partage de coo
    def get(self, url):
        r = requests.get(url)
        return r.status_code, r.content, r.headers, r.cookies
        