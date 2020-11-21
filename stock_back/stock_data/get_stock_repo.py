import pandas
import threadpool

from data_processing.DownloadReport import *

stock_list_path = "data/stock_list/list.csv"

if __name__ == '__main__':
    df = pandas.read_csv(stock_list_path, encoding="utf8")
    fromat_f = lambda x: '%06d' % x
    df['code'] = df['code'].apply(fromat_f)
    codes = df['code'].tolist()

    dr = DownloadReport("data/finance")

    func = dr.download_report

    args = list()

    nones = [None for i in range(len(codes))]
    args = zip(zip(codes), nones)

    pool_size = 4
    pool = threadpool.ThreadPool(pool_size)
    requests = threadpool.makeRequests(func, args)
    [pool.putRequest(req) for req in requests]
    pool.wait()

    pool.dismissWorkers(pool_size, do_join=True)

