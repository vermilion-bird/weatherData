import gzip


# gz
# 因为gz一般仅仅压缩一个文件，全部常与其它打包工具一起工作。比方能够先用tar打包为XXX.tar,然后在压缩为XXX.tar.gz
# 解压gz，事实上就是读出当中的单一文件

def un_gz(gz_file, ungz_file):
    """
    :param gz_file: gz压缩文件
    :param ungz_file: 解压后文件
    :return:
    """
    # f_name = gz_file.replace(".gz", "")
    # 获取文件的名称，去掉
    g_file = gzip.GzipFile(gz_file)
    # 创建gzip对象
    open(ungz_file, "w+").write(g_file.read().decode())
    # gzip对象用read()打开后，写入open()建立的文件里。
    g_file.close()
    # 关闭gzip对象
