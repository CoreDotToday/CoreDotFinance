import json
import re
import logging

from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup as bs
from finance.dataframing import GettingDataNm


class Info:
    def __init__(self, start, end, day):
        """ 지수
        :param start: 시작일
        :param end: 종료일
        :param day: 기준일
        """
        today = datetime.now()
        a_month_ago = today - timedelta(days=60)
        self.start = a_month_ago.strftime('%Y%m%d') if start is None else str(start)
        self.end = today.strftime('%Y%m%d') if end is None else str(end)
        self.day = today.strftime('%Y%m%d') if day is None else str(day)

        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15'
        }
        self.url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'

    def requests_data(self, data):
        print('in requests_data')
        print('data\n\n', data, '\n')
        data['MIME Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        data['csvxls_isNo'] = 'false'

        jsp_soup, mdcstat = self.get_jsp_soup(data)
        readable_columns = self.get_readable_columns(jsp_soup, mdcstat)
        modified_data = self.input_to_value(jsp_soup, data)
        r = requests.post(self.url, data=modified_data, headers=self.headers)

        try:
            data = json.loads(r.content)
        except json.JSONDecodeError as e:
            logger = logging.getLogger('log')
            logger.info(f'\tdata:\t{data}\n'
                        f'error:\t{e}\n'
                        f'status code:\t{r.status_code}'
                        f'response:\t{r}')

        return data, readable_columns

    def autocomplete(self, item_name, item_type):
        if item_name is None:
            return None, None, None
        if '&' in item_name:
            # url에 item_name 문자열을 적용시키기 위 '&'를 변환시킴
            item_name = item_name.replace('&', '%2526')

        autocomplete_urls = {
            'index': 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_equidx&value={item_name}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_equidx_autocomplete',
            'stock': 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_stkisu&value={item_name}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_stkisu_autocomplete',
            'ETF': 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_secuprodisu_etf&value={item_name}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_secuprodisu_etf_autocomplete',
            'ETN': 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_secuprodisu_etn&value={item_name}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_secuprodisu_etn_autocomplete',
            'ELW': 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_secuprodisu_elw&value={item_name}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_secuprodisu_elw_autocomplete',
            'derivative': 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_drvprodisu&value={item_name}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_drvprodisu_autocomplete',
            'publish': 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_bndordisu&value={item_name}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_bndordisu_autocomplete',
            'bond': 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_bondisu&value={item_name}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_bondisu_autocomplete'
        }
        autocomplete_response = requests.get(autocomplete_urls[item_type].format(item_name=item_name))
        soup = bs(autocomplete_response.content, 'html.parser')
        print("\nin autocomple\nsoup\n", soup) # Change the name soup to be more obvious

        if soup is None:
            raise AttributeError(f'{item_name} is Wrong name as a stock name')
        item_scripts = soup.find_all('li')
        print('What is soup_list??\nsoup_list\n', item_scripts)
        # item 입력값이 autocomplete 에서 반환해주는 soup에서 첫번째에 위치하지 않는 경우가 있다. (예 "바이온")
        # 따라서 입력된 item이 autocomlete 내에 있으면 그 soup을 반환해주는 기능을 구현한다.
        item_names = [script.attrs['data-nm'] for script in item_scripts]
        if item_name in item_names:
            index = item_names.index(item_name)
            item_script = item_scripts[index]
        else:
            item_script = item_scripts[0]
        GettingDataNm().data_nm = item_script.attrs['data-nm']
        return item_script.attrs['data-nm'], item_script.attrs['data-cd'], item_script.attrs['data-tp']

    def get_readable_columns(self, jsp_soup, mdcstat):
        map_ = {}
        jsGird_dict = self.parse_jspGrid_dict(jsp_soup)
        jsGrid = jsGird_dict[mdcstat]

        table_tag = jsp_soup.find('table', {'id': jsGrid})
        div_tag = jsp_soup.find('div', {'id': jsGrid})

        if table_tag:
            table_map = self.get_table_map(table_tag)
            map_.update(table_map)
        if div_tag:
            div_map = self.get_div_map(div_tag)
            map_.update(div_map)
        return map_

    def input_to_value(self, soup, data):
        answer_map = self.parse_answer_map(soup)
        for key in data.keys():
            inner = answer_map.get(key, None)
            if inner is not None:
                user_input = data[key]
                value = inner.get(user_input, None)
                data[key] = value
        return data

    def get_jsp_soup(self, data):
        # FIXME: you can split it as 2 functions. -> def parse_mdcstat/ def get_jsp_soup
        bld = data['bld']
        mdcstat = bld.split('/')[-1]
        jsp_filename = mdcstat[:-2]
        url = f'http://data.krx.co.kr/contents/MDC/STAT/standard/{jsp_filename}.jsp'
        html = requests.get(url)
        jsp_soup = bs(html.content, 'html.parser')
        return jsp_soup, mdcstat

    def get_table_map(self, table_tag):
        print('in get_table_map\ntable_tag\n', table_tag)
        dic = {}
        # TODO : Change the dictionary name, dic.
        for tr in table_tag.find_all('tr'):
            th = tr.find_all('th')
            td = tr.find_all('td')
            for name, id in zip(th, td):
                dic[id.attrs['data-bind']] = name.text
        return dic

    def parse_jspGrid_dict(self, jsp_soup):
        jscode_list = jsp_soup.find_all('script')
        for s in jscode_list:
            # TODO : change the variable, s
            #  What is s?
            if 'jsGrid' in str(s):
                jscode = s
                break
        jscode_str = str(jscode)
        mdcstat_list = re.findall(r'template: \$content\.select\(\'\#(jsGrid_MDCSTAT[0-9]*\_[0-9])', jscode_str)
        bld_list = re.findall(r'bld: \'dbms/MDC/STAT/standard/(MDCSTAT[0-9]*)', jscode_str)
        jsGrid_dict = {}
        for mdcstat, bld in zip(mdcstat_list, bld_list):
            lis = jsGrid_dict.setdefault(bld, [])
            lis.append(mdcstat)
        return jsGrid_dict

    def get_div_map(self, div_tag):
        thead = div_tag.thead
        if thead is None:
            return {}
        tag_list = []
        tag_list.extend(thead.find_all('th'))
        tag_list.extend(thead.find_all('td'))

        dic = {}
        for i in tag_list:
            dic[i.attrs['name']] = {
                'text': i.text,
                'parent': i.attrs.get('parent', None)
            }

        p_list = set()
        for key in dic:
            p = dic[key]['parent']

            if p is not None:
                child_name = dic[key]['text']
                parent_name = dic[p]['text']
                dic[key]['text'] = f'{parent_name}//{child_name}'

                p_list.add(p)
        [dic.pop(p) for p in p_list]
        for d in dic:
            dic[d] = dic[d]['text']
        return dic

    def parse_answer_map(self, soup):
        select = soup.find_all('select')
        label = soup.find_all('label')
        input_ = soup.find_all('input')
        label_map = {}
        for i in label:
            label_map[i.attrs['for']] = i.text

        answer = {}
        for i in input_:
            if i.attrs.get('value', None) != '':
                inner = answer.setdefault(i.attrs['name'], {})
                text = label_map.get(i.attrs.get('id', None), None)
                if text is not None:
                    inner[text] = i.attrs.get('value', None)

        for select_tag in select:
            if select_tag.attrs.get('name', None) in ['bndClssCd', 'isurCd', 'idxIndCd', 'prodId', 'isuCd', 'selecbox', 'invstTpCd']: # [14021], [15001], [15007]
                result = self.execute_for_resource_bundle(select_tag)
                answer[select_tag.attrs['name']] = result
            elif select_tag.find_all('option') != '':
                dic = {}
                for option in select_tag.find_all('option'):
                    dic[option.text] = option.attrs['value']
                answer[select_tag.attrs['name']] = dic
            else:
                answer[select_tag.attrs['name']] = {select_tag.text: select_tag.next.attrs['value']}

        no_use = []
        for key in answer.keys():
            if len(answer[key]) == 0:
                no_use.append(key)
        for no in no_use:
            answer.pop(no)
        return answer

    def execute_for_resource_bundle(self, s):
        the_script = s.next.next
        extaction = str(the_script).split('baseName:')[1].split('}')[0]
        for e in extaction.split('\''):
            if 'krx' in e:
                baseName = e
            elif 'bld' in e:
                key = e
        market = 'kospi'
        efrb_url = f'http://data.krx.co.kr/comm/bldAttendant/executeForResourceBundle.cmd?baseName={baseName}&key={key}&type={market}'
        html = requests.get(efrb_url)
        soup = bs(html.content, 'html.parser')
        the = json.loads(str(soup))
        new = the['result']['output']
        result = {}
        for n in new:
            result[n['name']] = n['value']
        return result



