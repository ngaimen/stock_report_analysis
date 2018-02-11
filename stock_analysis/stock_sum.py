import os
import urllib
from time import sleep
from datetime import datetime

import pandas as pd
import tushare

class stock_sum():

    """报表数据汇总类

    Parameters
    --------------
    __year  报表年份
    __m_d 报表月日
    __floder 报表源目录
    --------------
    """
    def __init__(self, year, month_day, bb_floder):
        self.__year = year
        self.__m_d = month_day
        self.__floder = bb_floder
        self.__today = str(datetime.now())[:10]

    def summary_report(self):
        stock_list_path = os.path.join(self.__floder, '股票列表%s.csv' % (self.__today))

        if not os.path.exists(stock_list_path):
            data = tushare.get_stock_basics()
            lie = ['名字', '行业', '地区', '市盈率', '流通股本', '总股本',
                   '总资产(万)', '流动资产', '固定资产', '公积金', '每股公积金', '每股收益', '每股净资',
                   '市净率', '上市日期', '未分利润', '每股未分配', '收入同比(%)', '利润同比(%)',
                   '毛利率(%)', '净利润率(%)', '股东人数']
            data.columns = lie
            data.index.names = ['代码']
            data.to_csv(stock_list_path, encoding='utf-8')

        data = pd.read_csv(stock_list_path, encoding='utf-8', index_col=0)
        if self.__m_d == '-12-31':
            data = data[data['上市日期'] < (self.__year - 1) * 10000]
        else:
            data = data[data['上市日期'] < (self.__year - 2) * 10000]

        data = data[data['上市日期'] > 1989 * 10000]

        data = self.__add_cwbb_data(data, self.__year)

        data.to_csv(
            os.path.join(self.__floder, '%s%s财务指标分析汇总.csv' % (self.__year, self.__m_d)), encoding='utf-8')

    def get_summary_report_data(self):
        report_path = os.path.join(self.__floder, '%s%s财务指标分析汇总.csv' % (self.__year, self.__m_d))
        if not os.path.exists(report_path):
            self.summary_report()

        return pd.read_csv(report_path, encoding='utf-8', index_col=0)

    def __download_report(self, code):
        url = 'http://quotes.money.163.com/service/zcfzb_%s.html?type=report' % code
        path = os.path.join(self.__floder, 'zcfzb')
        self.__create_folder_if_need(path)
        self.__download_if_need(code, url, path)

        url = 'http://quotes.money.163.com/service/lrb_%s.html?type=report' % code
        path = os.path.join(self.__floder, 'lrb')
        self.__create_folder_if_need(path)
        self.__download_if_need(code, url, path)

        url = 'http://quotes.money.163.com/service/xjllb_%s.html?type=report' % code
        path = os.path.join(self.__floder, 'xjllb')
        self.__create_folder_if_need(path)
        self.__download_if_need(code, url, path)

    def __create_folder_if_need(self, path):
        if not os.path.exists(path):  # 如果该文件夹不存在，创建文件夹
            os.makedirs(path)
        elif not os.path.isdir(path):
            os.makedirs(path)

    def __download_if_need(self, code, url, folder):
        path = os.path.join(folder, code + '.csv')
        if not os.path.exists(path):
            urllib.request.urlretrieve(url, path)
            sleep(1.5)  # 间隔一段时间，防止服务器关闭连接

    def __add_cwbb_data(self, data, year):
        data['经营活动产生的现金流量净额(万元)' + str(year)] = 0
        data['经营活动产生的现金流量净额(万元)' + str(year - 1)] = 0
        data['经营活动产生的现金流量净额(万元)' + str(year - 2)] = 0

        data['投资活动产生的现金流量净额(万元)' + str(year)] = 0
        data['投资活动产生的现金流量净额(万元)' + str(year - 1)] = 0
        data['投资活动产生的现金流量净额(万元)' + str(year - 2)] = 0

        data['筹资活动产生的现金流量净额(万元)' + str(year)] = 0
        data['筹资活动产生的现金流量净额(万元)' + str(year - 1)] = 0
        data['筹资活动产生的现金流量净额(万元)' + str(year - 2)] = 0

        data['现金及现金等价物的净增加额(万元)' + str(year)] = 0
        data['现金及现金等价物的净增加额(万元)' + str(year - 1)] = 0
        data['现金及现金等价物的净增加额(万元)' + str(year - 2)] = 0

        data['有息负债(万元)'] = 0
        data['非主业资产(万元)'] = 0
        data['生产资产(万元)'] = 0
        data['货币资金(万元)'] = 0
        data['应收款(万元)'] = 0
        data['其他应收款(万元)'] = 0
        data['其他应付款(万元)'] = 0

        data['利润总额(万元)'] = 0
        data['净利润(万元)' + str(year)] = 0
        data['净利润(万元)' + str(year - 1)] = 0
        data['净利润(万元)' + str(year - 2)] = 0
        data['营业总收入(万元)'] = 0
        data['营业外收入(万元)'] = 0
        data['营业总成本(万元)'] = 0
        data['营业外支出(万元)'] = 0
        data['资产减值损失(万元)'] = 0
        data['费用总和(万元)'] = 0
        data['平均利润(万元)'] = 0

        for index, row in data.iterrows():
            try:
                code = '%06d' % index
                self.__download_report(code)

                xjllb_data = pd.read_csv(os.path.join(os.path.join(self.__floder, 'xjllb'), code + '.csv'), encoding="gbk", index_col=0)
                xjllb_data = xjllb_data.T

                for i in range(year - 2, year + 1):
                    data.loc[index, '经营活动产生的现金流量净额(万元)' + str(i)] = \
                        float('--' == xjllb_data[' 经营活动产生的现金流量净额(万元)'][str(i) + self.__m_d]
                              and 0.00001 or xjllb_data[' 经营活动产生的现金流量净额(万元)'][str(i) + self.__m_d])

                    data.loc[index, '投资活动产生的现金流量净额(万元)' + str(i)] = \
                        float('--' == xjllb_data[' 投资活动产生的现金流量净额(万元)'][str(i) + self.__m_d]
                              and 0.00001 or xjllb_data[' 投资活动产生的现金流量净额(万元)'][str(i) + self.__m_d])

                    data.loc[index, '筹资活动产生的现金流量净额(万元)' + str(i)] = \
                        float('--' == xjllb_data[' 筹资活动产生的现金流量净额(万元)'][str(i) + self.__m_d]
                              and 0.00001 or xjllb_data[' 筹资活动产生的现金流量净额(万元)'][str(i) + self.__m_d])

                    data.loc[index, '现金及现金等价物的净增加额(万元)' + str(i)] = \
                        float('--' == xjllb_data[' 现金及现金等价物的净增加额(万元)'][str(i) + self.__m_d]
                              and 0.00001 or xjllb_data[' 现金及现金等价物的净增加额(万元)'][str(i) + self.__m_d])

                zcfzb_data = pd.read_csv(os.path.join(os.path.join(self.__floder, 'zcfzb'), code + '.csv'), encoding='gbk', index_col=0)
                zcfzb_data = zcfzb_data.T

                data.loc[index, '有息负债(万元)'] = \
                    float('--' == zcfzb_data['短期借款(万元)'][str(year) + self.__m_d] and 0.00001 or zcfzb_data['短期借款(万元)'][str(year) + self.__m_d]) \
                    + float('--' == zcfzb_data['长期借款(万元)'][str(year) + self.__m_d] and 0.00001 or zcfzb_data['长期借款(万元)'][str(year) + self.__m_d]) \
                    + float('--' == zcfzb_data['应付债券(万元)'][str(year) + self.__m_d] and 0.00001 or zcfzb_data['应付债券(万元)'][str(year) + self.__m_d])

                data.loc[index, '非主业资产(万元)'] = \
                    float('--' == zcfzb_data['可供出售金融资产(万元)'][str(year) + self.__m_d] and 0.00001 or zcfzb_data['可供出售金融资产(万元)'][str(year) + self.__m_d]) \
                    + float('--' == zcfzb_data['持有至到期投资(万元)'][str(year) + self.__m_d] and 0.00001 or zcfzb_data['持有至到期投资(万元)'][str(year) + self.__m_d])

                data.loc[index, '生产资产(万元)'] = \
                    float('--' == zcfzb_data['固定资产(万元)'][str(year) + self.__m_d] and 0.00001 or zcfzb_data['固定资产(万元)'][str(year) + self.__m_d]) \
                    + float('--' == zcfzb_data['在建工程(万元)'][str(year) + self.__m_d] and 0.00001 or zcfzb_data['在建工程(万元)'][str(year) + self.__m_d]) \
                    + float('--' == zcfzb_data['工程物资(万元)'][str(year) + self.__m_d] and 0.00001 or zcfzb_data['工程物资(万元)'][str(year) + self.__m_d])

                data.loc[index, '货币资金(万元)'] = \
                    float('--' == zcfzb_data['货币资金(万元)'][str(year) + self.__m_d] and 0.00001 or zcfzb_data['货币资金(万元)'][str(year) + self.__m_d])

                data.loc[index, '其他应收款(万元)'] = \
                    float('--' == zcfzb_data['其他应收款(万元)'][str(year) + self.__m_d] and 0.00001 or zcfzb_data['其他应收款(万元)'][str(year) + self.__m_d])

                data.loc[index, '其他应付款(万元)'] = \
                    float('--' == zcfzb_data['其他应付款(万元)'][str(year) + self.__m_d] and 0.00001 or zcfzb_data['其他应付款(万元)'][str(year) + self.__m_d])

                data.loc[index, '应收款(万元)'] = \
                    float('--' == zcfzb_data['应收票据(万元)'][str(year) + self.__m_d] and 0.00001 or zcfzb_data['应收票据(万元)'][str(year) + self.__m_d]) \
                    + float('--' == zcfzb_data['应收账款(万元)'][str(year) + self.__m_d] and 0.00001 or zcfzb_data['应收账款(万元)'][str(year) + self.__m_d]) \
                    + float('--' == zcfzb_data['其他应收款(万元)'][str(year) + self.__m_d] and 0.00001 or zcfzb_data['其他应收款(万元)'][str(year) + self.__m_d])

                lrb_data = pd.read_csv(os.path.join(os.path.join(self.__floder, 'lrb'), code + '.csv'), encoding='gbk', index_col=0)
                lrb_data = lrb_data.T

                average_profit = 0
                for i in range(year - 2, year + 1):
                    data.loc[index, '净利润(万元)' + str(i)] = \
                        float('--' == lrb_data['净利润(万元)'][str(i) + self.__m_d]
                              and 0.00001 or lrb_data['净利润(万元)'][str(i) + self.__m_d])

                    average_profit += data['净利润(万元)' + str(i)][index]

                data.loc[index, '平均利润(万元)'] = average_profit / 3

                data.loc[index, '利润总额(万元)'] = \
                    float('--' == lrb_data['利润总额(万元)'][str(year) + self.__m_d] and 0.00001 or lrb_data['利润总额(万元)'][str(year) + self.__m_d])

                data.loc[index, '营业总收入(万元)'] = \
                    float('--' == lrb_data['营业总收入(万元)'][str(year) + self.__m_d] and 0.00001 or lrb_data['营业总收入(万元)'][str(year) + self.__m_d])

                data.loc[index, '营业外收入(万元)'] = \
                    float('--' == lrb_data['营业外收入(万元)'][str(year) + self.__m_d] and 0.00001 or lrb_data['营业外收入(万元)'][str(year) + self.__m_d])

                data.loc[index, '营业总成本(万元)'] = \
                    float('--' == lrb_data['营业总成本(万元)'][str(year) + self.__m_d] and 0.00001 or lrb_data['营业总成本(万元)'][str(year) + self.__m_d])

                data.loc[index, '营业外支出(万元)'] = \
                    float('--' == lrb_data['营业外支出(万元)'][str(year) + self.__m_d] and 0.00001 or lrb_data['营业外支出(万元)'][str(year) + self.__m_d])

                data.loc[index, '资产减值损失(万元)'] = \
                    float('--' == lrb_data['资产减值损失(万元)'][str(year) + self.__m_d] and 0.00001 or lrb_data['资产减值损失(万元)'][str(year) + self.__m_d])

                data.loc[index, '费用总和(万元)'] = \
                    float('--' == lrb_data['销售费用(万元)'][str(year) + self.__m_d] and 0.00001 or lrb_data['销售费用(万元)'][str(year) + self.__m_d]) \
                    + float('--' == lrb_data['管理费用(万元)'][str(year) + self.__m_d] and 0.00001 or lrb_data['管理费用(万元)'][str(year) + self.__m_d]) \
                    + float('--' == lrb_data['财务费用(万元)'][str(year) + self.__m_d] and 0.00001 or lrb_data['财务费用(万元)'][str(year) + self.__m_d]) \
                    + float('--' == lrb_data['研发费用(万元)'][str(year) + self.__m_d] and 0.00001 or lrb_data['研发费用(万元)'][str(year) + self.__m_d]) \
                    + float('--' == lrb_data['分保费用(万元)'][str(year) + self.__m_d] and 0.00001 or lrb_data['分保费用(万元)'][str(year) + self.__m_d])

            except Exception as e:
                print(code)
                print(str(e))

        return data

