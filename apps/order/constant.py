# coding: utf-8


TAKER_ORDER_STATUS = {
    "matched": 1,
    "set_wallet": 2,
     "sended": 3,
     "received":4,
    "disputed": 5,
    "complete": 6,
    "canceled": 7
}


PROCESS_STATUS_EXPIRE_TIME = {
    "pending": 60 * 60,
    "matched": 10 * 60,
    "set_wallet": 60 * 60,
    "sended": 18 * 60 * 60
}