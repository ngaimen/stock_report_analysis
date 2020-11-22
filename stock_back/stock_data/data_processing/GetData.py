import os
import pandas
import numpy


class GetData:
    def __init__(self, code):
        self.__code = code
        self.__data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/finance'))

        self.__balance = pandas.read_csv(os.path.join(self.__data_path, 'balance/' + code + '.csv'), encoding='gbk',
                                         index_col=0)
        self.__balance = self.__balance.T

        self.__cash_flow = pandas.read_csv(os.path.join(self.__data_path, 'cash_flow/' + code + '.csv'), encoding='gbk',
                                           index_col=0)
        self.__cash_flow = self.__cash_flow.T
        self.__cash_flow.columns = self.__cash_flow.columns.str.strip()

        # self.__cash_flow.to_csv(self.__data_path + '/test.csv', encoding='utf8')

        self.__income = pandas.read_csv(os.path.join(self.__data_path, 'income/' + code + '.csv'), encoding='gbk',
                                        index_col=0)
        self.__income = self.__income.T

        # print(self.__balance.columns)
        # print(self.__cash_flow.columns)
        # print(self.__income.columns)

        # print(self.__balance)
        # print(self.__cash_flow)
        # print(self.__income)

    def get_data(self, key, year):
        try:
            if key in self.__balance.columns:
                return self.__balance[key][str(year) + '-12-31']
            elif key in self.__cash_flow.columns:
                return self.__cash_flow[key][str(year) + '-12-31']
            elif key in self.__income.columns:
                return self.__income[key][str(year) + '-12-31']
        except Exception as e:
            return '0'
