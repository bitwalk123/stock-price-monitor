import datetime

import numpy as np
import pandas as pd
from scipy.interpolate import (
    make_interp_spline,
    make_smoothing_spline,
)

TZDELTA = 9 * 60 * 60  # 時差


def get_smoothing(df: pd.DataFrame) -> pd.DataFrame:
    """Get B-spline smoothing data

    :param df:
    :param l:
    :return:
    """
    if len(df) < 6:
        return pd.DataFrame()

    x = np.array([t.timestamp() - TZDELTA for t in df.index])
    y = df['Price'].values
    spl = make_smoothing_spline(x, y, lam=10 ** 5)

    n = len(df)
    ts1 = x[0]
    ts2 = x[n - 1]
    xs = np.linspace(ts1, ts2, int(ts2 - ts1) + 1)
    ys = spl(xs)
    dt_index = pd.to_datetime([str(datetime.datetime.fromtimestamp(t)) for t in xs])

    return pd.DataFrame({'Price': ys}, index=dt_index)


def get_resample_1sec(df: pd.DataFrame) -> pd.DataFrame:
    """Get B-spline smoothing data

    :param df:
    :param l:
    :return:
    """
    if len(df) < 6:
        return pd.DataFrame()
    x = np.array([t.timestamp() - TZDELTA for t in df.index])
    y = df['Price'].values
    spl = make_interp_spline(x, y, k=1)

    n = len(df)
    ts1 = x[0]
    ts2 = x[n - 1]
    xs = np.linspace(ts1, ts2, int(ts2 - ts1) + 1)
    ys = spl(xs)
    dt_index = pd.to_datetime([str(datetime.datetime.fromtimestamp(t)) for t in xs])

    return pd.DataFrame({'Price': ys}, index=dt_index)

def resample_ohlc(df: pd.DataFrame, interval: str) -> pd.DataFrame:
    """Resample realtime data to 1 min OHLC data

    :param df:
    :return:
    """
    if len(df) == 0:
        return pd.DataFrame()

    df_ohlc = df['Price'].resample(interval).ohlc()
    df_ohlc.columns = ['Open', 'High', 'Low', 'Close']

    return df_ohlc
