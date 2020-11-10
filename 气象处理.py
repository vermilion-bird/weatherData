'''
author:zp
coding:UTF-8
date:20190530
'''
import os
import pandas as pd
import re

#露点转换为相对湿度函数
def cal_rhu(t,d):
    fuzhu_li = []
    for i in range(1,len(t)+1):
        tc = t[i]
        td = d[i]
        try:
            es = 6.11 * pow(10.0,7.5*tc/(237.7+tc))
            e = 6.11*pow(10.0,7.5*td/(237.7+td))
            rh=(e/es)*100
            fuzhu_li.append(rh)
        except:
            fuzhu_li.append('***')

    return fuzhu_li


def cope_weather(path,file):
    # 读取文件
    with open(path+file, encoding='utf-8') as f:
        data1 = f.readlines()

    # 处理每行中多余空格问题
    data2 = []
    for i in range(len(data1)):
        data2.append(data1[i].replace(' ', ','))

    # 处理每行数据
    data3 = []
    for i in range(len(data2)):
        test_data = data2[i]
        test = re.sub(',,+', ',', test_data)
        data3.append(test.lstrip(',').rstrip('\n').split(','))

    # 确定列名
    colum_name = data3[0]
    dff = pd.DataFrame(columns=colum_name)

    # 将读入数据插入到datafram中
    df_index = len(data3)
    for i in range(1, df_index):
        try:
            dff.loc[i] = data3[i]
        except:
            data3[i].insert(-3, data3[i][-3][0:5])
            data3[i][-3] = data3[i][-3][5:]
            dff.loc[i] = data3[i]

    dff2 = dff

    # 开始修改列名
    dff2 = dff2.rename(columns={'WBAN': 'STATION_CODE'})
    dff2['STATION_NAME'] = dff2['STATION_CODE']
    dff2['STATION_PROVINCE'] = dff2['STATION_CODE']
    dff2['STATION_CITY'] = dff2['STATION_CODE']
    dff2['STATION_COUNTY'] = dff2['STATION_CODE']
    dff2['STATION_LAT'] = dff2['STATION_CODE']
    dff2['STATION_LON'] = dff2['STATION_CODE']
    dff2['STP_MAX'] = dff2['STATION_CODE']
    dff2['STP_MIN'] = dff2['STATION_CODE']
    dff2['WIN_S_MAX'] = dff2['STATION_CODE']
    dff2['WIN_D_MAX'] = dff2['STATION_CODE']
    dff2['WIN_S_INS'] = dff2['STATION_CODE']
    dff2['WIN_D_INS'] = dff2['STATION_CODE']
    dff2['RHU'] = dff2['STATION_CODE']
    dff2['VAP'] = dff2['STATION_CODE']
    dff2['RHU_MIN'] = dff2['STATION_CODE']
    dff2 = dff2.rename(columns={'DIR': 'WIN_D_AVG'})
    dff2 = dff2.rename(columns={'SPD': 'WIN_S_AVG'})
    dff2 = dff2.rename(columns={'MAX': 'TEM_MAX'})
    dff2 = dff2.rename(columns={'MIN': 'TEM_MIN'})

    #     print(dff2.columns.values.tolist())
    # 删除不要的列
    delet_li_2 = ['GUS', 'CLG', 'SKC', 'L', 'M', 'H', 'MW', 'AW', 'W', 'ALT', 'PCPXX', 'SD']
    dff3 = dff2.drop(delet_li_2, axis=1, inplace=False)

    # print(dff3.columns.values.tolist())
    # 调整列顺序
    time = dff3.pop('YR--MODAHRMN')
    dff3.insert(1, 'YR--MODAHRMN', time)
    station_name = dff3.pop('STATION_NAME')
    dff3.insert(3, 'STATION_NAME', station_name)
    STATION_PROVINCE = dff3.pop('STATION_PROVINCE')
    dff3.insert(4, 'STATION_PROVINCE', STATION_PROVINCE)
    STATION_CITY = dff3.pop('STATION_CITY')
    dff3.insert(5, 'STATION_CITY', STATION_CITY)
    STATION_COUNTY = dff3.pop('STATION_COUNTY')
    dff3.insert(6, 'STATION_COUNTY', STATION_COUNTY)
    STATION_LAT = dff3.pop('STATION_LAT')
    dff3.insert(7, 'STATION_LAT', STATION_LAT)
    STATION_LON = dff3.pop('STATION_LON')
    dff3.insert(8, 'STATION_LON', STATION_LON)

    # 对列进行运算，转换为国内标准
    fuzhu_li = []
    for i in dff3['WIN_S_AVG']:
        if i == '***':
            fuzhu_li.append('***')
        else:
            fuzhu_li.append(int(i) * 0.44704)

    dff3['WIN_S_AVG'] = fuzhu_li

    fuzhu_li = []
    for i in dff3['VSB']:
        if i == '****':
            fuzhu_li.append('****')
        else:
            fuzhu_li.append(float(i) * 1.609)

    dff3['VSB'] = fuzhu_li

    fuzhu_li = []
    for i in dff3['PCP01']:
        if re.match('\*+', i):
            fuzhu_li.append('***')
        else:
            try:
                # print(float(i) * 25.4)
                fuzhu_li.append(float(i) * 25.4)
            except:
                fuzhu_li.append(0)

    dff3['PCP01'] = fuzhu_li

    fuzhu_li = []
    for i in dff3['PCP06']:
        if re.match('\*+', i):
            fuzhu_li.append('***')
        else:
            try:
                # print(float(i) * 25.4)
                fuzhu_li.append(float(i) * 25.4)
            except:
                fuzhu_li.append(0)

    dff3['PCP06'] = fuzhu_li

    fuzhu_li = []
    for i in dff3['PCP24']:
        if re.match('\*+', i):
            fuzhu_li.append('***')
        else:
            try:
                # print(float(i) * 25.4)
                fuzhu_li.append(float(i) * 25.4)
            except:
                fuzhu_li.append(0)

    dff3['PCP24'] = fuzhu_li

    fuzhu_li = []
    for i in dff3['TEMP']:
        if re.match('\*+', i):
            fuzhu_li.append('***')
        else:
            fuzhu_li.append((float(i) - 32) / 1.8)

    dff3['TEMP'] = fuzhu_li

    fuzhu_li = []
    for i in dff3['DEWP']:
        if re.match('\*+', i):
            fuzhu_li.append('***')
        else:
            fuzhu_li.append((float(i) - 32) / 1.8)

    dff3['DEWP'] = fuzhu_li

    fuzhu_li = []
    for i in dff3['TEM_MAX']:
        if re.match('\*+', i):
            fuzhu_li.append('***')
        else:
            fuzhu_li.append((float(i) - 32) / 1.8)

    dff3['TEM_MAX'] = fuzhu_li

    fuzhu_li = []
    for i in dff3['TEM_MIN']:
        if re.match('\*+', i):
            fuzhu_li.append('***')
        else:
            fuzhu_li.append((float(i) - 32) / 1.8)

    dff3['TEM_MIN'] = fuzhu_li

    dff3['RHU'] = cal_rhu(dff3['TEMP'], dff3['DEWP'])
    print(dff3)
    dff3.to_csv('/home/caidong/PycharmProjects/PycharmProjects/WeatherData/File/csv/'+file[:-4] + '.csv')#write_path + file[:-4] + '.csv')

'''气象原始文件目录'''
read_path = './File/out/'

'''处理后文件输出目录'''
write_path = './File/csv/'

if __name__ == '__main__':
    parsed_li = os.listdir('/home/caidong/PycharmProjects/PycharmProjects/WeatherData/File/csv')
    file_li = os.listdir(read_path)
    for dir in file_li:
        if dir not in parsed_li:
            # try:
                cope_weather(read_path,dir)

            # except Exception as e:
            #     print(e)
            #     pass
    # os.chdir(read_path)
    # for i in range(len(file_li)):

