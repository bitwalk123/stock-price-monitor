import datetime

import numpy as np
import pandas as pd
from scipy.interpolate import make_smoothing_spline


def get_smoothing(df: pd.DataFrame, l=6) -> pd.DataFrame:
    """Get B-spline smoothing data

    :param df:
    :param l:
    :return:
    """
    if len(df) < 6:
        return pd.DataFrame()
    delta = 9 * 60 * 60  # 時差
    x = np.array([t.timestamp() - delta for t in df.index])
    y = df['Price'].values
    spl = make_smoothing_spline(x, y, lam=10 ** l)

    n = len(df)
    ts1 = x[0]
    ts2 = x[n - 1]
    xs = np.linspace(ts1, ts2, int(ts2 - ts1) + 1)
    ys = spl(xs)
    dt_index = pd.to_datetime([str(datetime.datetime.fromtimestamp(t)) for t in xs])

    return pd.DataFrame({'Price': ys}, index=dt_index)
