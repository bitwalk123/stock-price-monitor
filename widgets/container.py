from PySide6.QtWidgets import (
    QFrame,
    QSizePolicy,
    QWidget,
)


class Container(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )


class Frame(QFrame):
    def __init__(self):
        super().__init__()
        self.setLineWidth(2)
        self.setContentsMargins(1, 1, 1, 1)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)


class HPad(QWidget):
    def __init__(self, w: None | int = None):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        if w is None:
            self.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Preferred
            )
        else:
            self.setFixedWidth(w)


class VPad(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding,
        )
