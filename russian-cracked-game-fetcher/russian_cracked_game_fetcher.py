# url sample: https://byrut.org/index.php?do=download&id=56751
import time
import requests
import re
from os.path import exists
import os


def download_file_by_id(directory, gameid):
    url = f'https://byrut.org/index.php?do=download&id={gameid}'
    if not exists(directory):
        os.mkdir(directory)

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'officecdn-microsoft-com.akamaized.net',
        'Pragma': 'no-cache',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }

    r = requests.get(url, headers)
    if r.status_code == 200:
        # get file name:game's english name
        content_disposition = r.headers.get('content-disposition')
        filename = re.search(r'"([\s\S]*)"', content_disposition).group(1)
        # add id before file name to fast find information on https://byrut.org/index.php?do=download&id={}
        # use $id$ as the prefix of filename
        filename = f'${gameid}$-' + filename
        game_full_path = os.path.join(directory, filename)

        with open(game_full_path, mode='wb') as torrent:
            torrent.write(r.content)
        print(f'{filename} downloaded')
    else:
        print(f'request failed,code:{r.status_code}')


directory = os.path.join(os.getcwd(), 'download')
# check if file exists
allfiles = os.listdir(directory)
for i in range(1, 10000):
    for f in allfiles:
        if f.startswith(f'${i}$-'):
            print(f'game id {i} exists')
            continue
        else:
            break

    download_file_by_id(directory, i)
