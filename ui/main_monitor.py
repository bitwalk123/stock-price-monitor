import pandas as pd

from PySide6.QtCore import QThreadPool, Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QMainWindow
from selenium import webdriver
from selenium.common import WebDriverException

from debug import DebugObj
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
        self.debug: DebugObj | None = None  # debug object
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
        dock.debugReplay.connect(self.on_debug_replay)
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
        # Browser initialization
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
    #  DebugObj
    def on_debug(self, state: bool):
        if state:
            self.debug = DebugObj(self.info, self.chart)
        else:
            self.debug = None

    def on_debug_csv(self, filename: str):
        if self.debug is None:
            return
        if filename == '':
            return
        self.debug.readCSV(filename)

    def on_debug_pickle(self, filename: str):
        if self.debug is None:
            return
        if filename == '':
            return
        self.debug.readPickle(filename)
        self.dock.setDebugState()

    def on_debug_play(self):
        if self.debug is None:
            return
        self.debug.play()

    def on_debug_replay(self):
        if self.debug is None:
            return
        self.debug.replay()

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
