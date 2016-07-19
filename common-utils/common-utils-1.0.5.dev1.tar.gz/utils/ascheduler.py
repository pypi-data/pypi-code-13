#! /usr/bin/evn python
# coding=UTF-8

import time
import sched
import datetime

class TimeAfterTimeScheduler:
    def __init__(self, delay_time=10, max_times=0):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.delay_time = delay_time
        if max_times<=0:
            self.max_times=0
        else:
            self.max_times = max_times

        self.times = 0
        self._current_event=None

    def register_task_func(self, task_func, condition_func=None, terminal_func=None):
        if hasattr(task_func, '__call__') == False:
            raise TypeError("The argument of task_func should be a function.")

        if condition_func and hasattr(condition_func, '__call__') == False:
            raise TypeError(
                "The argument of condition_func should be a function.")

        if terminal_func and hasattr(terminal_func, '__call__') == False:
            raise TypeError(
                "The argument of terminal_func should be a function.")

        self.task_func = task_func
        self.condition_func = condition_func
        self.terminal_func = terminal_func

    def _perform(self):
        if self.terminal_func is not None:
            if self.terminal_func() == True:
                return

        if self.max_times>0 and self.max_times<=self.times:
            return

        flag = True
        if self.condition_func is not None:
            if self.condition_func() == False:
                flag = False

        if flag:
            self.task_func()
        
        self.times=self.times+1

        self._current_event=self.scheduler.enter(self.delay_time, 0, self._perform, ())

    def run(self):
        self._current_event=self.scheduler.enter(0, 0, self._perform, ())
        self.scheduler.run()




class TimeRangeScheduler:

    def __init__(self,start_time,end_time,interval_type,intervals,delay_time=10, max_times=0):
        self.INTERVAL_TYPE=['days','hours','minutes','seconds']
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.delay_time = delay_time
        if isinstance(start_time,datetime.datetime):
            self.start_time=start_time
        else:
            raise TypeError("The argument start_time should be a datetime.datetime object.")

        if isinstance(end_time,datetime.datetime):
            self.end_time=end_time
        else:
            raise TypeError("The argument end_time should be a datetime.datetime object.")

        if interval_type and interval_type in self.INTERVAL_TYPE:
            self.interval_type=interval_type
        else:
            raise TypeError("he argument interval_type should be a value in %s." %(self.INTERVAL_TYPE))

        self.intervals=int(intervals)

        if max_times<=0:
            self.max_times=0
        else:
            self.max_times = max_times

        self.times = 0
        self._current_event=None
        
        if start_time>=end_time:
            self._step_direction=-1
        else:
            self._step_direction=1

        self.current_time=start_time

    def register_task_func(self, task_func,task_func_args, condition_func=None, terminal_func=None):
        if hasattr(task_func, '__call__') == False:
            raise TypeError("The argument of task_func should be a function.")

        if condition_func and hasattr(condition_func, '__call__') == False:
            raise TypeError(
                "The argument of condition_func should be a function.")

        if terminal_func and hasattr(terminal_func, '__call__') == False:
            raise TypeError(
                "The argument of terminal_func should be a function.")

        self.task_func = task_func
        self.task_func_args=task_func_args
        self.condition_func = condition_func
        self.terminal_func = terminal_func

    def _perform(self):
        if self.terminal_func is not None:
            if self.terminal_func() == True:
                return

        if self.max_times>0 and self.max_times<=self.times:
            return

        flag = True
        if self.condition_func is not None:
            if self.condition_func() == False:
                flag = False

        if self._step_direction==1:
            if self.current_time>self.end_time:
                return
        else:
            if self.current_time<self.end_time:
                return

        if flag:
            self.task_func(**self.task_func_args)

            steps={self.interval_type:self._step_direction*self.intervals}
            self.current_time=self.current_time+datetime.timedelta(**steps)

        self.times=self.times+1

        self._current_event=self.scheduler.enter(self.delay_time, 0, self._perform, ())

    def run(self):
        self._current_event=self.scheduler.enter(0, 0, self._perform, ())
        self.scheduler.run()


