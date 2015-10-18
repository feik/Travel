# -*- coding:utf-8 -*-

import collections
import re
import requests
from itertools import combinations

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
            if city_name.decode("utf-8") in item["cities"]:
                return item["cities"]

    @staticmethod
    def generate_one_trip_travel_list(province_city_simple, start_city, end_city):
        alter_cities = Helper.get_same_province_cities_by_city(province_city_simple, end_city)

        one_trip_list = []
        for city_name in alter_cities:
            temp_list = []
            if city_name is not end_city:
                temp_list.append(start_city.decode("utf-8"))
                temp_list.append(city_name)
                temp_list.append(end_city.decode("utf-8"))
                one_trip_list.append(temp_list)
        return one_trip_list

    @staticmethod
    def generate_two_trip_travel_list(province_city_simple, start_city, end_city):
        alter_cities = Helper.get_same_province_cities_by_city(province_city_simple, end_city)
        temp_alter_list = list(combinations(alter_cities, 2))
        two_trips_list = []
        for alter_city_name in temp_alter_list:
            if end_city not in temp_alter_list:
                temp_tuple = (start_city.decode("utf-8"), ) + alter_city_name + (end_city.decode("utf-8"), )
                two_trips_list.append(temp_tuple)

        return two_trips_list
