import requests
import configparser

class RequestRakutenProductAPI:

    def __init__(self, base_url, api_key, keyword):
        self.base_url = base_url
        self.api_key = api_key
        self.keyword = keyword

    # パラメータを付随する
    def make_url(self):
        search_params = {
            "format" :  "json",
            "keyword" : self.keyword,
            "applicationId" : self.api_key
        }
        return search_params

    def execute_api(self, params):
        return requests.get(self.base_url, params)

    def success(self, status_code):
        if (status_code == 200):
            return True

        return False