import requests
import pytest
import bs4

from coredotfinance.krx.core import webio


def test_get():
    res = webio.get("http://www.example.com")
    assert type(res) == bs4.BeautifulSoup


def test_post():
    res = webio.post("http://www.example.com", data={}, soup=True)
    assert type(res) == bs4.BeautifulSoup


def test_status_ok():
    res = requests.get("http://www.example.com/wrong")
    with pytest.raises(ConnectionError):
        webio.status_ok(res)
