import argparse
import datetime
from logging import Logger
import re
import os

import requests
import urllib.request

YEARS = [2017, 2018, 2019, 2020, 2021, 2022]
MONTHS = list(range(1, 13))
INTERVALS = [
    '1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d',
    '3d', '1w', '1M'
]
START_DATE = datetime.date(YEARS[0], MONTHS[0], 1)
END_DATE = datetime.datetime.date(datetime.datetime.now())
BASE_URL = 'https://data.binance.vision/'
TRADING_TYPE = ['spot', 'um', 'cm']


def get_store_directory(path, folder=None):
    if folder:
        store_directory = folder
    else:
        store_directory = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(store_directory, path)


def convert_to_date_object(date):
    return datetime.date(int(date.split('-')[0]), int(date.split('-')[1]),
                         int(date.split('-')[2]))


def match_date_regex(date):
    if re.match(r'\d{4}-\d{2}-\d{2}', date):
        return date
    else:
        raise argparse.ArgumentTypeError("Date must be in YYYY-MM-DD format")


def get_path(trading_type, market_data_type, time_period, symbol, interval=None):
    """
    generate data path
    """
    trading_type_path = 'data/spot'
    if trading_type != 'spot':
        trading_type_path = 'data/{}'.format(trading_type)
    if interval is not None:
        path = f'{trading_type_path}/{time_period}/{market_data_type}/{symbol.upper()}/{interval}/'
    else:
        path = f'{trading_type_path}/{time_period}/{market_data_type}/{symbol.upper()}/'
    return path

def download_file(base_path, file_name, logger, date_range=None, folder=None):
    download_path = "{}{}".format(base_path, file_name)

    if folder:
        base_path = os.path.join(folder, base_path)
    if date_range:
        date_range = date_range.replace(" ", ",")
        base_path = os.path.join(base_path, date_range)
    # generate local save path
    save_path = get_store_directory(os.path.join(base_path, file_name), folder)
    
    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))
    else:
        print("File already exists")
        #TODO:
        pass

    try:
        print("Downloading {}...".format(file_name))
        # generate download url
        download_url = "{}{}".format(BASE_URL, download_path)
        file = urllib.request.urlopen(download_url)
        length = file.getheader('Content-Length')
        if length:
            length = int(length)
            num_bars = max(4096, length // 100)
            print("File size: {:.2f} MB".format(length/1024/1024))
            with open(save_path, 'wb') as f:
                progress = 0
                print("\nFile Download: {}".format(save_path))
                logger.info("File Download: {}".format(save_path))
                while True:
                    chunk = file.read(num_bars)
                    if not chunk:
                        break
                    f.write(chunk)
                    progress += len(chunk)
                    print("\r{}%".format(int(progress / length * 100)), end='')
    except urllib.error.HTTPError as e:
        print("Error downloading file: {}".format(e))
        logger.error("Error downloading file: {}".format(e))
        return


def get_parser():
    parser = argparse.ArgumentParser(
        description='Download historical klines from Binance')
    parser.add_argument('-t',
                        dest='trading_type',
                        default='spot',
                        required=True,
                        choices=TRADING_TYPE,
                        help='Trading type')
    parser.add_argument('-s',
                        dest='symbols',
                        nargs='+',
                        required=True,
                        default='1INCHBTC',
                        help='Symbols to download split by space')
    parser.add_argument('-y',
                        dest='years',
                        default=YEARS,
                        nargs='+',
                        choices=YEARS,
                        help='Years to download split by space')
    parser.add_argument('-m',
                        dest='months',
                        default=MONTHS,
                        nargs='+',
                        choices=MONTHS,
                        help='Months to download split by space')
    parser.add_argument('-d',
                        dest='dates',
                        nargs='+',
                        type=match_date_regex,
                        help='Date range to download split by space')
    parser.add_argument('-startDate',
                        dest='start_date',
                        type=match_date_regex,
                        help='Start date to download')
    parser.add_argument('-endDate',
                        dest='end_date',
                        type=match_date_regex,
                        help='End date to download')
    parser.add_argument('-f',
                        dest='folder',
                        help='Folder to store downloaded data')
    parser.add_argument('-i',
                        dest='intervals',
                        default=INTERVALS,
                        help='Downlload Klines based on intervals')
    parser.add_argument('-c',
                        dest='checksum',
                        action='store_true',
                        help='Verify checksum of downloaded data')
    parser.add_argument('-skip-monthly',
                        dest='skip_monthly',
                        action='store_true')
    parser.add_argument('-skip-daily', dest='skip_daily', action='store_true')

    return parser