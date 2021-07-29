def is_ok_to_adjust(code):
    available_code_list = [
        '12003'
    ]
    if code in available_code_list:
        return True
    else:
        return False


def adjust_price(code, dataframe):
    # column has to be Korean column name
    if not is_ok_to_adjust(code):
        Warning("This data is not available to get adjusted price")
        return dataframe

    standard_ratio = dataframe['상장주식수'][0] / dataframe['상장주식수']
    available_column_list = ['종가', '대비', '시가', '고가', '저가', '거래량']
    for column in available_column_list:
        data = dataframe.get(column, None)
        if data is None:
            continue
        if column == '거래량':
            # volume only needs to be multiplied by standard_ratio
            dataframe[column] = data * standard_ratio
        else:
            dataframe[column] = data / standard_ratio
    return dataframe





