import json

from coredotfinance.krx.core import webio


def convert_vaild_post_params(jsp_soup, post_params):
    """
    post_params needs to be transformed in order to post krx data.
    User input as Korean word is converted into what krx server understands

    Parameters
    ----------
    jsp_soup : bs4.BeautifulSoup
        result of
    post_params : dict
        Examples :
            post_params : {
                "bld": "dbms/MDC/STAT/standard/MDCSTAT01501",
                "mktId": "전체",
                "trdDd": "20210621",
                "MIME Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "csvxls_isNo": "false",
            }

    Returns
    -------
    converted post_prams
    Examples :
        valid_post_params : {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT01501",
            "mktId": "ALL",
            "trdDd": "20210621",
            "MIME Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "csvxls_isNo": "false",
        }
    """
    converting_map = _parse_converting_map(jsp_soup)
    converting_map = _remove_empty_dict(converting_map)

    for key in post_params.keys():
        converting_by_key = converting_map.get(key, None)
        if converting_by_key is not None:
            user_input = post_params[key]
            post_params[key] = converting_by_key.get(user_input, None)
    return post_params


def get_krx_data(post_params):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/"
        "605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15"
    }
    url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
    r = webio.post(url, data=post_params, headers=headers)
    try:
        return r.json()
    except json.JSONDecodeError as e:
        print(
            f"\tdata:\t{post_params}\n"
            f"error:\t{e}\n"
            f"status code:\t{r.status_code}"
            f"response:\t{r}"
        )


def _parse_converting_map(jsp_soup):
    """
    converting map is utilized to convert post_parmas into vaild_post_params to get krx data

    Parameters
    ----------
    jsp_soup : bs4.BeautifulSoup

    Returns
    -------
    converting_map : dict
        {
        "mktId": {"전체": "ALL", "KOSPI": "STK", "KOSDAQ": "KSQ", "KONEX": "KNX"},
        "trdDd": {},
        "share": {"주": "1", "천주": "2", "백만주": "3"},
        "money": {"원": "1", "천원": "2", "백만원": "3", "십억원": "4"},
        }
    """
    # 총 3개의 tag(select, label, input)에서 필요한 정보를 추출한다.
    select = jsp_soup.find_all("select")
    label = jsp_soup.find_all("label")
    input_ = jsp_soup.find_all("input")

    label_map = {}
    for i in label:
        label_map[i.attrs["for"]] = i.text

    converting_map = {}
    for i in input_:
        if i.attrs.get("value", None) != "":
            inner = converting_map.setdefault(i.attrs["name"], {})
            text = label_map.get(i.attrs.get("id", None), None)
            if text is not None:
                inner[text] = i.attrs.get("value", None)

    for select_tag in select:
        if select_tag.attrs.get("name", None) in [
            "bndClssCd",
            "isurCd",
            "idxIndCd",
            "prodId",
            "isuCd",
            "selecbox",
            "invstTpCd",
        ]:  # [14021], [15001], [15007]
            efrb_url = _parse_efrb_url(select_tag)
            result = _get_converting_map(efrb_url)
            converting_map[select_tag.attrs["name"]] = result
        elif select_tag.find_all("option") != "":
            dic = {}
            for option in select_tag.find_all("option"):
                dic[option.text] = option.attrs["value"]
            converting_map[select_tag.attrs["name"]] = dic
        else:
            converting_map[select_tag.attrs["name"]] = {
                select_tag.text: select_tag.next.attrs["value"]
            }
    return converting_map


def _remove_empty_dict(converting_map):
    """
    removes some co

    Parameters
    ----------
    converting_map : dict
        {
        "mktId": {"전체": "ALL", "KOSPI": "STK", "KOSDAQ": "KSQ", "KONEX": "KNX"},
        "trdDd": {},
        "share": {"주": "1", "천주": "2", "백만주": "3"},
        "money": {"원": "1", "천원": "2", "백만원": "3", "십억원": "4"},
        }

    Returns
    -------
        {
        'mktId': {'전체': 'ALL', 'KOSPI': 'STK', 'KOSDAQ': 'KSQ', 'KONEX': 'KNX'},
        'share': {'주': '1', '천주': '2', '백만주': '3'},
        'money': {'원': '1', '천원': '2', '백만원': '3', '십억원': '4'}
        }
    """
    no_use = []
    for key in converting_map.keys():
        if len(converting_map[key]) == 0:
            no_use.append(key)
    for no in no_use:
        converting_map.pop(no)
    return converting_map


def _get_converting_map(efrb_url):
    """
    Getting bundle from ExecuteForResourceBundle.cmd in order to make korean map.
    if user inputs '코스피200 선물' as a parameter, It needs to be converted into 'KRDRVFUK2I'.

    Parameters
    ----------
    efrb_url : str
        Execute for resource bundle url
        Examples : http://data.krx.co.kr/comm/bldAttendant/executeForResourceBundle.cmd?baseName=krx.mdc.i18n.component&key=B107.bld&type=kospi

    Returns
    -------
    Examples :
        {
         '코스피200 선물': 'KRDRVFUK2I',
         '미니코스피200 선물': 'KRDRVFUMKI',
         '코스피200 옵션': 'KRDRVOPK2I',
         '코스피200 위클리 옵션': 'KRDRVOPWKI',
         '미니코스피200 옵션': 'KRDRVOPMKI',
         '코스닥150 선물': 'KRDRVFUKQI',
         '코스닥150 옵션': 'KRDRVOPKQI',
         'KRX300 선물': 'KRDRVFUXI3',
         '변동성지수 선물': 'KRDRVFUVKI',
         '섹터지수 선물': 'KRDRVFUXAT',
         '3년국채 선물': 'KRDRVFUBM3',
         '5년국채 선물': 'KRDRVFUBM5',
         '10년국채 선물': 'KRDRVFUBMA',
         '미국달러 선물': 'KRDRVFUUSD',
         '달러플렉스 선물': 'KRDRVFXUSD',
         '미국달러 옵션': 'KRDRVOPUSD',
         '엔 선물': 'KRDRVFUJPY',
         '유로 선물': 'KRDRVFUEUR',
         '위안 선물': 'KRDRVFUCNH',
         '금 선물': 'KRDRVFUKGD',
         '주식 선물': 'KRDRVFUEQU',
         '주식 옵션': 'KRDRVOPEQU',
         '유로스톡스50 선물': 'KRDRVFUEST'
         }
    """
    soup = webio.get(efrb_url)
    the = json.loads(str(soup))
    new = the["result"]["output"]
    converting_map = {}
    for key in new:
        converting_map[key["name"]] = key["value"]
    return converting_map


def _parse_efrb_url(select_tag):
    """
    returns efrb_url to get converting map

    Parameters
    ----------
    select_tag : bs4.element.Tag
        <select id="prodId" name="prodId"></select>
        The tag is utilzed to complete efrb_url queries.
        queries : str
              "'krx.mdc.i18n.component',
                    key: 'B107.bld'"
    Returns
    -------
    efrb_url : http://data.krx.co.kr/comm/bldAttendant/executeForResourceBundle.cmd?baseName=krx.mdc.i18n.component&key=B107.bld&type=kospi
    """
    queries = str(select_tag.next.next).split("baseName:")[1].split("}")[0]
    for e in queries.split("'"):
        if "krx" in e:
            baseName = e
        elif "bld" in e:
            key = e
    efrb_url = f"http://data.krx.co.kr/comm/bldAttendant/executeForResourceBundle.cmd?baseName={baseName}&key={key}&type=kospi"
    return efrb_url
