import requests

class ApiClient :
    
    def get(self, url):
        r = requests.get(url)
        return r.status_code, r.text