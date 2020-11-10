# encoding:utf-8
import datetime
import logging
import os
import re
from util.FileHelp import un_gz
from util.FtpHelp import FtpHelp
from config import BASE_DIR, FTP_HOST, FTP_FILE_PATH, INTERVAL
# 日志
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
logger_handler = logging.FileHandler("logs")
logger.addHandler(logger_handler)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger_handler.setFormatter(formatter)

def main():
    """
    程序入口
    :return:
    """

    try:
        year = str(datetime.datetime.now().year)
        basic_path = BASE_DIR
        with FtpHelp(FTP_HOST) as fh:
            dirs = fh.dirs(FTP_FILE_PATH.format(year))
            dirs = [i for i in dirs if i.startswith('5')]  # 5开头为中国气象站
            for dir_name in dirs:
                fh.download(FTP_FILE_PATH.format(year), dir_name, save_path=basic_path + 'gz/' + dir_name)
                file_name = dir_name
                un_gz(basic_path + 'gz/' + file_name, basic_path + 'ungz/' + file_name.replace(".gz", ""))
                os.system('java -classpath . ishJava {} {}'.format(basic_path + 'ungz/' + file_name.replace('.gz', ''),
                                                                   basic_path + 'out/' + file_name.replace('.gz',
                                                                                                           '') + '.out'))
        logger.error('运行正常')
    except Exception as e:
        logger.error('运行异常'+str(e))

if __name__ == '__main__':
    main()
