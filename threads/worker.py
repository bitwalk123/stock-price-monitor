from selenium import webdriver
from selenium.common import StaleElementReferenceException

from funcs.web import (
    do_autologout,
    do_credit,
    do_domestic,
    do_login,
    do_logout,
    do_long,
    do_search,
    do_short,
    do_update,
    do_update_button_auto,
    do_update_button_manual,
    get_auto_update_status,
    get_autologout_checked_status,
    get_stock_price,
    site_login,
)
from structs.web_info import WebInfoRakuten
from threads.worker_base import (
    WorkerBase1,
    WorkerBase2,
    WorkerBase3,
    WorkerBase4,
)


class WorkerAutoLogout(WorkerBase2):
    def __init__(self, driver: webdriver.Firefox, info: WebInfoRakuten):
        super().__init__(driver, info)

    def run(self):
        result = do_autologout(self.driver, self.info)
        status = get_autologout_checked_status(self.driver, self.info)
        self.threadFinished.emit(result, status)


class WorkerAutoUpdateStatus(WorkerBase1):
    def __init__(self, driver: webdriver.Firefox, info: WebInfoRakuten):
        super().__init__(driver, info)

    def run(self):
        do_update(self.driver, self.info)
        self.threadFinished.emit(True)


class WorkerCurrentPrice(WorkerBase3):
    def __init__(self, driver: webdriver.Firefox, info: WebInfoRakuten):
        super().__init__(driver, info)

    def run(self):
        self.threadFinished.emit(*get_stock_price(self.driver, self.info))


class WorkerCredit(WorkerBase1):
    def __init__(self, driver: webdriver.Firefox, info: WebInfoRakuten):
        super().__init__(driver, info)

    def run(self):
        result = do_credit(self.driver, self.info)
        self.threadFinished.emit(result)


class WorkerDomestic(WorkerBase1):
    def __init__(self, driver: webdriver.Firefox, info: WebInfoRakuten):
        super().__init__(driver, info)

    def run(self):
        result = do_domestic(self.driver, self.info)
        self.threadFinished.emit(result)


class WorkerLogin(WorkerBase1):
    def __init__(self, driver: webdriver.Firefox, info: WebInfoRakuten):
        super().__init__(driver, info)

    def run(self):
        result = do_login(self.driver, self.info)
        self.threadFinished.emit(result)


class WorkerLoginSite(WorkerBase1):
    def __init__(self, driver: webdriver.Firefox, info: WebInfoRakuten):
        super().__init__(driver, info)

    def run(self):
        self.threadFinished.emit(site_login(self.driver, self.info))


class WorkerLogout(WorkerBase1):
    def __init__(self, driver: webdriver.Firefox, info: WebInfoRakuten):
        super().__init__(driver, info)

    def run(self):
        result = do_logout(self.driver, self.info)
        self.threadFinished.emit(result)


class WorkerLong(WorkerBase1):
    def __init__(self, driver: webdriver.Firefox, info: WebInfoRakuten):
        super().__init__(driver, info)

    def run(self):
        result = do_long(self.driver, self.info)
        self.threadFinished.emit(result)


class WorkerSearch(WorkerBase2):
    def __init__(self, driver: webdriver.Firefox, info: WebInfoRakuten, ticker: str):
        super().__init__(driver, info)
        self.ticker = ticker

    def run(self):
        result = do_search(self.driver, self.info, self.ticker)
        self.threadFinished.emit(result, self.ticker)


class WorkerShort(WorkerBase1):
    def __init__(self, driver: webdriver.Firefox, info: WebInfoRakuten):
        super().__init__(driver, info)

    def run(self):
        result = do_short(self.driver, self.info)
        self.threadFinished.emit(result)


class WorkerStatus(WorkerBase4):
    def __init__(self, driver: webdriver.Firefox, info: WebInfoRakuten):
        super().__init__(driver, info)

    def run(self):
        # 現在の株価
        dict_price = dict()
        try:
            price_str, time_str = get_stock_price(self.driver, self.info)
        except StaleElementReferenceException:
            dict_price['result'] = False
            dict_price['price'] = None
            dict_price['time'] = None
        else:
            dict_price['result'] = True
            dict_price['price'] = price_str
            dict_price['time'] = time_str

        # 自動更新関連の状態
        dict_status = get_auto_update_status(self.driver, self.info)
        # 自動ログアウトの状態
        dict_status['auto-logout'] = get_autologout_checked_status(self.driver, self.info)

        self.threadFinished.emit(dict_status, dict_price)


class WorkerUpdateButtonAuto(WorkerBase1):
    def __init__(self, driver: webdriver.Firefox, info: WebInfoRakuten):
        super().__init__(driver, info)

    def run(self):
        self.threadFinished.emit(do_update_button_auto(self.driver, self.info))


class WorkerUpdateButtonManual(WorkerBase1):
    def __init__(self, driver: webdriver.Firefox, info: WebInfoRakuten):
        super().__init__(driver, info)

    def run(self):
        self.threadFinished.emit(do_update_button_manual(self.driver, self.info))
