import pandas
import os


class MergeData:
    def __init__(self, path, code_list_path):
        self.__data_root = path
        self.__code_list_path = code_list_path

    def merge(self):
        df = pandas.read_csv(self.__code_list_path, encoding='utf8')

        format_func = lambda x: '%06d' % x
        df['code'] = df['code'].apply(format_func)

        df = df.iloc[:, 0:4]

        print(df)

        for code_index, row in df.iterrows():
            df = self.__merge_balance(df, row['code'], code_index, 'balance')
            df = self.__merge_balance(df, row['code'], code_index, 'cash_flow')
            df = self.__merge_balance(df, row['code'], code_index, 'income')

        df.to_csv(os.path.join(self.__data_root, 'result.csv'), encoding='utf8')

    def __merge_balance(self, df, code, index, r_type):
        path = os.path.join(self.__data_root, r_type)
        path = os.path.join(path, code + '.csv')

        r_df = pandas.read_csv(path, encoding='gbk', index_col=0)

        r_df = r_df.T

        # 按行去遍历报表，并写入到总的df中
        for row_index, row in r_df.iterrows():
            # 只要年报的数据
            if str(row_index).endswith('12-31'):
                year = str(row_index)[0:4]

                for col_index in r_df.columns:
                    df.loc[index, col_index + year] = row[col_index]

        return df

