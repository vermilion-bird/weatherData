import os
import pandas as pd


def export_by_province():
    """
    :return:
    """
    ls = []
    for i in os.listdir('./weather/'):
        data = pd.read_csv('./weather/{}'.format(i))
        ls.append(data)
    all = pd.concat(ls)
    year = all[all['recordingtime'].apply(lambda x: str(x).startswith('2018'))]
    for name, g in year.groupby('station_province'):
        g.to_csv('./result/' + name + '_2019.csv')


def data_concat_export():
    """
    原始数据拼接
    :return:
    """
    adccode = pd.read_excel('./2019年10月中华人民共和国县以上行政区划代码.xlsx')
    station_name = pd.read_excel('./中国气象站点表.xlsx')
    BASE_DIR = './File/csv/'
    ls = []
    for i in os.listdir(BASE_DIR):
        data = pd.read_csv(BASE_DIR + '{}'.format(i))
        ls.append(data)
    all = pd.concat(ls)
    all = all.applymap(lambda x: '' if '*' in str(x) else x)
    all.to_csv('ad.csv')
    concat_data = pd.merge(left=all, right=station_name, how='left', right_on='区站号_1', left_on='USAF')
    stand_header = ['station_id', 'recordingtime', 'station_code', 'station_name', 'station_province', 'station_city',
                    'station_area', 'station_lat', 'station_lon', 'win_d_avg', 'win_s_avg', 'vsb', 'temp', 'dewp',
                    'slp', 'stp', 'tem_max', 'tem_min', 'pcp01', 'pcp06', 'pcp24', 'stp_max', 'stp_min', 'win_s_max',
                    'win_d_max', 'win_s_ins', 'win_d_ins', 'rhu', 'vap', 'rhu_min']
    concat_data.columns = map(str.lower, concat_data.columns)
    concat_adccode = pd.merge(left=concat_data, right=adccode, how='left', left_on='市', right_on='单位名称')
    concat_adccode.drop(
        ['station_province', 'station_city', 'station_county', 'station_code', '区站号', 'station_name', '观测场拔海高度（米）',
         '气压传感器拔海高度（米）', 'station_lat', 'station_lon'], axis=1, inplace=True)
    concat_adccode.rename(columns={"省份": "station_province", "市": "station_city",
                                   "区/县": "station_area", "区站号_1": 'station_id',
                                   "站名": 'station_name', "纬度": "station_lat", "经度": 'station_lon',
                                   'yr--modahrmn': 'recordingtime', '行政区划代码': 'station_code'
                                   }, inplace=True)
    print(concat_adccode.columns)
    concat_adccode = concat_adccode[stand_header]
    # concat_adccode.to_csv('./a.csv')
    concat_adccode['station_province'] = concat_adccode['station_province'].fillna('无城市归属')
    print(concat_adccode['station_province'].unique())
    for name, g in concat_adccode.groupby('station_province'):
        g.to_csv('./result/' + name + '_2019.csv', index=False)


if __name__ == '__main__':
    data_concat_export()
