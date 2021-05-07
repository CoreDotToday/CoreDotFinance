import datetime


def get_today():
    today = datetime.date.today()
    return today.strftime('%Y%m%d')


def get_past_days_ago(days: int=60) -> str:
    today = datetime.date.today()
    past_days_ago = today - datetime.timedelta(days)
    return past_days_ago.strftime('%Y%m%d')


def make_6digits_code(code: float) -> str:
    """
    종목코드/업종코드 등의 코드를 6자리 형식으로 맞추어줌
    (예: '5930.0' -> '005930')
    """
    return f'{float(code):06.0f}'
