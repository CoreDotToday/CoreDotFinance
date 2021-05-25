import datetime


def get_today():
    today = datetime.date.today()
    return today.strftime("%Y%m%d")


def get_past_days_ago(days: int = 60) -> str:
    today = datetime.date.today()
    past_days_ago = today - datetime.timedelta(days)
    return past_days_ago.strftime("%Y%m%d")
