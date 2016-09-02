# -*- coding: utf-8 -*-

import sys
#from ev3dev import *

def init():
    return 10

def coro_handle_ir_control():
    while True:
        print 1
        yield

def coro_handle_brick_control():
    global alive

    while True:
        print 2
        alive -= 1
        yield

def coro_drive():
    while True:
        print 3
        yield

if __name__ == '__main__':
    print 'Waiting the EV3 brick online...'
#    if not brick_init(): sys.exit( 1 )

    print '*** ( EV3 ) Hello! ***'
    alive = init()

    handle_ir_control = coro_handle_ir_control()
    handle_brick_control = coro_handle_brick_control()
    drive = coro_drive()

    while alive:
        handle_ir_control.next()
        handle_brick_control.next()
        drive.next()
#        sleep_ms( 10 )

#    brick_uninit()
    print
    print '*** ( EV3 ) Bye! ***'
