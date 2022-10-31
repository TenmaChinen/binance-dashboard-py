from collections import defaultdict, OrderedDict
from requests import get
import json

class Status:
    TRADING = 'TRADING'
    BREAK = 'BREAK'
    ALL = 'ALL'

def get_assets():
    l_all_assets, l_av_assets = [], []
    for d_symbol_info in d_exchange_info:
        l_base_quote = [d_symbol_info[k] for k in ['baseAsset', 'quoteAsset']]
        l_all_assets += l_base_quote

        if d_symbol_info['status'] == Status.TRADING:
            l_av_assets += l_base_quote

    l_av_assets = sorted(list(set(l_av_assets)))
    return l_av_assets


def get_assets_pairs():
    d_assets_pairs = defaultdict(dict)

    for d_info in d_exchange_info:
        if d_info['status'] == Status.TRADING:
            base, quote = d_info['baseAsset'], d_info['quoteAsset']
            d_common = dict(symbol=d_info['symbol'], name=f'{base}-{quote}')
            d_assets_pairs[base][quote] = dict(**d_common, op='M')
            d_assets_pairs[quote][base] = dict(**d_common, op='D')
    for key, d_obj in d_assets_pairs.items():
        d_assets_pairs[key] = dict(sorted(d_assets_pairs[key].items()))
    return d_assets_pairs


def get_last_closes(pair, interval):
    uri = 'https://api.binance.com/api/v1/klines?symbol=%s&interval=%s&limit=1000'
    l_klines = get(uri % (pair, interval)).json()
    l_ts, l_closes = zip(*[[x[6], float(x[4])] for x in l_klines])
    return l_ts, l_closes


def get_pair(asset_1, asset_2):
    try:
        d_pair = d_assets_pairs[asset_1][asset_2]
        return d_pair['symbol'], d_pair['name']
    except:
        return None

def get_to_assets(asset_from):
    d_assets_to = d_assets_pairs.get(asset_from,None)
    if d_assets_to:
        return list(d_assets_to.keys())
    return None


def load_json(file_name):
  file = open(file_name,'r')
  json_object = json.load(file)
  file.close()
  return json_object


def save_json(file_name, json_object):
  file = open(file_name,'w')
  json.dump(json_object,file)
  file.close()

def load_local_assets():
  return load_json('local/assets.json')

def load_local_assets_pairs():
  return load_json('local/assets_pairs.json')


d_exchange_info = get('https://api.binance.com/api/v1/exchangeInfo').json()['symbols']
l_assets = load_local_assets()
d_assets_pairs = load_local_assets_pairs()


if __name__ == '__main__':
  
  save_json('local/assets.json', get_assets())
  save_json('local/assets_pairs.json', get_assets_pairs())

  # print(load_local_assets())
  d_assets_pairs = load_local_assets_pairs()
  # print(d_assets_pairs['BNB']['BUSD'])
