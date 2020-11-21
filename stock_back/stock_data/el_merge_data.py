from data_processing.MergeData import *

stock_list_path = "data/stock_list/list.csv"
report_path = "data/finance"


if __name__ == '__main__':
    md = MergeData(report_path, stock_list_path)

    md.merge()