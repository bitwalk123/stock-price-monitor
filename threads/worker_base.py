from PySide6.QtCore import QObject, Signal, QRunnable
from selenium import webdriver

from structs.web_info import WebInfoRakuten


class WorkerSignal1(QObject):
    threadFinished = Signal(bool)


class WorkerSignal2(QObject):
    threadFinished = Signal(bool, str)


class WorkerSignal3(QObject):
    threadFinished = Signal(str, str)


class WorkerSignal4(QObject):
    threadFinished = Signal(dict, dict)


class WorkerBase1(QRunnable, WorkerSignal1):
    def __init__(self, driver: webdriver.Firefox, info: WebInfoRakuten):
        super().__init__()
        self.driver = driver
        self.info = info

    def run(self):
        self.threadFinished.emit(True)


class WorkerBase2(QRunnable, WorkerSignal2):
    def __init__(self, driver: webdriver.Firefox, info: WebInfoRakuten):
        super().__init__()
        self.driver = driver
        self.info = info

    def run(self):
        self.threadFinished.emit(True, None)


class WorkerBase3(QRunnable, WorkerSignal3):
    def __init__(self, driver: webdriver.Firefox, info: WebInfoRakuten):
        super().__init__()
        self.driver = driver
        self.info = info

    def run(self):
        self.threadFinished.emit(None, None)


class WorkerBase4(QRunnable, WorkerSignal4):
    def __init__(self, driver: webdriver.Firefox, info: WebInfoRakuten):
        super().__init__()
        self.driver = driver
        self.info = info

    def run(self):
        self.threadFinished.emit(dict(), dict())
