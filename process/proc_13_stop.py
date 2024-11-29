from PySide6.QtCore import Signal

from process.process_base import ProcessBase
from threads.worker import WorkerLogout


class Proc13Stop(ProcessBase):
    processFinished = Signal()

    def __init__(self, parent, driver, info, threadpool):
        super().__init__(parent, driver, info, threadpool)

    def run(self):
        # logout from site
        worker = WorkerLogout(self.driver, self.info)
        worker.threadFinished.connect(self.stage_1_post_logout)
        self.threadpool.start(worker)

    def stage_1_post_logout(self):
        self.processFinished.emit()