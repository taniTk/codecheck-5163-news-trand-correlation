#!/usr/bin/env python

import urllib.request, urllib.parse
import json
import asyncio
import aiohttp
import datetime


end_point = "http://54.92.123.84/search?"
api_key = "869388c0968ae503614699f99e09d960f9ad3e12"
params = {
    "q": "",
    "wt": "json",
    "rows": "100",
    "ackey": api_key
}


def parse_args(argv):
    keywords = argv[0][1:-1].replace('"', '').replace(', ', ',').split(',')
    start_date = argv[1]
    end_date = argv[2]
    return {'keywords': keywords, 'start_date': start_date, 'end_date': end_date}


def generate_url(keyword, start_date, end_date):
    '''
    keywordを含む記事を日付の範囲を指定して検索するAPIを生成
    '''
    params["q"] = "Body:" + keyword + " AND ReleaseDate:[" + start_date + " TO " + end_date + "]"
    return end_point + urllib.parse.urlencode(params)


async def get_response(keyword, url):
    '''
    keywordとそれに対応するAPIのURLを叩いて結果をJSONにして返す
    '''
    response = await aiohttp.get(url)
    data = await response.text()
    json_data = json.loads(data)
    return json_data


def parse_response2weekly(res):
    docs = res['response']['result']['doc']
    for doc in docs:
        release_date = doc['ReleaseDate']


def convert_str2date(date_str):
    return datetime.date(*[int(a) for a in date_str.split('-')])


def init_week_num_dict(start_date, end_date):
    start_week_num_tpl = start_date.isocalendar()[:-1]
    end_week_num_tpl = end_date.isocalendar()[:-1]

    week_num_dict = {}
    key_year = start_week_num_tpl[0]
    key_week_num = start_week_num_tpl[1]
    while((key_year, key_week_num) != end_week_num_tpl):
        week_num_dict[(key_year, key_week_num)] = 0
        if key_week_num == 53 or \
            (key_week_num == 52 and datetime.date(key_year, 12, 31).isocalendar()[1] != 53):
            key_year += 1
            key_week_num = 1
            continue

        key_week_num += 1
    week_num_dict[end_week_num_tpl] = 0
    return week_num_dict

def main(argv):
    print(parse_args(argv))
