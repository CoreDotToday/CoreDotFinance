import json

with open('finance/code_to_menuId.json', 'r', encoding='utf-8') as f:
    code_to_menuId = json.load(f)

index_code_list = [code for code in range(11001, 110015)]
stock_code_list = [code for code in range(12001, 120029)]
product_code_list = [code for code in range(13001, 13313)]
bond_code_list = [code for code in range(14001, 14028)]
derivative_code_list = [code for code in range(15001, 15018)]

code_list = [code for code in code_to_menuId.keys()]





