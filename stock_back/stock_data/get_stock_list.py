import tushare as ts
import pandas

stock_list_path = "data/stock_list/list.csv"


if __name__ == '__main__':
    df = ts.get_stock_basics()
    df.to_csv(stock_list_path)

    df = pandas.read_csv(stock_list_path, encoding="utf8")
    print(df)