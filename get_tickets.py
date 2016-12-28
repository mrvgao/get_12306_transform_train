# !/usr/bin/python3 

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import sys

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


result = 'result.txt'
result = open(result, 'w+')

    
def make_address_dic():
    address_file = 'address.txt'
    address_dic = {}
    for line in open(address_file).readlines():
        line = line.split(':')
        assert len(line) == 2
        code = line[1].strip()
        address = line[0].strip()
        address_dic[code] = address

    return address_dic


def combine_url(begin, end, time):
    url = "https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate=2017-01-{0}&from_station={1}&to_station={2}".format(time, begin, end)
    return url


def print_train_no(r):
    for t in r:
        print(t['station_train_code'])


def test_two_city_have_seats(city1, city2, time):
    url = combine_url(begin=city1, end=city2, time=time)
    r = requests.get(url, verify=False)

    try:
        r.raise_for_status()
    except Exception as e:
        print('网络错误')
        print(e)
    
    JSON = r.json()['data']
    if 'datas' in JSON:
        seats = filter(lambda r: have_seats(r), JSON['datas'])
        if len(list(seats)) == 0:
            #print('no')
            return False
        else:
            return seats
        return seats
    return False
    

def have_seats(data):
    seats = ('yw_num', 'ze_num', 'zy_num')
    have = False
    for s in seats:
        if str(data[s]).isdigit():
            have = True
            break
    return have


def test_two_city_could_arrive(START, TO, time):
    start_code = from_city_get_code(START)
    to_code = from_city_get_code(TO)
    directed = test_two_city_have_seats(start_code, to_code, time)
    if not directed or len(list(directed)) == 0:
        find_transform(start_code, to_code, time)
    else:
        print("%s ====> %s" % (START, TO))


def find_transform(START, TO, time):
    address_list = make_address_dic()
    for city in address_list:
        if test_two_city_have_seats(START, city, time):
            if test_two_city_have_seats(city, TO, time) or test_two_city_have_seats(city, TO, time+1):
                line = "\n%s: %s ===> %s ==> %s" % (str(time), address_list[START], address_list[city], address_list[TO])
                print(line)
                result.write(line)
            
    
def from_city_get_code(city):
    address_dict = make_address_dic()
    for code in address_dict:
        if address_dict[code] == city:
            return code
    else:
        return None


start = input('input start location(eg. 杭州): ____ \b\b\b\b')
end = input('input destination (eg. 成都): ____ \b\b\b\b')

lastest = input('请输出最晚乘车时间： 一月__日\b\b\b')

print('From {0} ==> {1}, the lastest data is January {2}'.format(start, end, lastest))

for t in range(20, 25):
    test_two_city_could_arrive(start, end, t)
