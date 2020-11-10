# encoding:utf-8
from ftplib import FTP  # 加载ftp模块


class FtpHelp:
    def __init__(self, ip=None, port=21, user=None, pwd=None):
        """

        :param ip:   ftp主机ip
        :param port: 端口
        :param user: 用户名
        :param pwd:  密码
        """

        self.ftp = FTP()  # 设置变量
        self.ip = ip
        self.port = port
        # ftp.set_debuglevel(2) #打开调试级别2，显示详细信息
        self.buf_size = 1024  # 设置的缓冲区大小

    def __enter__(self):
        self.ftp.connect(self.ip, self.port)
        self.ftp.login("anonymous", "password")  # 连接的用户名，密码
        return self

    def download(self, filepath, filename, save_path):
        """

        :param filepath: 文件路径
        :param filename: 文件名
        :param save_path: 保存路径
        :return:
        """

        # print(self.ftp.getwelcome())  # 打印出欢迎信息
        self.ftp.cwd(filepath)  # 进入远程目录
        file_handle = open(save_path, "wb").write  # 以写模式在本地打开文件
        self.ftp.retrbinary("RETR " + filename, file_handle, self.buf_size)  # 接收服务器上文件并写入本地文件
        # self.ftp.set_debuglevel(0)  # 关闭调试模式

    def dirs(self, filepath):
        """
        列出文件目录
        :param filepath:
        :return:
        """
        self.ftp.cwd(filepath)  # 进入远程目录
        x = []
        self.ftp.dir(lambda L: x.append(L.split()[-1]))
        return x

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ftp.quit()


if __name__ == '__main__':
    with FtpHelp('ftp.ncdc.noaa.gov') as fh:
        # fh.download('/pub/data/noaa/2019/', '010010-99999-2019.gz')
        print(fh.dirs('/pub/data/noaa/2019/'))
