import collections
import re
import requests


class Helper:
    def __init__(self):
        pass

    @staticmethod
    def convert(data):
        if isinstance(data, basestring):
            return str(data)
        elif isinstance(data, collections.Mapping):
            return dict(map(Helper.convert, data.iteritems()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(Helper.convert, data))
        else:
            return data

    @staticmethod
    def get_city_code(city_url, city_name):
        city_response = requests.get(city_url)
        city_text = city_response.text

        city_text_reg = re.search(r'data\:\"\|' + city_name + '\|(.*?)\"',
                                  city_text.replace(" ", "").encode("utf-8"))
        city_code = city_text_reg.group(1)

        return city_code

    @staticmethod
    def get_city_by_province(province_city_simple=[], province_name=None):
        for item in province_city_simple:
            if item["name"] is province_name:
                return item["cities"]

    @staticmethod
    def get_province_by_city(province_city_simple=[], city_name=None):
        for item in province_city_simple:
            if city_name in item["cities"]:
                return item["name"]

    @staticmethod
    def get_same_province_cities_by_city(province_city_simple=[], city_name=None):
        for item in province_city_simple:
            if city_name in item["cities"]:
                return item["cities"]