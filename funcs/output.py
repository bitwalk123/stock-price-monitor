import datetime
import os

from structs.web_info import WebInfoRakuten


def get_result_pkl_filename(ticker: str = '8035') -> str:
    """Get picle filename for saving realtime stock data

    :param ticker:
    :return:
    """
    info = WebInfoRakuten()
    dir = info.getPickleDir()
    if not os.path.isdir(dir):
        os.mkdir(dir)
    return os.path.join(
        dir,
        '%s_%s.pkl' % (ticker, str(datetime.datetime.now().date()))
    )


def show_dict_contents(dict_contents: dict):
    """Print contents of dictionary

    :param dict_contents:
    :return:
    """
    print(datetime.datetime.now())
    for key in dict_contents.keys():
        print(key, dict_contents[key])
