from collections import deque

import pandas as pd


class PSAR:
    # Reference:
    # https://raposa.trade/blog/the-complete-guide-to-calculating-the-parabolic-sar-in-python/
    def __init__(self, af_init=0.02, af_max=0.2, af_step=0.02):
        self.af_max = af_max
        self.af_init = af_init
        self.af = af_init
        self.af_step = af_step
        self.point_extreme = None
        self.trend_high = list()
        self.trend_low = list()
        self.window_high = deque(maxlen=2)
        self.window_low = deque(maxlen=2)

        # Lists to track results
        self.list_psar = list()
        self.list_af = list()
        self.list_ep = list()
        self.list_high = list()
        self.list_low = list()
        self.list_trend = list()
        self._num_days = 0

    def calcPSAR(self, high, low):
        if self._num_days >= 3:
            psar = self._calcPSAR()
        else:
            psar = self._initPSARVals(high, low)

        psar = self._updateCurrentVals(psar, high, low)
        self._num_days += 1

        return psar

    def _initPSARVals(self, high, low):
        if len(self.window_low) <= 1:
            self.trend = None
            self.point_extreme = high
            return None

        if self.window_high[0] < self.window_high[1]:
            self.trend = 1
            psar = min(self.window_low)
            self.point_extreme = max(self.window_high)
        else:
            self.trend = 0
            psar = max(self.window_high)
            self.point_extreme = min(self.window_low)

        return psar

    def _calcPSAR(self):
        psar_prev = self.list_psar[-1]

        if self.trend == 1:  # Up
            psar = psar_prev + self.af * (self.point_extreme - psar_prev)
            psar = min(psar, min(self.window_low))
        else:
            psar = psar_prev - self.af * (psar_prev - self.point_extreme)
            psar = max(psar, max(self.window_high))

        return psar

    def _updateCurrentVals(self, psar, high, low):
        if self.trend == 1:
            self.trend_high.append(high)
        elif self.trend == 0:
            self.trend_low.append(low)

        psar = self._trendReversal(psar, high, low)

        self.list_psar.append(psar)
        self.list_af.append(self.af)
        self.list_ep.append(self.point_extreme)
        self.list_high.append(high)
        self.list_low.append(low)
        self.window_high.append(high)
        self.window_low.append(low)
        self.list_trend.append(self.trend)

        return psar

    def _trendReversal(self, psar, high, low):
        # Checks for reversals
        reversal = False
        if self.trend == 1 and psar > low:
            self.trend = 0
            psar = max(self.trend_high)
            self.point_extreme = low
            reversal = True
        elif self.trend == 0 and psar < high:
            self.trend = 1
            psar = min(self.trend_low)
            self.point_extreme = high
            reversal = True

        if reversal:
            self.af = self.af_init
            self.trend_high.clear()
            self.trend_low.clear()
        else:
            if high > self.point_extreme and self.trend == 1:
                self.af = min(self.af + self.af_step, self.af_max)
                self.point_extreme = high
            elif low < self.point_extreme and self.trend == 0:
                self.af = min(self.af + self.af_step, self.af_max)
                self.point_extreme = low

        return psar


def parabolic_sar(df:pd.DataFrame):
    indic = PSAR()
    df['PSAR'] = df.apply(lambda x: indic.calcPSAR(x['High'], x['Low']), axis=1)
    df['EP'] = indic.list_ep
    df['Trend'] = indic.list_trend
    df['AF'] = indic.list_af
