from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QAbstractButton,
    QButtonGroup,
    QSpinBox,
)

from structs.enumtype import XAxisRange
from structs.web_info import WebInfoRakuten
from widgets.buttons import (
    TradingCheckButton,
    TradingRadioButton,
)
from widgets.container import (
    Container,
    Frame,
    HPad,
)
from widgets.labels import (
    LabelToolBar,
    StockPrice,
)
from widgets.layout import (
    HBoxLayout,
    VBoxLayout,
)
from widgets.toolbar import ToolBar


class ToolBarMonitor(ToolBar):
    clickedChartXAxisRange = Signal()

    def __init__(self, info: WebInfoRakuten):
        super().__init__()
        self.info = info
        # _____________________________________________________________________
        lab_range = LabelToolBar('表示範囲')
        self.addWidget(lab_range)

        # １日
        rb_day = TradingRadioButton('１日')
        rb_day.setXAxisRange(XAxisRange.DAY)
        rb_day.setEnabled(True)
        rb_day.setChecked(True)
        self.addWidget(rb_day)

        # 前場
        rb_am = TradingRadioButton('前場')
        rb_am.setXAxisRange(XAxisRange.AM)
        rb_am.setEnabled(True)
        self.addWidget(rb_am)

        # 後場
        rb_pm = TradingRadioButton('後場')
        rb_pm.setXAxisRange(XAxisRange.PM)
        rb_pm.setEnabled(True)
        self.addWidget(rb_pm)

        # group handling for radio buttons
        self.rb_rng_group = rb_rng_group = QButtonGroup()
        rb_rng_group.addButton(rb_day)
        rb_rng_group.addButton(rb_am)
        rb_rng_group.addButton(rb_pm)
        rb_rng_group.buttonClicked.connect(self.on_xaxis_range_changed)

        # y軸スケール
        self.chk_yaxis_scale = chk_yaxis_scale = TradingCheckButton('y軸スケール固定')
        chk_yaxis_scale.toggled.connect(self.on_yaxis_scale_changed)
        self.addWidget(chk_yaxis_scale)

    def on_xaxis_range_changed(self):
        but: QAbstractButton | TradingRadioButton = self.rb_rng_group.checkedButton()
        self.info.setXAxisRange(but.getXAxisRange())

    def on_yaxis_scale_changed(self, state: bool):
        self.info.yaxis_scale_fixed = state
