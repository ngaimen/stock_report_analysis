import tushare
import pandas
import threadpool

hist_data_path = "data/history/hist_data/hist_data_{0}.csv"
hist_w_data_path = "data/history/hist_data/hist_data_w_{0}.csv"

codes_list = "data/stock_list/etf.csv"

codes = ["162411", "513050"]
def get_hist_data(code):
    print(code)
    df = tushare.get_hist_data(code)
    df.to_csv(hist_data_path.format(code))

    df = tushare.get_hist_data(code, ktype='W')
    df.to_csv(hist_w_data_path.format(code))


if __name__ == "__main__":
    df = pandas.read_csv(codes_list)
    df["基金代码"] = df["基金代码"].apply(str)
    print(df)
    print(codes)
    codes += df["基金代码"].tolist()
    print(codes)
    func = get_hist_data

    args = list()

    nones = [None for i in range(len(codes))]
    args = zip(zip(codes), nones)

    pool_size = 4
    pool = threadpool.ThreadPool(pool_size)
    requests = threadpool.makeRequests(func, args)
    [pool.putRequest(req) for req in requests]
    pool.wait()

    pool.dismissWorkers(pool_size, do_join=True)
