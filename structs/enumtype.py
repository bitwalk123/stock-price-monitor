from enum import Enum


class TypeDeal(Enum):
    BUYSELL = 1
    TRANSACTION = 2
    FORCE = 3


class XAxisRange(Enum):
    DAY = 1
    AM = 2
    PM = 3
