import sys

finance_path = sys.path[0].replace('/test', '')
sys.path.append(finance_path)

from finance import dataframing

def test_data_validation():
    pass

def test_column