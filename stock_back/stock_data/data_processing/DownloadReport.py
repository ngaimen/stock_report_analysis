import os
import urllib
import time
import urllib.request


class DownloadReport:

    def __init__(self, path):
        """
        path 为保存财务报表的路径
        """
        self.__floder = path

    @staticmethod
    def __create_folder_if_need(path):
        if not os.path.exists(path):  # 如果该文件夹不存在，创建文件夹
            os.makedirs(path)
        elif not os.path.isdir(path):
            os.makedirs(path)

    @staticmethod
    def __download_if_need(code, url, folder):
        path = os.path.join(folder, code + '.csv')
        if not os.path.exists(path):
            urllib.request.urlretrieve(url, path)
            time.sleep(1.5)  # 间隔一段时间，防止服务器关闭连接

    def download_report(self, code):
        url = 'http://quotes.money.163.com/service/zcfzb_%s.html?type=report' % code
        path = os.path.join(self.__floder, 'balance')
        self.__create_folder_if_need(path)
        self.__download_if_need(code, url, path)

        url = 'http://quotes.money.163.com/service/lrb_%s.html?type=report' % code
        path = os.path.join(self.__floder, 'income')
        self.__create_folder_if_need(path)
        self.__download_if_need(code, url, path)

        url = 'http://quotes.money.163.com/service/xjllb_%s.html?type=report' % code
        path = os.path.join(self.__floder, 'cash_flow')
        self.__create_folder_if_need(path)
        self.__download_if_need(code, url, path)
