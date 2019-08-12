# coding: utf-8


TAKER_ORDER_STATUS = {
    "matched": "matched",
    "set_wallet": "set_wallet",
    "sended": "sended",
    "received": "received",
    "disputed": "disputed",
    "complete": "complete",
    "canceled": "canceled"
}

MAKER_ORDER_STATUS = {
    "pending":"pending",
    "createded": "createded",
    "matched": "matched",
    "set_wallet": "set_wallet",
    "sended": "sended",
    "received": "received",
    "disputed": "disputed",
    "complete": "complete",
    "canceled": "canceled"
}


EXCHANGE_PROCESS_STATUS = {
    "pending": "pending",
    'canceled': "canceled",
    'matched': "matched",
    'sended': "sended",
    'received': "received",
    'set_wallet': "set_wallet",
    'payed': "payed",
    'disputed': "disputed",
    'complete': "complete"
}


PROCESS_STATUS_EXPIRE_TIME = {
    #"matched": 10 * 60,
    "pending": 60 * 60,
    "matched": 5,
    "set_wallet": 60 * 60,
    "sended": 18 * 60 * 60
}

ENTRUST_TYPE = {
    "maker": "maker",
    "taker": "taker"
}

ECCHANGE_CURRENCY_TYPE = {
    'CNY': '1',
    'USD': '2'
}