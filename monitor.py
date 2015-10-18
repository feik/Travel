# -*- coding:utf-8 -*-

from ctrip import Flight, Train, Bus
from helper import Helper
import simplejson as json


class Monitor:
    province_city_simple = None
    start_city = end_city = start_date = ""
    alter_cities = []

    def __init__(self, start_city, end_city, start_date):
        self.province_city_simple = json.load(open('province_city_simple.json', 'r+'))

        self.start_city = start_city
        self.end_city = end_city
        self.start_city = start_date

        self.alter_cities = Helper.get_same_province_cities_by_city(self.province_city_simple, self.end_city)

    def flight_to_train_to_bus(self):
        print "飞机转火车转汽车"
        for city_item in self.alter_cities:
            pass

    def flight_to_bus_to_train(self):
        print "飞机转汽车转火车"

    def flight_to_bus(self):
        print "飞机转汽车"

    def flight_to_train(self):
        print "飞机转火车"

    def train_to_flight_to_bus(self):
        print "火车转飞机转汽车"

    def train_to_bus_to_flight(self):
        print "火车转汽车转飞机"

    def train_to_flight(self):
        print "火车转飞机"

    def train_to_bus(self):
        print "火车转汽车"

    def bus_to_flight_to_train(self):
        print "汽车转飞机转火车"

    def bus_to_train_to_flight(self):
        print "汽车转火车转飞机"

    def bus_to_train(self):
        print "汽车转火车"

    def bus_to_flight(self):
        print "汽车转飞机"




monitor = Monitor("北京", "盐城", "2015-11-07")

# flight = Flight("北京", "盐城", "2015-11-07")
# flight.get_flight_list()

# train = Train("北京", "盐城", "2015-11-07")
# train.get_train_list()

# bus = Bus("北京", "盐城", "2015-11-07")
# bus.get_bus_list()