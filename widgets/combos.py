from PySide6.QtWidgets import QComboBox

from structs.web_info import WebInfoRakuten


def set_combo_status(combo: QComboBox, status: bool = True):
    combo.setEnabled(status)


class ComboBoxTicker(QComboBox):
    def __init__(self, info: WebInfoRakuten):
        super().__init__()
        self.dict_ticker = info.getTicker()
        self.addItems(list(self.dict_ticker.keys()))
        self.setEnabled(False)

    def currentTicker(self) -> str:
        return self.dict_ticker[self.currentText()]
