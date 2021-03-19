import json

#with open('finance/code_to_menuId.json', 'r', encoding='utf-8') as f:
#    code_to_menuId = json.load(f)

index_code_list_stock = ['11001', '11002', '11003', '11004', '11005', '11006', '11007']
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

bond_code_list_price = ['14001', '14002']
bond_code_list_info = ['14003', '14004']
bond_code_list_trade = ['14005', '14006', '14007', '14008']
bond_code_list_detail = [str(code) for code in range(14009, 14028)]


derivative_code_list_price = ['15001', '15002', '15003']
derivative_code_list_info = ['15004', '15005']
derivative_code_list_trade = ['15006', '15007', '15008', '15009']
derivative_code_list_detail = [str(code) for code in range(15010, 15017)]


commodity_code_list_oil = [str(code) for code in range(16101, 16106)]
commodity_code_list_gold = [str(code) for code in range(16201, 16208)]
commodity_code_list_carbonemission = [str(code) for code in range(16301, 16305)]

oversees_code_list_euro = [str(code) for code in range(17101, 17109)]

#code_list = [code for code in code_to_menuId.keys()]





