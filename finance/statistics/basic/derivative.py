# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
from finance.statistics.basic.info import Info

class Derivative(Info):
    def __init__(self, code, start, end, day, product, code_to_function):
        super().__init__(start, end, day)
        self.function = code_to_function

    def autocomplete(self, product):
        pass

class Price(Derivative):
    def __init__(self, code, start, end, day, product, **kwargs):
        code_to_function = {
            '15001': '',
            '15002': '',
            '15003': ''
        }


class Information(Derivative):
    def __init__(self, code, start, end, day, product, **kwargs):
        code_to_function = {
            '15004': '',
            '15005': '',
        }

class Performance(Derivative):
    def __init__(self, code, start, end, day, product, **kwargs):
        code_to_function = {
            '15006': '',
            '15007': '',
            '15008': '',
            '15009': ''
        }


class Detail(Derivative):
    def __init__(self, code, start, end, day, product, **kwargs):
        code_to_function = {
            '15010': '',
            '15011': '',
            '15012': '',
            '15013': '',
            '15014': '',
            '15015': '',
            '15016': ''
        }
