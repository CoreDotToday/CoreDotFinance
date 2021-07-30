import re
import os
import json

FILE_PATH = os.path.dirname(os.path.realpath(__file__))


def get_korean_columns(jsp_soup, mdcstat):
    """
    data.krx.co.kr returns data with not friendly-key name.
    Korean_columns is utilzed to convert not friendly-key name into Korean word.

    Parameters
    ----------
    jsp_soup : bs4.BeautifulSoup
    mdcstat : str

    Returns
    -------
    map_ : dict
    Examples :
    {
     'ISU_SRT_CD': '종목코드',
     'ISU_NM': '종목명',
     'TDD_CLSPRC': '종가',
     'CMPPREVDD_PRC': '대비',
     'TDD_OPNPRC': '시가',
     'TDD_HGPRC': '고가',
     'TDD_LWPRC': '저가',
     'SPOT_PRC': '현물가',
     'SETL_PRC': '정산가',
     'ACC_TRDVOL': '거래량',
     'ACC_TRDVAL': '거래대금',
     'ACC_OPNINT_QTY': '미결제약정'
    }
    """
    map_ = {}
    jsGrid_dict = _parse_jsGrid_dict(jsp_soup)
    jsGrid = jsGrid_dict[mdcstat]

    table_tag = jsp_soup.find("table", {"id": jsGrid})
    div_tag = jsp_soup.find("div", {"id": jsGrid})

    if table_tag:
        table_map = _parse_table_map(table_tag)
        map_.update(table_map)
    if div_tag:
        div_map = _parse_div_map(div_tag)
        map_.update(div_map)
    return map_


def _parse_jsGrid_dict(jsp_soup):
    """
    Parameters
    ----------
    jsp_soup : bs4.BeautifulSoup

    Returns
    -------
    Examples:
        {
        'MDCSTAT12501': ['jsGrid_MDCSTAT125_0'],
        'MDCSTAT12502': ['jsGrid_MDCSTAT125_1']
        }
    """
    jscode_tag_list = jsp_soup.find_all("script")
    for tag in jscode_tag_list:
        # TODO : change the variable, s
        #  What does s mean?
        if "jsGrid" in str(tag):
            jscode = tag
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


def _parse_table_map(table_tag):
    table_map = {}
    for tr in table_tag.find_all("tr"):
        th = tr.find_all("th")
        td = tr.find_all("td")
        for name, id in zip(th, td):
            table_map[id.attrs["data-bind"]] = name.text
    return table_map


def _parse_div_map(div_tag):
    """
    Parameters
    ----------
    div_tag: bs4.element.Tag
        Examples : '15001'
            <div id="jsGrid_MDCSTAT125_0">
            <table>
            <thead>
            <tr>
            <th align="center" name="ISU_SRT_CD" scope="col" width="100px">종목코드</th>
            <th name="ISU_NM" scope="col" width="220px">종목명</th>
            <th align="right" name="TDD_CLSPRC" scope="col" width="90px">종가</th>
            <th align="right" name="CMPPREVDD_PRC" scope="col" width="90px">대비</th>
            <th align="right" name="TDD_OPNPRC" scope="col" width="90px">시가</th>
            <th align="right" name="TDD_HGPRC" scope="col" width="90px">고가</th>
            <th align="right" name="TDD_LWPRC" scope="col" width="90px">저가</th>
            <th align="right" name="SPOT_PRC" scope="col" width="100px">현물가</th>
            <th align="right" name="SETL_PRC" scope="col" width="100px">정산가</th>
            <th align="right" name="ACC_TRDVOL" scope="col" width="120px">거래량</th>
            <th align="right" name="ACC_TRDVAL" scope="col" width="130px">거래대금</th>
            <th align="right" name="ACC_OPNINT_QTY" scope="col" width="120px">미결제약정</th>
            </tr>
            </thead>
            <tbody>
            <tr>
            <td bind="ISU_SRT_CD" name="ISU_SRT_CD"></td>
            <td bind="ISU_NM" name="ISU_NM"></td>
            <td bind="TDD_CLSPRC" name="TDD_CLSPRC"></td>
            <td bind="CMPPREVDD_PRC" name="CMPPREVDD_PRC"></td>
            <td bind="TDD_OPNPRC" name="TDD_OPNPRC"></td>
            <td bind="TDD_HGPRC" name="TDD_HGPRC"></td>
            <td bind="TDD_LWPRC" name="TDD_LWPRC"></td>
            <td bind="SPOT_PRC" name="SPOT_PRC"></td>
            <td bind="SETL_PRC" name="SETL_PRC"></td>
            <td bind="ACC_TRDVOL" name="ACC_TRDVOL"></td>
            <td bind="ACC_TRDVAL" name="ACC_TRDVAL"></td>
            <td bind="ACC_OPNINT_QTY" name="ACC_OPNINT_QTY"></td>
            </tr>
            </tbody>
            </table>
            </div>
    Returns
    -------
    div_map : dict
    Examples :
        {
         'ISU_SRT_CD': '종목코드',
         'ISU_NM': '종목명',
         'TDD_CLSPRC': '종가',
         'CMPPREVDD_PRC': '대비',
         'TDD_OPNPRC': '시가',
         'TDD_HGPRC': '고가',
         'TDD_LWPRC': '저가',
         'SPOT_PRC': '현물가',
         'SETL_PRC': '정산가',
         'ACC_TRDVOL': '거래량',
         'ACC_TRDVAL': '거래대금',
         'ACC_OPNINT_QTY': '미결제약정'
        }
    """
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
