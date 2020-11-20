import backtrader
import pandas
import datetime
import os

def get_data(csv):
    data = backtrader.feeds.GenericCSVData(
        dataname=csv,
        fromdate=datetime.datetime(2018, 1, 1),
        todate=datetime.datetime(2020, 12, 31),

        nullvalue=0.0,

        dtformat=('%Y-%m-%d'),

        datetime=1,
        high=3,
        low=5,
        open=2,
        close=4,
        volume=6,
        openinterest=-1
    )

    return data


def generic_data(stock_code):
    hist_data_path = "data/history/hist_data/hist_data_{0}.csv"
    bt_data_path = "data/history/bt_data/{0}.csv"

    dest = bt_data_path.format(stock_code)

    df = pandas.read_csv(hist_data_path.format(stock_code), encoding="utf8")
    df = df.iloc[::-1]

    if not os.path.exists(dest):
        df.to_csv(dest)

    return get_data(dest)


def generic_week_data(stock_code):
    hist_data_path = "data/history/hist_data/hist_data_w_{0}.csv"
    bt_data_path = "data/history/bt_data/w_{0}.csv"

    dest = bt_data_path.format(stock_code)

    df = pandas.read_csv(hist_data_path.format(stock_code), encoding="utf8")
    df = df.iloc[::-1]

    if not os.path.exists(dest):
        df.to_csv(dest)

    return get_data(dest)
