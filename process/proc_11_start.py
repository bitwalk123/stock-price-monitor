from PySide6.QtCore import Signal
from PySide6.QtTest import QTest

from process.process_base import ProcessBase
from threads.worker import (
    WorkerAutoLogout,
    WorkerDomestic,
    WorkerLogin,
    WorkerLoginSite,
    WorkerSearch,
    WorkerUpdateButtonAuto,
)


class Proc11Start(ProcessBase):
    processFinished = Signal()

    def __init__(self, parent, driver, info, threadpool):
        super().__init__(parent, driver, info, threadpool)

    # =========================================================================
    # RUN
    def run(self):
        # goto login site
        worker = WorkerLoginSite(self.driver, self.info)
        worker.threadFinished.connect(self.stage_1_login)
        self.threadpool.start(worker)

    def stage_1_login(self, result: bool):
        if not result:
            print('ログインサイトの表示ができませんでした。')
            return

        # login to site
        worker = WorkerLogin(self.driver, self.info)
        worker.threadFinished.connect(self.stage_2_domestic)
        self.threadpool.start(worker)

    def stage_2_domestic(self):
        print('ログインしました。')
        # goto domestic page
        worker = WorkerDomestic(self.driver, self.info)
        worker.threadFinished.connect(self.stage_3_search)
        self.threadpool.start(worker)

    def stage_3_search(self):
        QTest.qWait(1000)
        # search target ticker
        ticker = self.info.getTickerTarget()
        worker = WorkerSearch(self.driver, self.info, ticker)
        worker.threadFinished.connect(self.stage_4_autologout)
        self.threadpool.start(worker)

    def stage_4_autologout(self):
        # switch auto-login button
        worker = WorkerAutoLogout(self.driver, self.info)
        worker.threadFinished.connect(self.stage_5_update_auto)
        self.threadpool.start(worker)

    def stage_5_update_auto(self):
        QTest.qWait(1000)
        # enable auto update
        worker = WorkerUpdateButtonAuto(self.driver, self.info)
        worker.threadFinished.connect(self.stage_6_finished)
        self.threadpool.start(worker)

    def stage_6_finished(self):
        # notify job finished!
        self.processFinished.emit()
