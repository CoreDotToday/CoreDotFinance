import json

#with open('finance/code_to_menuId.json', 'r', encoding='utf-8') as f:
#    code_to_menuId = json.load(f)

index_code_list_stock = ['11001', '11002', '11003', '11004', '11005', '11006', '11007_a', '11007_b']
index_code_list_bond = ['11008', '11009']
index_code_list_derivation = ['11010', '11011', '11012', '11013', '11014']

stock_code_list_item = ['12001', '12002', '12003', '12004']
stock_code_list_info = ['12005', '12006', '12007']
stock_code_list_trade = [str(code) for code in range(12008, 12013)]
stock_code_list_others = [str(code) for code in range(12013, 12020)]
stock_code_list_detail = [str(code) for code in range(12020, 12029)]
product_code_list_ETF = [str(code) for code in range(13101, 13118)]
product_code_list_ETN = [str(code) for code in range(13201, 13217)]
product_code_list_ELW = [str(code) for code in range(13301, 13313)]

stock_code_list = [code for code in range(12001, 120029)]
product_code_list = [code for code in range(13001, 13313)]
bond_code_list = [code for code in range(14001, 14028)]
derivative_code_list = [code for code in range(15001, 15018)]

#code_list = [code for code in code_to_menuId.keys()]





