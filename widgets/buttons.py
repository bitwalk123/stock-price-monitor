from PySide6.QtWidgets import QPushButton, QSizePolicy, QRadioButton, QCheckBox, QAbstractButton

from structs.enumtype import XAxisRange


def set_button_status(button: QAbstractButton, status: bool = True):
    button.setEnabled(status)


class TradingButton(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.func = None
        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding
        )
        self.setStyleSheet("""
            TradingButton {
                font-family: monospace;
            }        
            TradingButton:disabled {
                color: #888;
                background-color: #ddd;
            }
        """)
        self.setEnabled(False)

    def setFunc(self, func: str):
        self.func = func

        if func == 'autologout':
            self.setStyleSheet(self.cssButtonAutoLogout())
        elif func == 'credit':
            self.setStyleSheet(self.cssButtonCredit())
        elif func == 'debug':
            self.setStyleSheet(self.cssButtonDebug())
        elif func == 'domestic':
            self.setStyleSheet(self.cssButtonDomestic())
        elif func == 'login':
            self.setStyleSheet(self.cssButtonLogin())
        elif func == 'loginsite':
            self.setStyleSheet(self.cssButtonLoginSite())
        elif func == 'logout':
            self.setStyleSheet(self.cssButtonLogout())
        elif func == 'long':
            self.setStyleSheet(self.cssButtonLong())
        elif func == 'monitor':
            self.setStyleSheet(self.cssButtonMonitor())
        elif func == 'order':
            self.setStyleSheet(self.cssButtonOrder())
        elif func == 'search':
            self.setStyleSheet(self.cssButtonSearch())
        elif func == 'short':
            self.setStyleSheet(self.cssButtonShort())
        elif func == 'start':
            self.setStyleSheet(self.cssButtonStart())
        elif func == 'status':
            self.setStyleSheet(self.cssButtonStatus())
        elif func == 'stop':
            self.setStyleSheet(self.cssButtonStop())
        elif func == 'update':
            self.setStyleSheet(self.cssButtonUpdate())

    def getFunc(self) -> str:
        return self.func

    @staticmethod
    def cssButtonAutoLogout() -> str:
        return """
            TradingButton {
                color: #002;
                background-color: #ddf;
                font-family: monospace;
                font-size: 8pt;
                padding: 0.25em 0.5em;
            }
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
            }
        """

    @staticmethod
    def cssButtonCredit() -> str:
        return """
            TradingButton {
                color: white;
                background-color: #a762df;
                font-family: monospace;
            }
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
            }
        """

    @staticmethod
    def cssButtonDebug() -> str:
        return """
            TradingButton {
                font-family: monospace;
                font-size: 9pt;
            }
            TradingButton:checked {
                color: white;
                background-color: chocolate;
            }
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
            }
        """

    @staticmethod
    def cssButtonDomestic() -> str:
        return """
            TradingButton {
                color: #212;
                background-color: #fef;
                font-family: monospace;
                padding: 0.5em;
            }
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
                font-weight: normal;
            }
        """

    @staticmethod
    def cssButtonLogin() -> str:
        return """
            TradingButton {
                color: white;
                background-color: #bf0000;
                font-family: monospace;
                padding: 0.5em;
            }
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
                font-weight: normal;
            }
        """

    @staticmethod
    def cssButtonLoginSite() -> str:
        return """
            TradingButton {
                color: #002;
                background-color: #ddf;
                font-family: monospace;
                font-size: 8pt;
                padding: 0.25em 0.5em;
            }
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
            }
        """

    @staticmethod
    def cssButtonLogout() -> str:
        return """
            TradingButton {
                font-family: monospace;
                padding: 0.25em;
            }
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
            }
        """

    @staticmethod
    def cssButtonLong() -> str:
        return """
            TradingButton {
                color: #008;
                background-color: #ddf;
                font-family: monospace;
                padding: 0.25em;
            }
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
            }
        """

    @staticmethod
    def cssButtonMonitor() -> str:
        return """
            TradingButton {
                color: #012;
                background-color: #def;
                font-family: monospace;
                padding: 0.5em;
            }        
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
            }
        """

    @staticmethod
    def cssButtonOrder() -> str:
        return """
            TradingButton {
                color: #121;
                background-color: #efe;
                font-family: monospace;
                padding: 0.5em;
            }        
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
            }
        """

    @staticmethod
    def cssButtonSearch() -> str:
        return """
            TradingButton {
                color: white;
                background-color: #6385cd;
                font-family: monospace;
                padding: 0 0.5em;
            }        
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
            }
        """

    @staticmethod
    def cssButtonShort() -> str:
        return """
            TradingButton {
                color: #800;
                background-color: #fdd;
                font-family: monospace;
                padding: 0.25em;
            }        
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
            }
        """

    @staticmethod
    def cssButtonStart() -> str:
        return """
            TradingButton {
                color: white;
                background-color: #bf0000;
                font-family: monospace;
                padding: 0.5em;
            }
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
                font-weight: normal;
            }
        """

    @staticmethod
    def cssButtonStatus() -> str:
        return """
            TradingButton {
                color: #fff;
                background-color: olive;
                font-family: monospace;
                font-size: 9pt;
            }        
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
            }
        """

    @staticmethod
    def cssButtonStop() -> str:
        return """
            TradingButton {
                color: white;
                background-color: #444;
                font-family: monospace;
                padding: 0.1em;
            }
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
                font-weight: normal;
            }
        """

    @staticmethod
    def cssButtonUpdate() -> str:
        return """
            TradingButton {
                font-family: monospace;
                font-size: 8pt;
                padding: 0 0.5em;
            }        
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
            }
        """


class TradingCheckButton(QCheckBox):
    def __init__(self, *args):
        super().__init__(*args)


class TradingRadioButton(QRadioButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.func = None
        self.mode = None
        self.xrange = None
        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.MinimumExpanding
        )
        self.setStyleSheet("""
            TradingRadioButton {
                font-family: monospace;
            }        
            TradingRadioButton:disabled {
                color: #888;
                background-color: #ddd;
            }
        """)
        self.setEnabled(False)

    def setFunc(self, func: str):
        self.func = func
        if func == 'update':
            self.setStyleSheet(self.cssButtonUpdate())

    def setMode(self, mode: str):
        self.mode = mode

    def setXAxisRange(self, xrange: XAxisRange):
        self.xrange = xrange

    def getFunc(self) -> str:
        return self.func

    def getMode(self) -> str:
        return self.mode

    def getXAxisRange(self) -> XAxisRange:
        return self.xrange

    @staticmethod
    def cssButtonUpdate() -> str:
        return """
            TradingRadioButton {
                font-family: monospace;
                font-size: 8pt;
                padding: 0 0.5em;
            }        
            TradingRadioButton:disabled {
                color: gray;
                background-color: lightgray;
            }
        """
