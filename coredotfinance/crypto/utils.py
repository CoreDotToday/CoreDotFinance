import time
import datetime


def date_to_timestamp(date):
    timestamp = time.mktime(datetime.datetime.strptime(date, '%Y%m%d').timetuple())
    return f'{timestamp * 1000:.0f}'