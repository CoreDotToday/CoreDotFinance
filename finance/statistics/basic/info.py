import json
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup as bs

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

    def requests_data(self, data, new_col_map=None):

        data['MIME Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        data['csvxls_isNo'] = 'false'

        jsp_soup, tag = self.get_jsp_soup(data)
        new_col_map = self.find_column_name(jsp_soup, tag)
        modified_data = self.input_to_value(jsp_soup, data)
        r = requests.post(self.url, data=modified_data, headers=self.headers)
        data = json.loads(r.content)

        return data, new_col_map

    def input_to_value(self, soup, data):
        # print(data)
        anwser_map = self.get_answer_map(soup)
        for key in data.keys():
            inner = anwser_map.get(key, None)
            if inner is not None:
                user_input = data[key]
                value = inner[user_input]
                data[key] = value

        if 'searchType' in data.keys():
            searchtype = data['searchType']
            if searchtype == 'A':
                searchtype = '1'
            elif searchtype == 'P':
                searchtype = '2'
            bld = data['bld']
            new_bld = bld[:-1] + searchtype
            data['bld'] = new_bld
            # print(data)
        return data

    def get_jsp_soup(self, data):
        bld = data['bld']
        tag = bld.split('/')[-1][:-2]
        url = f'http://data.krx.co.kr/contents/MDC/STAT/standard/{tag}.jsp'
        html = requests.get(url)
        soup = bs(html.content, 'html.parser')
        return soup, tag

    def find_column_name(self, soup, tag):
        a = soup.find('div', {'id': f'jsGrid_{tag}_0'}).thead
        b = a.find_all('th')
        dic = {}
        for i in b:
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
                dic[key]['text'] = f'{parent_name}{child_name}'
                p_list.add(p)
        [dic.pop(p) for p in p_list]
        for d in dic:
            dic[d] = dic[d]['text']
        return dic

    def get_answer_map(self, soup):
        select = soup.find_all('select')
        label = soup.find_all('label')
        input_ = soup.find_all('input')

        label_map = {}
        for i in label:
            label_map[i.attrs['for']] = i.text

        answer = {}
        for i in input_:
            if i.attrs['value'] != '':
                inner = answer.setdefault(i.attrs['name'], {})
                text = label_map.get(i.attrs['id'], None)
                if text is not None:
                    inner[text] = i.attrs['value']

        for s in select:
            if s.attrs['class'] == ['selectbox']:
                result = self.function_(s)
                answer[s.attrs['name']] = result
            else:
                answer[s.attrs['name']] = {s.text: s.next.attrs['value']}

        no_use = []
        for key in answer.keys():
            if len(answer[key]) == 0:
                no_use.append(key)
        for no in no_use:
            answer.pop(no)
        # print(answer)
        return answer

    def function_(self, s):
        the_script = s.next.next
        extaction = str(the_script).split('baseName:')[1].split('}')[0]
        for e in extaction.split('\''):
            if 'krx' in e:
                baseName = e
            elif 'bld' in e:
                key = e
        market = 'kospi'
        efrb = f'http://data.krx.co.kr/comm/bldAttendant/executeForResourceBundle.cmd?baseName={baseName}&key={key}&type={market}'
        html = requests.get(efrb)
        soup = bs(html.content, 'html.parser')
        the = json.loads(str(soup))
        new = the['result']['output']
        result = {}
        for n in new:
            result[n['name']] = n['value']
        return result

    def read(self):
        return self.function()
