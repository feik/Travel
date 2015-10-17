# -*- coding:utf-8 -*-

import requests
import re
import simplejson as json
import collections
import datetime

class Helper:
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


# * 北京到盐城 11-07 直达航班
# * S-单程 M-联程 D-往返
class Flight:
    base_url = start_city_code = end_city_code = start_date = ""

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
        'Connection': 'keep-alive',
        'Cookie': '',
        'DNT': '1',
        'Host': 'flights.ctrip.com',
        'Referer': 'http://flights.ctrip.com/booking/BJS-YNZ-day-1.html',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/46.0.2490.71 Safari/537.36'
    }

    def __init__(self, start_city, end_city, start_date=None):
        # S$北京(BJS)$BJS$2015-11-07$盐城(YNZ)$YNZ
        self.start_city_code = self.get_city_code(start_city)
        self.end_city_code = self.get_city_code(end_city)
        self.start_date = start_date if not start_date is None else datetime.date.today()

        temp_history = 'S%24{0}%28{1}%29%24{2}%24{3}%24{4}%28{5}%29%24{6}'\
                       .format(start_city, self.start_city_code, self.start_city_code, self.start_date,
                               end_city, self.end_city_code, self.end_city_code)
        temp_history = 'ASP.NET_SessionSvc=MTAuMTUuMTM2LjI3fDkwOTB8b3V5YW5nfGRlZmF1bHR8MTQ0NDI5NjA3NDM3MA;' \
                       'FD_SearchHistorty={"type":"S","data":"' + temp_history + '"}'

        self.base_url = "http://flights.ctrip.com/booking/{0}-{1}.html".format(self.start_city_code, self.end_city_code)
        self.headers["Cookie"] = temp_history
        self.headers["Referer"] = self.base_url

    def get_flight_list(self):
        base_response = requests.get(self.base_url)
        base_text = base_response.text

        if base_response.headers["Set-Cookie"] is not None:
            pass

        default_url = self.generate_default_url(base_text)

        flights_response = requests.get(default_url, headers=self.headers)
        flights_response_json = json.loads(flights_response.text, encoding='utf-8')

        # dic {YNZ0: "南洋国际机场", PEK3: "首都国际机场T3"}
        flight_response_apb = flights_response_json["apb"]

        flights = flights_response_json["fis"]
        flight_ret = {}

        if len(flights) > 0:
            for flight in flights:
                flight_ret["price"] = flight["lp"]

                flight_ret["start_time"] = flight["dt"].encode("utf-8")
                flight_ret["end_time"] = flight["at"].encode("utf-8")

                flight_ret["start_airport_code"] = "{0}{1}".format(flight["dpc"], flight["dbid"])
                flight_ret["start_airport"] = flight_response_apb[flight_ret["start_airport_code"]].encode("utf-8")
                flight_ret["end_airport_code"] = "{0}{1}".format(flight["apc"], flight["abid"])
                flight_ret["end_airport"] = flight_response_apb[flight_ret["end_airport_code"]].encode("utf-8")

                print flight_ret

    @staticmethod
    def generate_default_url(base_text):
        default_url_reg = re.search(r'http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?(.*)";',
                                    base_text)
        default_url = "http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights" + \
                      default_url_reg.group(1)

        default_params_reg = re.search(r"ajaxRequest\(url\+\'&rk=\'\+Math\.random\(\)\*10\+\'(\d+)\'\,\'(.*?)\'\);",
                                       base_text.replace(" ", ""))
        rk = "0.971286497078836" + default_params_reg.group(1)
        r = default_params_reg.group(2)

        default_url += "&rk=" + rk + "&r=" + r
        return default_url

    @staticmethod
    def get_city_code(city_name):
        city_url = "http://webresource.c-ctrip.com/code/cquery/resource/address/flight/flight_new_gb2312.js"
        city_response = requests.get(city_url)
        city_text = city_response.text

        city_text_reg = re.search(r'data\:\"\|' + city_name + '\|(.*?)\"',
                                  city_text.replace(" ", "").encode("utf-8"))
        city_code = city_text_reg.group(1)

        return city_code


# * 北京到盐城 11-07 直达汽车票
class Bus:
    base_url = ""

    def __init__(self, base_url="http://bus.ctrip.com/busList.html?from=%E5%8C%97%E4%BA%AC&to=%E7%9B%90%E5%9F%8E"
                                "&date=2015-11-07"):
        self.base_url = base_url

    def get_bus_list(self):
        base_response = requests.get(self.base_url)
        base_text = base_response.text


# * 北京到盐城 11-07 直达火车票
class Train:
    base_url = ""

    def __init__(self, base_url="http://trains.ctrip.com/TrainBooking/Search.aspx?from=beijing&to=yancheng2&day=22"
                                "&number=&fromCn=%B1%B1%BE%A9&toCn=%D1%CE%B3%C7"):
        self.base_url = base_url

    def get_train_list(self):
        base_response = requests.get(self.base_url)
        base_text = base_response.text

flight = Flight("北京", "盐城", "2015-11-07")
flight.get_flight_list()