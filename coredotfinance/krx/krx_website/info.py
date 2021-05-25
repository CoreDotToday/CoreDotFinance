from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup as bs
from coredotfinance.krx._to_DataFrame import GettingDataNm


class Info:
    def __init__(self, start, end, day):
        """지수
        :param start: 시작일
        :param end: 종료일
        :param day: 기준일
        """
        today = datetime.now()
        a_month_ago = today - timedelta(days=60)
        self.start = a_month_ago.strftime("%Y%m%d") if start is None else str(start)
        self.end = today.strftime("%Y%m%d") if end is None else str(end)
        self.day = today.strftime("%Y%m%d") if day is None else str(day)

    def update_requested_data(self, requested_data):
        requested_data["MIME Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        requested_data["csvxls_isNo"] = "false"
        return requested_data

    def autocomplete(self, item_name, item_type):
        if item_name is None:
            return None, None, None
        if "&" in item_name:
            # url에 item_name 문자열을 적용시키기 위 '&'를 변환시킴
            item_name = item_name.replace("&", "%2526")

        autocomplete_urls = {
            "index": "http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_equidx&value={item_name}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_equidx_autocomplete",
            "stock": "http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_stkisu&value={item_name}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_stkisu_autocomplete",
            "ETF": "http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_secuprodisu_etf&value={item_name}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_secuprodisu_etf_autocomplete",
            "ETN": "http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_secuprodisu_etn&value={item_name}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_secuprodisu_etn_autocomplete",
            "ELW": "http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_secuprodisu_elw&value={item_name}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_secuprodisu_elw_autocomplete",
            "derivative": "http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_drvprodisu&value={item_name}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_drvprodisu_autocomplete",
            "publish": "http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_bndordisu&value={item_name}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_bndordisu_autocomplete",
            "bond": "http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_bondisu&value={item_name}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_bondisu_autocomplete",
        }
        autocomplete_response = requests.get(
            autocomplete_urls[item_type].format(item_name=item_name)
        )
        soup = bs(autocomplete_response.content, "html.parser")

        if soup is None or len(soup) == 0:
            raise AttributeError(f"{item_name} is Wrong name as a stock name")
        item_scripts = soup.find_all("li")
        # item 입력값이 autocomplete 에서 반환해주는 soup에서 첫번째에 위치하지 않는 경우가 있다. (예 "바이온")
        # 따라서 입력된 item이 autocomlete 내에 있으면 그 soup을 반환해주는 기능을 구현한다.
        item_names = [script.attrs["data-nm"] for script in item_scripts]
        if item_name in item_names:
            index = item_names.index(item_name)
            item_script = item_scripts[index]
        else:
            item_script = item_scripts[0]
        GettingDataNm().data_nm = item_script.attrs["data-nm"]
        return (
            item_script.attrs["data-nm"],
            item_script.attrs["data-cd"],
            item_script.attrs["data-tp"],
        )
