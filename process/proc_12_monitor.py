import os

import pandas as pd
import re

from PySide6.QtCore import Signal, QTimer

from funcs.output import (
    get_result_pkl_filename,
    show_dict_contents,
)
from process.process_base import ProcessBase
from threads.worker import (
    WorkerAutoUpdateStatus,
    WorkerStatus,
    WorkerUpdateButtonAuto,
)


class Proc12Monitor(ProcessBase):
    dataUpdated = Signal(pd.DataFrame, float, pd.Timestamp)
    processFinished = Signal()

    def __init__(self, parent, driver, info, threadpool):
        super().__init__(parent, driver, info, threadpool)
        # _____________________________________________________________________
        self.dict_state = dict()
        # _____________________________________________________________________
        # timer & stock price related
        self.timer = QTimer(self)
        self.lock = False
        self.at_price = None
        self.at_time = None
        self.pattern_time = re.compile('（([0-9]{1,2}:[0-9]{2}:[0-9]{2})）')
        self.df = pd.DataFrame()

    # =========================================================================
    # RUN
    def run(self):
        print('監視状態に入ります。')
        worker = WorkerStatus(self.driver, self.info)
        worker.threadFinished.connect(self.stage_1_status)
        self.threadpool.start(worker)

    def stage_1_status(self, dict_state: dict, dict_price: dict):
        self.update_stock_price(dict_price)
        show_dict_contents(dict_state)

        self.dict_state = dict_state
        self.timer.timeout.connect(self.stage_2_loop)
        self.timer.start(1000)

    def stage_2_loop(self):
        if self.lock:
            return

        worker = WorkerStatus(self.driver, self.info)
        worker.threadFinished.connect(self.stage_3_compare_status)
        self.threadpool.start(worker)

    def stage_3_compare_status(self, dict_state: dict, dict_price: dict):
        if self.at_time != dict_price['time']:
            self.update_stock_price(dict_price)

        for key in dict_state.keys():
            if self.dict_state[key] != dict_state[key]:
                print('\'%s\' の状態が変更されました' % key)
                show_dict_contents(dict_state)
                self.dict_state = dict_state
                if dict_state['auto-update-off-select'] == 'display: block;':
                    self.lock = True
                    self.stage_4_update_flush()
                break

    def stage_4_update_flush(self):
        worker = WorkerAutoUpdateStatus(self.driver, self.info)
        worker.threadFinished.connect(self.stage_5_update_auto)
        self.threadpool.start(worker)

    def stage_5_update_auto(self):
        worker = WorkerUpdateButtonAuto(self.driver, self.info)
        worker.threadFinished.connect(self.stage_6_get_status)
        self.threadpool.start(worker)

    def stage_6_get_status(self):
        worker = WorkerStatus(self.driver, self.info)
        worker.threadFinished.connect(self.stage_7_show_status)
        self.threadpool.start(worker)

    def stage_7_show_status(self, dict_state: dict, dict_price: dict):
        print('更新しました')
        if self.at_time != dict_price['time']:
            self.update_stock_price(dict_price)

        show_dict_contents(dict_state)
        self.dict_state = dict_state
        self.lock = False

    # =========================================================================
    # STOP monitoring
    def stop(self):
        # stop timer if running
        if self.timer.isActive():
            print('タイマーを止めて監視を終了しました。')
            self.timer.stop()

        # print(self.df)
        if len(self.df) > 1:
            ticker = self.info.getTickerTarget()
            pkl = get_result_pkl_filename(ticker)
            if os.path.exists(pkl):
                print('【上書保存】 %s' % pkl)
            else:
                print('【新規保存】 %s' % pkl)
            self.df.to_pickle(pkl)
        else:
            print('【保存データなし】')

        self.processFinished.emit()

    # =========================================================================
    def update_stock_price(self, dict_price: dict):
        if dict_price['time'] is None:
            return

        self.at_price = dict_price['price']
        self.at_time = dict_price['time']

        price_value = None
        price_time = None

        try:
            price_value = float(self.at_price.replace(',', ''))
        except ValueError:
            price_value = self.at_price
        else:
            m = self.pattern_time.match(self.at_time)
            if m:
                price_time = pd.to_datetime(m.group(1))
                # print('DEBUG', price_time, type(price_time))

                if len(self.df) == 0:
                    self.df = pd.DataFrame({'Price': [price_value]}, index=[price_time])
                else:
                    self.df.loc[price_time] = price_value
                # signal to send data
                self.dataUpdated.emit(self.df, price_value, price_time)
            else:
                price_time = self.at_time
        # finally:
        #    print('%s at %s' % (price_value, price_time))
