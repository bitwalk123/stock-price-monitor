import os

from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDockWidget,
    QFileDialog,
    QHBoxLayout,
    QPushButton,
    QStyle,
    QVBoxLayout,
    QWidget,
)

from structs.web_info import WebInfoRakuten
from widgets.buttons import TradingButton
from widgets.combos import ComboBoxTicker


class DockMonitor(QDockWidget):
    clickedStart = Signal()
    clickedStop = Signal()
    csvSelected = Signal(str)
    debugEnabled = Signal(bool)
    debugPause = Signal()
    debugPlay = Signal()
    debugPlot = Signal()
    debugStop = Signal()
    pickleSelected = Signal(str)

    def __init__(self, info: WebInfoRakuten):
        super().__init__()
        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.ui_state = dict()
        # _____________________________________________________________________
        # base container
        base = QWidget()
        self.setWidget(base)

        layout = QVBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)
        base.setLayout(layout)

        # =====================================================================

        # _____________________________________________________________________
        # for debug
        layout_debug = QHBoxLayout()
        layout.addLayout(layout_debug)

        # _____________________________________________________________________
        # for debug
        self.but_debug = but_debug = TradingButton('debug')
        but_debug.setFunc('debug')
        but_debug.setEnabled(True)
        but_debug.setCheckable(True)
        but_debug.toggled.connect(self.set_debug_mode)
        layout_debug.addWidget(but_debug, stretch=1)

        # _____________________________________________________________________
        # for pickle file selection
        self.but_debug_folder = but_debug_folder = QPushButton()
        but_debug_folder.setIcon(self.get_builtin_icon('SP_DirIcon'))
        but_debug_folder.clicked.connect(self.on_select_file)
        but_debug_folder.setDisabled(True)
        layout_debug.addWidget(but_debug_folder)

        # _____________________________________________________________________
        # for PLAY icon
        self.but_debug_play = but_debug_play = QPushButton()
        but_debug_play.setIcon(self.get_builtin_icon('SP_MediaPlay'))
        but_debug_play.clicked.connect(self.debugPlay.emit)
        but_debug_play.setDisabled(True)
        layout_debug.addWidget(but_debug_play)

        # _____________________________________________________________________
        # for PAUSE icon
        self.but_debug_pause = but_debug_pause = QPushButton()
        but_debug_pause.setIcon(self.get_builtin_icon('SP_MediaPause'))
        but_debug_pause.clicked.connect(self.debugPause.emit)
        but_debug_pause.setDisabled(True)
        layout_debug.addWidget(but_debug_pause)

        # _____________________________________________________________________
        # for STOP icon
        self.but_debug_stop = but_debug_stop = QPushButton()
        but_debug_stop.setIcon(self.get_builtin_icon('SP_MediaStop'))
        but_debug_stop.clicked.connect(self.debugStop.emit)
        but_debug_stop.setDisabled(True)
        layout_debug.addWidget(but_debug_stop)

        # _____________________________________________________________________
        # for Plot All icon
        self.but_debug_plot = but_debug_plot = QPushButton()
        but_debug_plot.setIcon(self.get_builtin_icon('SP_ArrowRight'))
        but_debug_plot.clicked.connect(self.debugPlot.emit)
        but_debug_plot.setDisabled(True)
        layout_debug.addWidget(but_debug_plot)

        # _____________________________________________________________________
        # combobox for tickers
        self.combo_ticker = combo_ticker = ComboBoxTicker(info)
        combo_ticker.setEnabled(True)
        layout.addWidget(combo_ticker, stretch=1)

        # _____________________________________________________________________
        # start monitoring
        self.but_start = but_start = TradingButton('開始')
        but_start.setFunc('start')
        but_start.setEnabled(True)
        but_start.clicked.connect(self.clickedStart.emit)
        layout.addWidget(but_start)

        # _____________________________________________________________________
        # stop monitoring
        self.but_stop = but_stop = TradingButton('終了')
        but_stop.setFunc('stop')
        but_stop.clicked.connect(self.clickedStop.emit)
        layout.addWidget(but_stop)

        # _____________________________________________________________________
        # stretch
        layout.addStretch(stretch=1)

    def get_builtin_icon(self, name) -> QIcon:
        pixmap_icon = getattr(QStyle.StandardPixmap, name)
        icon = self.style().standardIcon(pixmap_icon)
        return icon

    def getTicker(self) -> str:
        return self.combo_ticker.currentTicker()

    def on_select_file(self):
        dialog = QFileDialog()
        dialog.setNameFilters(['Pickle files (*.pkl)', 'CSV files (*.csv)'])
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
        else:
            filename = ''

        # check filename extension
        _, extension = os.path.splitext(filename)
        if extension == '.pkl':
            self.pickleSelected.emit(filename)
            return
        if extension == '.csv':
            self.csvSelected.emit(filename)
            return

    def set_debug_mode(self, state: bool):
        if state:
            self.ui_state['combo'] = self.combo_ticker.isEnabled()
            self.combo_ticker.setDisabled(True)
            self.ui_state['start'] = self.but_start.isEnabled()
            self.but_start.setDisabled(True)
            self.ui_state['stop'] = self.but_stop.isEnabled()
            self.but_start.setDisabled(True)
            #
            self.but_debug_folder.setEnabled(True)
            #
            self.debugEnabled.emit(True)
        else:
            self.combo_ticker.setEnabled(self.ui_state['combo'])
            self.but_start.setEnabled(self.ui_state['start'])
            self.but_stop.setEnabled(self.ui_state['stop'])
            #
            self.but_debug_folder.setDisabled(True)
            self.setDebugState(False)
            #
            self.debugEnabled.emit(False)

    def setDebugState(self, state: bool = True):
        self.but_debug_play.setEnabled(state)
        self.but_debug_pause.setEnabled(state)
        self.but_debug_stop.setEnabled(state)
        self.but_debug_plot.setEnabled(state)

    def setButtonStatus(self, name: str, state: bool):
        if name == 'start':
            self.but_start.setEnabled(state)
        elif name == 'stop':
            self.but_stop.setEnabled(state)

    def setTickerFixed(self, state: bool = True):
        self.combo_ticker.setDisabled(state)
