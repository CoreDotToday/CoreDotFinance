import json

with open('finance/code_to_menuId.json', 'r', encoding='utf-8') as f:
    code_to_menuId = json.load(f)

index_code_list_stock = ['11001', '11002', '11003', '11004', '11005', '11006', '11007_a', '11007_b']
index_code_list_bond = ['11008', '11009']
index_code_list_derivation = ['11010', '11011', '11012', '11013', '11014']

stock_code_list_item = ['12001', '12002', '12003', '12004']
stock_code_list_info = ['12005', '12006', '12007']
stock_code_list_trade = ['12008', '12009', '12010', '12011', '12012']
stock_code_list_others = ['12013', '12014', '12015', '12016', '12017', '12018', '12019']
stock_code_list_detail = ['12020', '12021', '12022', '12023', '12024', '12025', '12026', '12027', '12028']


stock_code_list = [code for code in range(12001, 120029)]
product_code_list = [code for code in range(13001, 13313)]
bond_code_list = [code for code in range(14001, 14028)]
derivative_code_list = [code for code in range(15001, 15018)]

code_list = [code for code in code_to_menuId.keys()]





