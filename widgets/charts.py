import datetime

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator
import pandas as pd

from funcs.plot import (
    clear_axes,
    refresh_draw,
    set_xaxis_limits,
)
from funcs.sci import get_smoothing
from structs.web_info import WebInfoRakuten

FONT_PATH = 'fonts/RictyDiminished-Regular.ttf'


class ChartTechnical(FigureCanvas):
    YHALFDELTA = 250
    YPAD = 10
    YMAJORTICK = 50
    YMINORTICK = 10

    def __init__(self, info: WebInfoRakuten):
        self.fig = Figure()
        super().__init__(self.fig)
        self.setFixedSize(1200, 700)

        self.info = info
        self.df = pd.DataFrame()
        self.df_order = pd.DataFrame() # 実際に取引した結果

        # font setting
        fm.fontManager.addfont(FONT_PATH)
        font_prop = fm.FontProperties(fname=FONT_PATH)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['font.size'] = 14

        self.fig.subplots_adjust(
            top=0.98,
            bottom=0.04,
            left=0.09,
            right=0.95,
        )
        self.ax = self.fig.add_subplot(111)

    def plot(self, df: pd.DataFrame):
        self.df = df

        # Clear plots
        clear_axes(self.fig)

        # ---------------------------------------------------------------------
        #  DATA PREP.
        # ---------------------------------------------------------------------
        # Morning and Afternoon session
        df1 = df[df.index <= self.info.dt_noon1]
        df2 = df[df.index >= self.info.dt_noon2]

        # Smoothing
        df1_s = get_smoothing(df1)
        df2_s = get_smoothing(df2)

        # ---------------------------------------------------------------------
        #  PLOT
        # ---------------------------------------------------------------------
        # Raw data line
        for df_half in [df1, df2]:
            if len(df_half) > 0:
                self.ax.plot(
                    df_half,
                    linewidth=0.75,
                    color='gray',
                    alpha=0.75
                )

        # _____________________________________________________________________
        # Smoothed data line
        for df_s in [df1_s, df2_s]:
            if len(df_s) > 0:
                self.ax.plot(
                    df_s,
                    linewidth=1,
                    color='black'
                )

        # _____________________________________________________________________
        # X axis limits
        set_xaxis_limits(self.ax, self.info)
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

        # _____________________________________________________________________
        # Y axis label
        self.ax.set_ylabel('Price (JPY)')

        # _____________________________________________________________________
        # Annotation of current stock price
        if len(df) > 0:
            df_tail = df.tail(1)
            x = df_tail.index[0]
            y = df_tail.iloc[0, 0]
            self.ax.scatter(
                x=x,
                y=y,
                marker='x',
                s=50,
                c='black'
            )
            price = ' %.1f' % y
            self.ax.annotate(
                price,
                xy=(x, y),
                size=14,
                color='black',
                ha='left',
                va='center'
            )

        self.ax.minorticks_on()
        if self.info.yaxis_scale_fixed:
            n = len(df)
            if n > 0:
                df_tail = df.tail(1)
                y = df_tail.iloc[0, 0]
                self.ax.set_ylim(y - self.YHALFDELTA, y + self.YHALFDELTA)
            self.ax.yaxis.set_major_locator(MultipleLocator(self.YMAJORTICK))
            self.ax.yaxis.set_minor_locator(MultipleLocator(self.YMINORTICK))
        else:
            self.ax.set_ylim(None, None)

        self.ax.grid(which='major', linestyle='-', linewidth=0.75, color='gray')
        self.ax.grid(which='minor', linestyle='dotted', linewidth=0.75, color='gray')
        self.ax.grid(True, which='both')

        # _____________________________________________________________________
        # show order result if exists
        if len(self.df_order) > 0:
            self.show_buysell()

        # _____________________________________________________________________
        # Refresh drawings
        refresh_draw(self.fig)

    def setBuySell(self, df_trade: pd.DataFrame):
        self.df_order = df_trade

    def show_buysell(self):
        for idx in self.df_order.index:
            x = self.df_order.loc[idx]['time']
            buysell = self.df_order.loc[idx]['buysell']
            price = self.df_order.loc[idx]['unitprice']

            try:
                y = float(price.replace(',', ''))
            except TypeError:
                print('Type Error!', price, type(price))
            else:
                msg = '  %s\n  %s' % (buysell, price)
                if buysell[0] == '売':
                    acolor = '#00a'
                elif buysell[0] == '買':
                    acolor = '#a00'
                else:
                    acolor = '#000'

                self.ax.scatter(x, y, 30, c=acolor)
                self.ax.annotate(
                    msg,
                    xy=(x, y),
                    size=9,
                    color=acolor,
                    ha='left',
                    va='center',
                )


class ChartNavigation(NavigationToolbar):
    def __init__(self, chart: FigureCanvas):
        super().__init__(chart)
