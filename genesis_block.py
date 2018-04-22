import datetime as date
from block import Block


def create_genesis_block():
    return Block(0,
                 date.datetime.now(),
                 {
                     "proof-of-work": 6,
                     "transactions": None
                 },
                 "0")
