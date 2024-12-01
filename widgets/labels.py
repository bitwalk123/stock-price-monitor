from PySide6.QtWidgets import QLCDNumber, QLabel, QSizePolicy


def set_label_status(label: QLabel, status: bool = True):
    label.setEnabled(status)


class StockPrice(QLCDNumber):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(250)
        self.setStyleSheet("""
            QLCDNumber {
                background-color: darkgreen;
                color: lightyellow;
            }
        """)
        # self.setSizePolicy(
        #    QSizePolicy.Policy.MinimumExpanding,
        #    QSizePolicy.Policy.Preferred
        # )
        self.setDigitCount(8)
        self.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)


class TradingLabel(QLabel):
    def __init__(self, title: str):
        super().__init__(title)
        self.func = None
        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding
        )
        self.setEnabled(False)

    def setFunc(self, func: str):
        self.func = func
        if func == 'update':
            self.setStyleSheet(self.cssLabelUpdate())
            self.setAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )

    def getFunc(self, func: str) -> str:
        return self.func

    @staticmethod
    def cssLabelUpdate() -> str:
        return """
            TradingLabel {
                font-family: monospace;
                font-size: 8pt;
                margin: 0 0.25em;
            }
            TradingLabel:disabled {
                color: gray;
                background-color: lightgray;
            }
        """


class LabelToolBar(QLabel):
    def __init__(self, title: str):
        super().__init__(title)
        self.setStyleSheet("""
            LabelToolBar {
                font-family: monospace;
                padding: 0 0.25em 0 1em;
            }
        """)
