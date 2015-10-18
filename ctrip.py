# -*- coding:utf-8 -*-

import requests
import re
import simplejson as json
import collections
import datetime
import urllib
from bs4 import BeautifulSoup


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


# * 北京到盐城 11-07 直达航班
# * S-单程 M-联程 D-往返
class Flight:
    base_url = start_city_code = end_city_code = start_date = ""
    start_city = end_city = ""

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
        self.start_city = start_city
        self.end_city = end_city

        city_url = "http://webresource.c-ctrip.com/code/cquery/resource/address/flight/flight_new_gb2312.js"
        self.start_city_code = Helper.get_city_code(city_url, start_city)
        self.end_city_code = Helper.get_city_code(city_url, end_city)
        self.start_date = start_date if not start_date is None else datetime.date.today()

        temp_history = 'S%24{0}%28{1}%29%24{2}%24{3}%24{4}%28{5}%29%24{6}'\
                       .format(start_city, self.start_city_code, self.start_city_code, self.start_date,
                               end_city, self.end_city_code, self.end_city_code)
        temp_history = 'FD_SearchHistorty={"type":"S","data":"' + temp_history + '"};'

        self.base_url = "http://flights.ctrip.com/booking/{0}-{1}.html".format(self.start_city_code, self.end_city_code)
        self.headers["Cookie"] = temp_history
        self.headers["Referer"] = self.base_url

    def get_flight_list(self):
        base_response = requests.get(self.base_url)
        base_text = base_response.text

        if base_response.headers["Set-Cookie"] is not None:
            # ASP.NET_SessionSvc=MTAuMTUuMTM2LjMxfDkwOTB8b3V5YW5nfGRlZmF1bHR8MTQ0NDI5NzI2NzI1NA;
            session_reg = re.search(r'ASP.NET_SessionSvc=(.*?);',
                                    base_response.headers["Set-Cookie"].replace(" ", "").encode("utf-8"))
            session_code = session_reg.group(1)
            self.headers["Cookie"] += session_code + ';'

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

                print "{0}到{1}在{2}的直达航班：".format(self.start_city, self.end_city, self.start_date)
                print json.dumps(flight_ret, ensure_ascii=False)

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


# flight = Flight("北京", "盐城", "2015-11-07")
# flight.get_flight_list()


