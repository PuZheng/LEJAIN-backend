# -*- coding: UTF-8 -*-
# -*- coding: UTF-8 -*-
import string
import math
import random
import tempfile
import os

from PIL import ImageFont, Image, ImageDraw
from datetime import datetime, timedelta

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

    return ''.join(random.sample(chars, size))


def domain():
    return 'www.' + word() + '.' + random.choice(
        ['com', 'net', 'io', 'tv', 'biz'])


def telephone():
    return word(string.digits, 4) + '-' + word(string.digits, 8)


def lorem(word_cnt=32):
    return ' '.join([word() for i in range(word_cnt)])


def address():
    province = random.choice(provinces)
    city = random.choice(province['cities'])
    county = random.choice(city['counties'])
    return province['name'] + city['name'] + county['name'] + word() + '路' + \
        str(random.randrange(1, 100)) + '号'


def color():
    return random.randrange(0, 0xffff)


def image(size, text=None, dir_=None, filename=None, bg=None, fg=None):

    size = size or (256, 256)
    text = text or 'x'.join(map(str, size))
    bg = color() if bg is None else bg
    fg = color() if fg is None else fg

    if (size[0] / size[1] > len(text)):  # text should be laid in landscape mode
        font_size = math.floor(size[1] * 0.95)
    else:
        font_size = math.floor(size[0] / len(text) * 0.95)

    font = ImageFont.truetype('FreeMono.ttf', font_size)

    im = Image.new('RGB', size, color=bg)
    draw = ImageDraw.Draw(im)
    text_size = font.getsize(text)
    draw.text(
        ((size[0] - text_size[0]) / 2, (size[1] - text_size[1]) / 2),
        text=text, font=font, fill=fg)

    dir_ = dir_ or './'
    filename = os.path.join(dir_, filename) if filename else \
        tempfile.mktemp(dir=dir_, suffix='.jpg', prefix='')

    im.save(filename)

    return filename


def time(range_=None):
    range_ = range_ or [-7 * 24 * 3600, 7 * 24 * 3600 + 1]

    return datetime.now() + timedelta(seconds=random.randrange(*range_))


BOUNDS = [
    # a block of area in HangZhou
    {
        'weight': 1,
        'ne': {
            'lng': 120.279919,
            'lat': 30.300651
        },
        'sw': {
            'lng': 120.079762,
            'lat': 30.196848,
        }
    },
    # a block of area in BeiJing
    {
        'weight': 1,
        'ne': {
            'lng': 116.496674,
            'lat': 39.955216,
        },
        'sw': {
            'lng': 116.296517,
            'lat': 39.863043,
        }
    },
    # a huge area
    {
        'weight': 98,
        'ne': {
            'lng': 116.015625,
            'lat': 39.774769
        },
        'sw': {
            'lng': 100.019531,
            'lat': 23.563987
        }
    }
]


def lng_lat():
    tmp = random.randrange(0, sum(b['weight'] for b in BOUNDS))
    acc = 0
    for bound in BOUNDS:
        if tmp < bound['weight'] + acc:
            break
        acc += bound['weight']
    lng1, lng2 = bound['sw']['lng'], bound['ne']['lng']
    lat1, lat2 = bound['sw']['lat'], bound['ne']['lat']
    return {
        'lng': lng1 + random.random() * (lng2 - lng1),
        'lat': lat1 + random.random() * (lat2 - lat1),
    }
