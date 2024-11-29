from PySide6.QtWidgets import QToolBar


class ToolBar(QToolBar):

    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)