# * 北京到盐城 11-07 直达火车票
class Train:
    base_url = start_city_code = end_city_code = start_date_length = start_date = ""
    start_city = end_city = ""

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
        self.start_city = start_city
        self.end_city = end_city
        self.start_date = start_date

        city_url = "http://webresource.ctrip.com/ResTrainOnline/R6/TrainBooking/JS/station_gb2312.js"
        self.start_city_code = Helper.get_city_code(city_url, start_city)
        self.end_city_code = Helper.get_city_code(city_url, end_city)

        date_length = (abs(datetime.datetime.strptime(start_date, "%Y-%m-%d") - datetime.datetime.today())).days

        if start_date is not None:
            self.start_date_length = date_length + 2
        else:
            self.start_date_length = "1"
            self.start_date = datetime.datetime.today()

        encode_start_city = urllib.quote_plus(self.start_city.decode('utf-8').encode('gb2312'))
        encode_end_city = urllib.quote_plus(self.end_city.decode('utf-8').encode('gb2312'))

        self.base_url = "http://trains.ctrip.com/TrainBooking/Search.aspx" \
                        "?from={0}&to={1}&day={2}&number=&fromCn={3}&toCn={4}"\
                        .format(self.start_city_code, self.end_city_code, self.start_date_length,
                                encode_start_city, encode_end_city)
        self.headers["Referer"] = self.base_url

    def get_train_list(self):
        base_response = requests.get(self.base_url)
        base_text = base_response.text

        soup = BeautifulSoup(base_text, "html5lib")
        tr_list = soup.find(id='resultTable01').find_all('tr')

        train_ret = {}
        for tr in tr_list:
            if tr.find(class_="railway_num") is not None:
                train_ret["start_city"] = self.start_city
                train_ret["end_city"] = self.end_city

                train_ret["train_code"] = tr.find(class_="railway_num").get_text()

                train_time_list = tr.find(class_="railway_time").find_parent("td").get_text("|", strip=True)
                train_time_list = train_time_list.split("|")

                train_ret["start_time"] = self.start_date + " " + train_time_list[0]
                train_ret["end_time"] = self.start_date + " " + train_time_list[1]

                if train_time_list[2] is "1":
                    current_date = datetime.datetime.strptime(self.start_date, "%Y-%m-%d")
                    second_day = current_date.day + 1
                    second_date = current_date.replace(day=second_day)

                    train_ret["end_time"] = second_date.strftime("%Y-%m-%d") + " " + train_time_list[1]

                train_seat_list = tr.find_all(class_="railway_seat")
                trains = []
                for train_seat in train_seat_list:
                    one_train = {}
                    one_train["seat"] = train_seat.find(class_="seat_type").get_text(strip=True)

                    train_price = ""
                    train_price_list = train_seat.find(class_=re.compile(r"base_price")).find_all('b')
                    useful_price_list = self.generate_price_class(base_text)
                    for train_price_item in train_price_list:
                        if train_price_item["class"][0] in useful_price_list:
                            train_price += train_price_item.get_text()

                    one_train["price"] = train_price
                    one_train["left_tickets"] = train_seat.find(class_="seat_num").i.get_text()

                    trains.append(one_train)

                train_ret["trains"] = trains

                print "{0}到{1}在{2}的直达列车：".format(self.start_city, self.end_city, self.start_date)
                print json.dumps(train_ret, ensure_ascii=False)

    @staticmethod
    def generate_price_class(base_text):
        m = re.findall(r"\.([a-z0-9]+)\{(?:display)?\:?\}", base_text.replace(" ", ""))
        return m

# train = Train("北京", "盐城", "2015-11-07")
# train.get_train_list()


# * 北京到盐城 11-07 直达汽车票
class Bus:
    base_url = start_city_code = end_city_code = start_date_length = start_date = ""
    start_city = end_city = ""

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
        self.start_city = start_city
        self.end_city = end_city
        self.start_date = start_date

        encode_start_city = urllib.quote_plus(self.start_city)
        encode_end_city = urllib.quote_plus(self.end_city)

        self.base_url = "http://bus.ctrip.com/busList.html" \
                        "?from={0}&to={1}&date={2}"\
                        .format(encode_start_city, encode_end_city, self.start_date)
        self.headers["Referer"] = self.base_url

    def get_bus_list(self):
        base_response = requests.get(self.base_url)
        # 取unicode编码的text会乱码
        base_text = base_response.content

        soup = BeautifulSoup(base_text, "html5lib")
        tr_list = soup.find(id='tb_railway_list').find_all('tr')
        bus_ret = {}
        for tr in tr_list:
            if tr.find(class_="railway_time") is not None:
                bus_ret["start_city"] = self.start_city
                bus_ret["end_city"] = self.end_city

                bus_ret["start_time"] = tr.find(class_="railway_time").get_text()

                from_to_tag = tr.find(class_="icon_start").find_parent("td")
                bus_ret["from_to"] = from_to_tag.get_text(" - ", strip=True)
                bus_ret["bus_code"] = from_to_tag.find_next_sibling("td").get_text(" - ", strip=True)
                bus_ret["price"] = tr.find(class_="price").find(class_="base_price").get_text()
                bus_ret["enable_book"] = tr.find(class_="btn_book")["value"]

                print "{0}到{1}在{2}的直达汽车：".format(self.start_city, self.end_city, self.start_date)
                print json.dumps(bus_ret, ensure_ascii=False)

bus = Bus("北京", "盐城", "2015-11-07")
bus.get_bus_list()
