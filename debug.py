import pandas as pd
from PySide6.QtCore import QObject, QTimer

from structs.web_info import WebInfoRakuten
from widgets.charts import ChartTechnical


class DebugObj(QObject):
    YEAR = 2024

    def __init__(self, info: WebInfoRakuten, chart: ChartTechnical):
        super().__init__()
        self.info = info
        self.chart = chart
        self.df: pd.DataFrame | None = None
        # Timer related
        self.timer = QTimer(self)
        self.counter = 0

    def loop_play(self):
        if self.counter < len(self.df):
            self.chart.plot(self.df.iloc[0:self.counter + 1])
            self.counter += 1
        else:
            self.stop()

    def plot(self):
        self.chart.plot(self.df)

    def readCSV(self, filename: str):
        if len(self.df) == 0:
            return

        df = pd.read_csv(filename, encoding='cp932')
        col_order = '注文番号'
        col_dt = '注文日時'
        year = self.YEAR
        ser_dt = pd.to_datetime(['%d/%s' % (year, s) for s in df[col_dt]])
        col_buysell = '売買'
        col_unitprice = '約定単価[円]'
        col_amount = '約定数量[株/口]'
        df_order = pd.DataFrame({
            'time': ser_dt,
            'buysell': df[col_buysell],
            'unitprice': df[col_unitprice],
            'amount': df[col_amount],
        })
        df_order.index = df[col_order]
        df_order.index.name = ''
        df_order.sort_index(inplace=True)

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        print(df_order)

        self.chart.setBuySell(df_order)

    def readPickle(self, filename: str):
        self.df = pd.read_pickle(filename)
        dt = self.df.index[0]
        self.info.setYMD(dt)

    def pause(self):
        if self.timer.isActive():
            self.timer.stop()

    def play(self):
        self.timer.timeout.connect(self.loop_play)
        if not self.timer.isActive():
            self.timer.start(100)

    def stop(self):
        if self.timer.isActive():
            self.timer.stop()
            self.counter = 0
