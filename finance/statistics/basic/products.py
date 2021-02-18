# -*- coding: utf-8 -*-

from finance.statistics.basic.info import Info

class Product(Info):
    pass

class ETF(Product):
    def __init__(self, code, start, end, day, product_name, search_type):
        """
        증권 상품
        :param code:
        :param start:
        :param end:
        :param day:
        :param product_name:
        :param search_type:
        """
        code_to_function = {

        }
        super(ETF, self).__init__(code, start, end, day, product_name, code_to_function)
