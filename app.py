import sys

from PySide6.QtWidgets import QApplication
from ui.main_monitor import MainMonitor


def main():
    app = QApplication(sys.argv)
    win = MainMonitor()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
