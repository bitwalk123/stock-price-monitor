from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout


class HBoxLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)


class VBoxLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
