import datetime
import pandas as pd
from matplotlib import axes
from matplotlib.figure import Figure

from structs.enumtype import XAxisRange
from structs.web_info import WebInfoRakuten
from tech.psar import parabolic_sar

DT_GAP = datetime.timedelta(minutes=2)
DT_PAD_1 = datetime.timedelta(minutes=5)
DT_PAD_2 = datetime.timedelta(minutes=10)


def clear_axes(fig: Figure):
    """Clear axes

    :param fig:
    :return:
    """
    axs = fig.axes
    for ax in axs:
        ax.cla()
        ax.grid()


def plot_parabolic_sar(list_df: list, ax: axes.Axes):
    """Plot Parabolic SAR

    :param list_df:
    :param ax:
    :return:
    """
    for df in list_df:
        if len(df) < 5:
            continue
        parabolic_sar(df)
        bull = df.loc[df['Trend'] == 1]['PSAR']
        bear = df.loc[df['Trend'] == 0]['PSAR']
        # ax.scatter(bull.index, bull, color='#00f', s=6, alpha=0.75)
        ax.scatter(bull.index, bull, s=30, facecolors='none', edgecolors='red')
        # ax.scatter(bear.index, bear, color='#f00', s=6, alpha=0.75)
        ax.scatter(bear.index, bear, s=30, facecolors='none', edgecolors='blue')


def plot_rsi_area(list_series: list, dict_ax: dict):
    """Plot RSI area

    :param list_series:
    :param dict_ax:
    :return:
    """
    for series in list_series:
        if len(series) == 0:
            continue

        x = series.index
        y = series.values
        # for i in self.ax.keys():
        for i in range(2):
            dict_ax[i].fill_between(
                x, 0, 1,
                where=y < 30,
                color='#0f0', alpha=0.1,
                transform=dict_ax[i].get_xaxis_transform()
            )
            dict_ax[i].fill_between(
                x, 0, 1,
                where=y > 70,
                color='#f00', alpha=0.1,
                transform=dict_ax[i].get_xaxis_transform()
            )


def plot_rsi_line(list_series: list, ax: axes.Axes):
    """Plot RSI line

    :param list_series:
    :param ax:
    :return:
    """
    for series in list_series:
        if len(series) > 1:
            ax.plot(series, linewidth=1, color='black')


def refresh_draw(fig: Figure):
    """Refresh drawing

    :param fig:
    :return:
    """
    fig.canvas.draw()


def remove_axes(fig: Figure):
    """Remove axes

    :param fig:
    :return:
    """
    axs = fig.axes
    for ax in axs:
        ax.remove()


def set_xaxis_limits(ax: axes.Axes, info: WebInfoRakuten):
    """Set X axis limits

    :param ax:
    :param info:
    :return:
    """
    if info.getXAxisRange() == XAxisRange.AM:
        x1 = info.dt_start - DT_PAD_1
        x2 = info.dt_noon1 + DT_PAD_1
    elif info.getXAxisRange() == XAxisRange.PM:
        x1 = info.dt_noon2 - DT_PAD_1
        x2 = info.dt_end + DT_PAD_1
    else:
        x1 = info.dt_start - DT_PAD_2
        x2 = info.dt_end + DT_PAD_2

    ax.set_xlim(x1, x2)


def show_annotation(df: pd.DataFrame, ax: axes.Axes):
    """Show annotation

    :param df:
    :param ax:
    :return:
    """
    if len(df) == 0:
        return

    df_tail = df.tail(1)
    ax.plot(df_tail, marker='x', markersize=8, c='black')

    x = df_tail.index[0] + DT_GAP
    y = df_tail.iloc[0, 0]
    price = str(y)
    ax.annotate(price, xy=(x, y), size=14, color='black')
