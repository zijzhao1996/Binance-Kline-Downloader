import os
import sys
import urllib.request as ur
import json
from logger import get_logger
from utils import START_DATE, END_DATE, convert_to_date_object, download_file, get_parser, get_path


def download_monthly_klines(trading_type, symbols, intervals,
                            years, months, start_date, end_date, folder,
                            checksum, logger):
    """
    main function to download klines data. 
    Params: 
        months: 
        folder: which folder to store the data, default is current folder (None)
    """

    date_range = None

    if start_date and end_date:
        date_range = start_date + " " + end_date

    if not start_date:
        start_date = START_DATE
    else:
        start_date = convert_to_date_object(start_date)
    
    if not end_date:
        end_date = END_DATE
    else:
        end_date = convert_to_date_object(end_date)

    print("Found {} symbols".format(len(symbols)))

    current = 0
    for symbol in symbols:
        print("[{}/{}] Downloading monthly {} klines...".format(current+1, len(symbols), symbol))
        for interval in intervals:
            for year in years:
                for month in months:
                    current_date = convert_to_date_object('{}-{}-01'.format(year, month))
                    if current_date >= start_date and current_date <= end_date:
                        path = get_path(trading_type, 'klines', 'monthly', symbol, interval)
                        file_name = "{}-{}-{}-{}.zip".format(symbol.upper(), interval, year, '{:02d}'.format(month))
                        download_file(path, file_name, logger, date_range, folder)

                    if checksum:
                        checksum_name = "{}-{}-{}-{}.zip.CHECKSUM".format(symbol.upper(), interval, year, '{:02d}'.format(month))
                        download_file(path, checksum_name, logger, date_range, folder)


def download():
    parser = get_parser()
    args = parser.parse_args(sys.argv[1:])

    


if __name__ == "__main__":
    print('=====================')
    download()
    #TODO: modify log file name
    logger = get_logger('info', os.path.join('./logs', 'log.txt'))
    download_monthly_klines('spot', ['1INCHBTC'], ['1m'], [2022], [1], '2017-12-21', '2022-07-01', None, True, logger)