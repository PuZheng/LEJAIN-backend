# -*- coding: UTF-8 -*-
# -*- coding: UTF-8 -*-
import string
import math
import random

provinces = [
    {
        'name': '浙江省',
        'cities': [
            {
                'name': '杭州市',
                'counties': [
                    {'name': '西湖区'},
                    {'name': '上城区'},
                    {'name': '下城区'},
                    {'name': '拱墅区'},
                    {'name': '江干区'},
                    {'name': '萧山区'},
                    {'name': '滨江区'},
                ]
            },
            {
                'name': '宁波市',
                'counties': [
                    {'name': '海曙区'},
                    {'name': '江东区'},
                    {'name': '江北区'},
                    {'name': '北仑区'},
                    {'name': '镇海区'},
                    {'name': '鄞州区'},
                ]
            }
        ]
    },
    {
        'name': '云南省',
        'cities': [
            {
                'name': '昆明市',
                'counties': [
                    {'name': '五华区'},
                    {'name': '盘龙区'},
                    {'name': '官渡区'},
                    {'name': '西山区'},
                    {'name': '东川区'},
                ]

            },
            {
                'name': '玉溪市',
                'counties': [
                    {'name': '红塔区'}
                ]
            }
        ]
    }
]


def word(chars=None, size=8):
    chars = chars or string.ascii_letters + string.digits

    if size > len(chars):
        chars *= math.ceil(size / len(chars))

    return random.sample(chars, size)


def domain():
    return 'www.' + word() + '.' + random.choice(
        ['com', 'net', 'io', 'tv', 'biz'])


def telephone():
    return word(string.digits, 4) + '-' + word(string.digits, 8)


def lorem(word_cnt=32):
    return ' '.join([word() for i in xrange(word_cnt)])


def address():
    province = random.choice(provinces)
    city = random.choice(province.cities)
    county = random.choice(city.counties)
    return province.name + city.name + county.name + word() + '路' + \
        random.randrange(1, 100) + '号'
