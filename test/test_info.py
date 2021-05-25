from coredotfinance.krx.krx_website.info import Info


# testing for checking '&' having word, kt&g
def test_autocomplete_stock_1():
    assert Info(None, None, None).autocomplete("kt&g", "stock") == (
        "KT&G",
        "KR7033780008",
        "033780",
    )


# testing for checking word priority, 바이온
def test_autocomplete_stock_2():
    assert Info(None, None, None).autocomplete("바이온", "stock") == (
        "바이온",
        "KR7032980005",
        "032980",
    )


def test_autocomplete_index():
    assert Info(None, None, None).autocomplete("zhtmvl", "index") == ("코스피", "1", "001")


def test_autocomplete_ETF():
    assert Info(None, None, None).autocomplete("arirang alrnrsk", "ETF") == (
        "ARIRANG 미국나스닥기술주",
        "KR7287180004",
        "287180",
    )


def test_autocomplete_ETN():
    assert Info(None, None, None).autocomplete("qv 미국", "ETN") == (
        "QV 미국 IT TOP5 ETN(H)",
        "KRG552100411",
        "550041",
    )


def test_autocomplete_ELW():
    assert Info(None, None, None).autocomplete("37tkatjdwjswk", "ELW") == (
        "KBF937삼성전자콜",
        "KRA5811BKA77",
        "58F937",
    )


def test_autocomplete_dericative():
    assert Info(None, None, None).autocomplete("a", "derivative") == (
        "ARIRANG 고배당 F 202106",
        "KR41M2R60003",
        "1M2R6000",
    )


def test_autocomplete_publish():
    assert Info(None, None, None).autocomplete("a", "publish") == (
        "AJ네트웍스",
        "09557",
        "09557",
    )
