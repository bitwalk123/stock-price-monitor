from PySide6.QtWidgets import QComboBox

from structs.web_info import WebInfoRakuten


def set_combo_status(combo: QComboBox, status: bool = True):
    combo.setEnabled(status)


class ComboBox(QComboBox):
    def __init__(self, info: WebInfoRakuten):
        super().__init__()
        self.info = info
        self.addItems(info.ticker.keys())
        self.setEnabled(False)

    def currentTicker(self) -> str:
        return self.info.ticker[self.currentText()]
