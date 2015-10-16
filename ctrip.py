# -*- coding:utf-8 -*-

import requests
import re
import json

base_url = "http://flights.ctrip.com/booking/BJS-YNZ-day-1.html"

base_response = requests.get(base_url)
base_text = base_response.text

default_url_reg = re.search(r'http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?(.*)";', base_text)
default_url = "http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights" + default_url_reg.group(1)

default_params_reg = re.search(r"ajaxRequest\(url\+\'&rk=\'\+Math\.random\(\)\*10\+\'(\d+)\'\,\'(.*?)\'\);", base_text.replace(" ", ""))
rk = "0.971286497078836" + default_params_reg.group(1)
r = default_params_reg.group(2)

default_url += "&rk=" + rk + "&r=" + r
print default_url


headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
    'Connection': 'keep-alive',
    'Cookie': '_abtest_userid=08420bcc-33a2-4ae9-95ef-1988c91e64b3; Union=AllianceID=1432&SID=1686&OUID=4978350482__13529; Session=SmartLinkCode=U1686&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; zdata=zdata=Q+Wu3r+UJgLwCtLkVMFsbP57m1g=; DomesticUserHostCity=BJS|%b1%b1%be%a9; bid=bid=F; _gat=1; appFloatCnt=5; ASP.NET_SessionSvc=MTAuMTUuMTM2LjMxfDkwOTB8b3V5YW5nfGRlZmF1bHR8MTQ0NDI5NzI2NzI1NA; _bfa=1.1444659470950.1r59xd.1.1444998788490.1445012376199.5.13; _bfs=1.2; _ga=GA1.2.738540759.1444659474; _jzqco=%7C%7C%7C%7C1444659474101%7C1.30253621.1444659474074.1445012379229.1445012385255.1445012379229.1445012385255.undefined.0.0.12.12; __zpspc=9.4.1445012379.1445012385.2%234%7C%7C%7C%7C%7C%23; _bfi=p1%3D101027%26p2%3D100101991%26v1%3D13%26v2%3D12; FD_SearchHistorty={"type":"S","data":"S%24%u5317%u4EAC%28BJS%29%24BJS%242015-11-07%24%u76D0%u57CE%28YNZ%29%24YNZ"}',
    'DNT': '1',
    'Host': 'flights.ctrip.com',
    'Referer': 'http://flights.ctrip.com/booking/BJS-YNZ-day-1.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
}
flights_response = requests.get(default_url, headers=headers)
flights_response_json = json.loads(flights_response.text)

# dic {ZH: "深圳航空", CA: "中国国航"}
print flights_response_json["als"]
# dic {YNZ0: "南洋国际机场", PEK3: "首都国际机场T3"}
print flights_response_json["apb"]
# list [{dcc: "BJS", acc: "YNZ", dtr: "", atr: "", nd: 0, rlp: 0, fx: 0,…},…]
print flights_response_json["fis"]