from PySide6.QtCore import QObject, QThreadPool
from selenium import webdriver

from structs.web_info import WebInfoRakuten


class ProcessBase(QObject):
    def __init__(
            self,
            parent,
            driver: webdriver.Firefox,
            info: WebInfoRakuten,
            threadpool: QThreadPool
    ):
        super().__init__(parent)
        self.driver = driver
        self.info = info
        self.threadpool = threadpool
