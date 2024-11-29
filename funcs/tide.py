import datetime
import re

import pandas as pd


def get_ymd(dt: datetime) -> str:
    """Generate string YYYY-=MM-DD from datatime

    :param dt:
    :return:
    """
    # TODO:
    # need to try using date() method
    yr = dt.year
    mo = dt.month
    dy = dt.day
    ymd = '%04d-%02d-%02d' % (yr, mo, dy)
    return ymd
