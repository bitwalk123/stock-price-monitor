import numpy as np
import pandas as pd

from funcs.sci import resample_1m_ohlc, get_smoothing
from structs.enumtype import TypeDeal
from structs.web_info import WebInfoRakuten
from tech.psar import parabolic_sar


def sim_get_ohlc(df: pd.DataFrame, info: WebInfoRakuten) -> tuple[pd.DataFrame, pd.DataFrame]:
    if len(df) == 0:
        return pd.DataFrame(), pd.DataFrame()

    df1 = df[df.index <= info.dt_noon1]
    if len(df1) > 0:
        df1_ohlc = resample_1m_ohlc(df1)
        df1s = get_smoothing(df1)
        df1s_ohlc = resample_1m_ohlc(df1s)
        parabolic_sar(df1s_ohlc)
        df1_ohlc['Trend'] = df1s_ohlc['Trend']
    else:
        df1_ohlc = pd.DataFrame()

    df2 = df[df.index >= info.dt_noon2]
    if len(df2) > 0:
        df2_ohlc = resample_1m_ohlc(df2)
        df2s = get_smoothing(df2)
        df2s_ohlc = resample_1m_ohlc(df2s)
        parabolic_sar(df2s_ohlc)
        df2_ohlc['Trend'] = df2s_ohlc['Trend']
    else:
        df2_ohlc = pd.DataFrame()

    return df1_ohlc, df2_ohlc


# -------------------
# 取引シュミレーション
# -------------------

def sim_get_action(trend: float) -> str:
    if trend == 0:
        return '売'
    else:
        return '買'


def sim_update_position(status, price, unit) -> float:
    if status == 0:
        return price * unit
    else:
        return -price * unit


def print_transaction(type_trans, n, ser, price, trend, position=0):
    print('{:0=2}.'.format(n), ser.name, price, sim_get_action(trend), end=' ')
    if type_trans == TypeDeal.BUYSELL:
        print('')
    elif type_trans == TypeDeal.TRANSACTION:
        print(position)
    elif type_trans == TypeDeal.FORCE:
        print(position, '（強制決済）')


def sim_transaction(df: pd.DataFrame, verbose=True) -> float:
    """Transaction simulator based on PSAR trend signal

    :param df:
    :param verbose:
    :return:
    """
    n = len(df)
    started = False
    status = None
    trend = np.nan
    position = 0  # 建玉
    earning = 0  # 収益
    unit = 100  # 売買単位
    num_deal = 0

    for r in range(n - 1):
        series = df.iloc[r]
        trend = series['Trend']

        if np.isnan(trend):
            # NaN
            continue
        if not started:
            # 売買
            started = True
            price = series['Close']
            status = trend
            position += sim_update_position(status, price, unit)
            if num_deal > 0:
                if verbose:
                    print_transaction(TypeDeal.BUYSELL, num_deal, series, price, status)
        elif status != trend:
            # 決済
            started = False
            price = series['Close']
            status = trend
            position += sim_update_position(status, price, unit)
            if num_deal > 0:
                earning += position
                if verbose:
                    print_transaction(TypeDeal.TRANSACTION, num_deal, series, price, status, position)
            position = 0
            num_deal += 1

    if started:
        # 強制決済
        series = df.iloc[n - 1]
        started = False
        price = series['Close']
        if trend == 0.:
            status = 1.
        else:
            status = 0.
        position += sim_update_position(status, price, unit)
        earning += position
        if verbose:
            print_transaction(TypeDeal.FORCE, num_deal, series, price, status, position)
        position = 0

    return earning
