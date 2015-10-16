# -*- coding:utf-8 -*-

import requests
import re

# 北京到盐城直达机票
base_url = "http://flights.ctrip.com/booking/BJS-YNZ-day-1.html"

base_response = requests.get(base_url)
base_text = base_response.text

default_url_reg = re.search(r'http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?(.*)";', base_text)
default_url = "http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?" + default_url_reg.group(1)

default_params_reg = re.search(r"ajaxRequest\(url\+\'&rk=\'\+Math\.random\(\)\*10\+\'(\d+)\'\,\'(.*?)\'\);", base_text.replace(" ", ""))
rk = default_params_reg.group(1)
r = default_params_reg.group(2)

default_url += "&rk=" + rk + "&r=" + r
print default_url

headers = {'Referer': 'http://flights.ctrip.com/booking/BJS-YNZ-day-1.html?allianceid=13963&sid=457771&ouid=000401app-&flightway=SINGLE&flightsearchtype=S&ddate1=2015-10-17&SortByPrice=true'}
flights_response = requests.get(default_url, headers)
print flights_response.text