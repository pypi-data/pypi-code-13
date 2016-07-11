# -*- coding: utf-8 -*-

"""
Basic Usage:

Dealer:
    dealer = BaseDealer()
    dealer.connect("tcp://localhost:1234")
    dealer.{method}({args})

Worker:
    worker = BaseWorker({Cls()})
    worker.bind("tcp://*:1234")
    worker.run()
"""




