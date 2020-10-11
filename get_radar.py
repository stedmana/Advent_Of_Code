from bs4 import BeautifulSoup
import requests
import pandas as pd
import os


'''
https://climate.weather.gc.ca/radar/image_e.html?time=200710060010&site=CASBV&image_type=CAPPI_RAIN_WEATHEROFFICE
200710060010 is earliest date when getting every 10 min
'''

# radar_page = 'https://climate.weather.gc.ca/radar/index_e.html?site=CASBV&year=2018&month=10&day=6&hour=00&minute=00&duration=6&image_type=CAPPI_RAIN_WEATHEROFFICE'
# radar_page = 'https://climate.weather.gc.ca/radar/image_e.html?time=201810060100&site=CASBV&image_type=CAPPI_RAIN_WEATHEROFFICE'
radar_page = 'https://climate.weather.gc.ca/radar/image_e.html?time='
pt_2 = '&site=CASBV&image_type=COMP_PRECIPET_RAIN_WEATHEROFFICE'
years = ['2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
days_in_month_max = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
minutes = ['00', '10', '20', '30', '40', '50']

for year in years[1:]:
    for month in months:
        month_index = int(month) - 1

        for day_index in range(days_in_month[month_index]):
            day = days_in_month_max[day_index]
            for hour in hours:
                for minute in minutes:
                    combo = year + month + day + hour + minute
                    file_name = './images/' + combo + '.gif'
                    full = radar_page + combo + pt_2
                    # print(combo)

                    if os.path.exists(file_name) and os.path.getsize(file_name) > 0 or (year == '2019' and (month == '01' or month == '02')):
                        print(file_name)
                    else:
                        result = requests.get(full)
                        if result.status_code == 200:
                            with open(file_name, 'wb') as f:
                                f.write(result.content)
                            if os.path.getsize(file_name) < 10:
                                print('small file: {}', file_name)
                                # os.remove(file_name)
                        else:
                            print('Error!\tStatus Code: {}\tURL: {}'.format(result.status_code, combo))


# result = requests.get(radar_page)
#
# if result.status_code == 200:
#     with open('./test.gif', 'wb') as f:
#         f.write(result.content)
# print('done')
print(range(24))
# if result.status_code == 200:
#     soup = BeautifulSoup(result.content, 'html.parser')
#     print('done')