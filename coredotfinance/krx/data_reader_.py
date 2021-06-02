import re
import json
import requests
import logging

from bs4 import BeautifulSoup as bs

from coredotfinance.krx._to_DataFrame import to_DataFrame
from coredotfinance.krx._get_requested_data import get_requested_data


def data_reader(
    code, start=None, end=None, day=None, division=None, item=None, **kwargs
):
    requested_data = get_requested_data(code, start, end, day, division, item, **kwargs)
    # jsp_soup는 MDCSTAT044.jsp 의 소스 코드다.
    # readable_column, conveted_requested_data 를 얻기에 필요하다.
    mdcstat = parse_mdcstat(requested_data)
    jsp_soup = get_jsp_soup(mdcstat)
    # requested_data는 data.krx로 requests.post 되기 부적합하다. 유효한 형태로 전환해 주어야 한다.
    # ex) '전체' -> 'ALL' , '주식 선물' -> 'KRDRVFUEQU'
    valid_requested_data = convert_valid_requested_data(jsp_soup, requested_data)

    readable_columns = get_readable_columns(jsp_soup, mdcstat)
    krx_data = get_krx_data(valid_requested_data)

    return to_DataFrame(krx_data, readable_columns)


def parse_mdcstat(requested_data):
    bld = requested_data["bld"]
    mdcstat = bld.split("/")[-1]
    return mdcstat


def get_jsp_soup(mdcstat):
    jsp_filename = mdcstat[:-2]
    url = f"http://data.krx.co.kr/contents/MDC/STAT/standard/{jsp_filename}.jsp"
    # TODO: Consider whether it is needed that checking status_code is 200 or not.
    html = requests.get(url)
    response = html.status_code
    if response == 403:
        print('Ip may be blocked from [http://data.krx.co.kr/]')
        raise requests.ConnectionError(html)
    elif response != 200:
        raise requests.ConnectionError(html)
    jsp_soup = bs(html.content, "html.parser")
    return jsp_soup


def convert_valid_requested_data(jsp_soup, requested_data):
    converting_map = parse_converting_map(jsp_soup)
    converting_map = remove_len_zero(converting_map)

    for key in requested_data.keys():
        converting_by_key = converting_map.get(key, None)
        if converting_by_key is not None:
            user_input = requested_data[key]
            requested_data[key] = converting_by_key.get(user_input, None)
    # now requested_data becomes requested_data
    return requested_data


def parse_converting_map(jsp_soup):
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
        # TODO: 아래의 if 문이 hard coding 으로 작성되어 있다.
        #  리스트를 사용하기 보다 어떤 경우에 execute_for_resource_bundle 을 사용하는지 알아내라.
        if select_tag.attrs.get("name", None) in [
            "bndClssCd",
            "isurCd",
            "idxIndCd",
            "prodId",
            "isuCd",
            "selecbox",
            "invstTpCd",
        ]:  # [14021], [15001], [15007]
            efrb_url = parse_efrb_url(select_tag)
            result = get_resource_bundle(efrb_url)
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


def remove_len_zero(converting_map):
    no_use = []
    for key in converting_map.keys():
        if len(converting_map[key]) == 0:
            no_use.append(key)
    for no in no_use:
        converting_map.pop(no)
    return converting_map


# Getting bundle from ExecuteForResourceBundle.cmd
# in order to make readable map
def get_resource_bundle(efrb_url):
    html = requests.get(efrb_url)
    if html.status_code != 200:
        raise requests.ConnectionError(html)
    soup = bs(html.content, "html.parser")
    the = json.loads(str(soup))
    new = the["result"]["output"]
    result = {}
    for n in new:
        result[n["name"]] = n["value"]
    return result


def parse_efrb_url(select_tag):
    queries = str(select_tag.next.next).split("baseName:")[1].split("}")[0]
    for e in queries.split("'"):
        if "krx" in e:
            baseName = e
        elif "bld" in e:
            key = e
    market = "kospi"
    efrb_url = f"http://data.krx.co.kr/comm/bldAttendant/executeForResourceBundle.cmd?baseName={baseName}&key={key}&type={market}"
    return efrb_url


def get_readable_columns(jsp_soup, mdcstat):
    map_ = {}
    jsGrid_dict = parse_jsGrid_dict(jsp_soup)
    jsGrid = jsGrid_dict[mdcstat]

    table_tag = jsp_soup.find("table", {"id": jsGrid})
    div_tag = jsp_soup.find("div", {"id": jsGrid})

    if table_tag:
        print("*" * 100, "이 글을 보았다면 바로 개발자에게 알려주세요 ㅎㅎ")
        table_map = parse_table_map(table_tag)
        map_.update(table_map)
    if div_tag:
        div_map = parse_div_map(div_tag)
        map_.update(div_map)
    return map_


def parse_jsGrid_dict(jsp_soup):
    jscode_list = jsp_soup.find_all("script")
    for s in jscode_list:
        # TODO : change the variable, s
        #  What does s mean?
        if "jsGrid" in str(s):
            jscode = s
            break
    jscode_str = str(jscode)
    mdcstat_list = re.findall(
        r"template: \$content\.select\(\'\#(jsGrid_MDCSTAT[0-9]*\_[0-9])", jscode_str
    )
    bld_list = re.findall(r"bld: \'dbms/MDC/STAT/standard/(MDCSTAT[0-9]*)", jscode_str)
    jsGrid_dict = {}
    for mdcstat, bld in zip(mdcstat_list, bld_list):
        lis = jsGrid_dict.setdefault(bld, [])
        lis.append(mdcstat)
    return jsGrid_dict


def parse_table_map(table_tag):
    table_map = {}
    # TODO : Change the table_maptionary name, table_map.
    for tr in table_tag.find_all("tr"):
        th = tr.find_all("th")
        td = tr.find_all("td")
        for name, id in zip(th, td):
            table_map[id.attrs["data-bind"]] = name.text
    return table_map


def parse_div_map(div_tag):
    thead = div_tag.thead
    if thead is None:
        return {}
    tag_list = []
    tag_list.extend(thead.find_all("th"))
    tag_list.extend(thead.find_all("td"))

    div_map = {}
    for i in tag_list:
        div_map[i.attrs["name"]] = {
            "text": i.text,
            "parent": i.attrs.get("parent", None),
        }

    p_list = set()
    for key in div_map:
        p = div_map[key]["parent"]

        if p is not None:
            child_name = div_map[key]["text"]
            parent_name = div_map[p]["text"]
            div_map[key]["text"] = f"{parent_name}//{child_name}"

            p_list.add(p)
    [div_map.pop(p) for p in p_list]
    for d in div_map:
        div_map[d] = div_map[d]["text"]
    return div_map


def get_krx_data(requested_data):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/"
        "605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15"
    }
    url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
    r = requests.post(url, data=requested_data, headers=headers)

    try:
        krx_data = json.loads(r.content)
    except json.JSONDecodeError as e:
        logger = logging.getLogger("log")
        logger.info(
            f"\tdata:\t{requested_data}\n"
            f"error:\t{e}\n"
            f"status code:\t{r.status_code}"
            f"response:\t{r}"
        )
    return krx_data
