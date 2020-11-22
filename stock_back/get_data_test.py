from stock_data.data_processing.GetData import *

if __name__ == '__main__':
    gd = GetData('000002')

    print(gd.get_data('货币资金(万元)', 2019))
    print(gd.get_data('销售商品、提供劳务收到的现金(万元)', 2019))
    print(gd.get_data('营业总收入(万元)', 2019))
