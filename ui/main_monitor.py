import pandas as pd

from PySide6.QtCore import QThreadPool, Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QMainWindow
from selenium import webdriver
from selenium.common import WebDriverException

from process.proc_11_start import Proc11Start
from process.proc_12_monitor import Proc12Monitor
from process.proc_13_stop import Proc13Stop
from structs.web_info import WebInfoRakuten
from ui.dock_monitor import DockMonitor
from ui.status_monitor import StatusBarMonitor
from ui.toolbar_monitor import ToolBarMonitor
from widgets.charts import ChartNavigation, ChartTechnical


class MainMonitor(QMainWindow):
    __appname__ = 'Stock Price Monitor'
    __version__ = '0.1.0'

    def __init__(self):
        super().__init__()
        self.debug = False  # debug flag
        self.df = pd.DataFrame()
        # _____________________________________________________________________
        # thread pool
        self.threadpool = QThreadPool(self)

        # _____________________________________________________________________
        # information related to Rakuten securities
        self.info = WebInfoRakuten()

        # _____________________________________________________________________
        # title
        self.setWindowTitle('%s - %s' % (self.__appname__, self.__version__,))

        # _____________________________________________________________________
        # Top toolbar
        self.toolbar = toolbar = ToolBarMonitor(self.info)
        self.addToolBar(
            Qt.ToolBarArea.TopToolBarArea,
            toolbar,
        )
        # _____________________________________________________________________
        # Main
        self.chart = chart = ChartTechnical(self.info)
        self.setCentralWidget(chart)

        # _____________________________________________________________________
        # monitor dock
        self.dock = dock = DockMonitor(self.info)
        dock.clickedStart.connect(self.on_start)
        dock.clickedStop.connect(self.on_stop)
        dock.csvSelected.connect(self.on_debug_csv)
        dock.debugEnabled.connect(self.on_debug)
        dock.debugPlay.connect(self.on_debug_play)
        dock.debugSimulation.connect(self.on_debug_simulation)
        dock.pickleSelected.connect(self.on_debug_pickle)
        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            dock
        )

        # _____________________________________________________________________
        # Bottom toolbar
        self.navtoolbar = navtoolbar = ChartNavigation(chart)
        self.addToolBar(
            Qt.ToolBarArea.BottomToolBarArea,
            navtoolbar,
        )

        # _____________________________________________________________________
        # Statusbar
        self.statusbar = statusbar = StatusBarMonitor()
        self.setStatusBar(statusbar)

        # _____________________________________________________________________
        # browser initialization
        self.driver = webdriver.Firefox()
        # web handling
        self.p_start: Proc11Start | None = None
        self.p_mon: Proc12Monitor | None = None
        self.p_stop: Proc13Stop | None = None

    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    #  Application closure
    def closeEvent(self, event: QCloseEvent):
        print('アプリケーションを終了します。')
        try:
            self.driver.close()
        except WebDriverException as e:
            print(e)
        event.accept()  # let the window close

    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    #  DEBUG related
    def on_debug(self, state: bool):
        self.debug = state

    def on_debug_csv(self, filename: str):
        if not self.debug:
            return
        if filename == '':
            return
        if len(self.df) == 0:
            return

        df = pd.read_csv(filename, encoding='cp932')
        col_order = '注文番号'
        col_dt = '注文日時'
        dt = self.df.index[0]
        year = dt.year
        ser_dt = pd.to_datetime(['%d/%s' % (year, s) for s in df[col_dt]])
        col_buysell = '売買'
        col_unitprice = '約定単価[円]'
        col_amount = '約定数量[株/口]'
        df_trade = pd.DataFrame({
            'time': ser_dt,
            'buysell': df[col_buysell],
            'unitprice': df[col_unitprice],
            'amount': df[col_amount],
        })
        df_trade.index = df[col_order]
        df_trade.index.name = ''
        df_trade.sort_index(inplace=True)

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        print(df_trade)
        self.chart.setBuySell(df_trade)

    def on_debug_pickle(self, filename: str):
        if not self.debug:
            return
        if filename == '':
            return

        self.df = pd.read_pickle(filename)
        dt = self.df.index[0]
        self.info.setYMD(dt)
        self.dock.setDebugState()

    def on_debug_play(self):
        self.chart.plot(self.df)

    def on_debug_simulation(self):
        pass

    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    #  START PROCESS
    def on_start(self):
        # _____________________________________________________________________
        # change button status
        self.dock.setTickerFixed()
        self.dock.setButtonStatus('start', False)
        self.dock.setButtonStatus('stop', True)
        # _____________________________________________________________________
        # starting START process
        print('ログイン・プロセスを開始します。')
        self.info.setTargetTicker(self.dock.getTicker())
        self.p_start = Proc11Start(self, self.driver, self.info, self.threadpool)
        self.p_start.processFinished.connect(self.on_monitor)
        self.p_start.run()

    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    #  MONITOR PROCESS
    def on_monitor(self):
        self.p_start.deleteLater()
        print('ログイン・プロセスを終了しました。次に監視プロセスへ進みます。')
        # _____________________________________________________________________
        # starting MONITOR process
        self.p_mon = Proc12Monitor(self, self.driver, self.info, self.threadpool)
        self.p_mon.dataUpdated.connect(self.price_updated)
        self.p_mon.processFinished.connect(self.on_monitor_stopped)
        self.p_mon.run()

    def on_monitor_stop(self):
        print('タイマーを止めます。')
        self.p_mon.stop()

    def on_monitor_stopped(self):
        self.p_mon.deleteLater()
        print('監視プロセスを終了しました。')

    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    #  STOP PROCESS
    def on_stop(self):
        print('ログアウト・プロセスを開始します。')
        # _____________________________________________________________________
        # stop monitoring
        self.on_monitor_stop()
        QTest.qWait(1000)

        # _____________________________________________________________________
        # starting STOP process
        self.p_stop = Proc13Stop(self, self.driver, self.info, self.threadpool)
        self.p_stop.processFinished.connect(self.on_stop_completed)
        self.p_stop.run()
        # _____________________________________________________________________
        # change button status
        self.dock.setButtonStatus('start', True)
        self.dock.setButtonStatus('stop', False)
        self.dock.setTickerFixed(False)

    def on_stop_completed(self):
        self.p_stop.deleteLater()
        print('ログアウト・プロセスを終了しました。')

    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    #  PRICE updated
    def price_updated(self, df: pd.DataFrame, price_value, price_time):
        print(price_value, 'at', price_time)
        # self.toolbar.showPrice(str(price_value))
        self.df = df

        # update chart
        self.chart.plot(df)
