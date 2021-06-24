import pickle

# test_is to avoid a conflict
# btw same file name(.py) and function name(def .

"""
bundle_for_test 는 coredotcoredotfinance.krx.'15001', item='코스피200 선물', market='전체') 20210430 에 만들었다.
"""

with open("test/test_data_reader.bin", "rb") as f:
    data = pickle.load(f)

requested_data = data["requested_data"]
mdcstat = data["mdcstat"]
jsp_soup = data["jsp_soup"]
krx_data = data["krx_data"]
efrb_url = data["efrb_url"]
resource_bundle = data["resource_bundle"]
converting_map = data["converting_map"]
len_zero_converting_map = data["len_zero_converting_map"]
valid_requested_data = data["valid_requested_data"]
jsGrid_dict = data["jsGrid_dict"]

# FIXME: tag can not be pickled.
# select_tag = bs(data['select_tag'])
# div_tag = bs(data['div_tag'])
# div_map = data['div_map']


def test_parse_mdcstat():
    assert parse_mdcstat(requested_data) == mdcstat


def test_get_jsp_soup():
    # Removes date data in jsp_soup
    result = str(get_jsp_soup(mdcstat))
    result = re.sub(r"SEARCH_COMPONENT__[0-9]*", "", result)
    result = re.sub(f'value="[0-9]*"', "", result)
    answer = str(jsp_soup)
    answer = re.sub(r"SEARCH_COMPONENT__[0-9]*", "", answer)
    answer = re.sub(f'value="[0-9]*"', "", answer)
    assert result == answer


def test_convert_valid_requested_data():
    assert (
        convert_valid_requested_data(jsp_soup, requested_data) == valid_requested_data
    )


def test_parse_converting_map():
    assert parse_converting_map(jsp_soup) == converting_map


def test_remove_len_zero():
    assert remove_len_zero(converting_map) == len_zero_converting_map


def test_get_resource_bundle():
    assert get_resource_bundle(efrb_url) == resource_bundle


def test_parse_jsGride_dict():
    assert parse_jsGrid_dict(jsp_soup) == jsGrid_dict


"""
def test_parse_efrb_url():
    assert parse_efrb_url(select_tag) == efrb_url
"""

# FIXME : No test data! If someone finds some functions using table_tag, Add that or tell Gukmoon.
"""
def test_parse_table_map():
    assert parse_table_map(table_tag) == table_map
"""

"""
def test_parse_div_map():
    assert parse_div_map(div_tag) == div_map
"""
