import datetime
import pandas as pd
from matplotlib import axes
from matplotlib.figure import Figure

from structs.enumtype import XAxisRange
from structs.web_info import WebInfoRakuten

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

def get_x_minor_tick_interval(info: WebInfoRakuten)->int:
    if info.getXAxisRange() == XAxisRange.DAY:
        return 10
    else:
        return 5

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
