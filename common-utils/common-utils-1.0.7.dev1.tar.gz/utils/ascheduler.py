#! /usr/bin/evn python
# coding=UTF-8
"""Library for simplifying coding process for usage scenarios of scheduling.

This module provides easy ways to schedule your functions.

Available classes:
- TimeAfterTimeScheduler: Execute registered function time after time.
- TimeRangeScheduler: Execute registered function between start time and end time.

"""

import time
import sched
import datetime

class TimeAfterTimeScheduler:
    """TimeAfterTimeScheduler is a scheduler that will execute registered function time after time.

    You can create an object of TimeAfterTimeScheduler,then execute registered function time after time.
    If you passed number greater than 0 for 'max_times' parameter,when executed times is equal to 'max_times' the process will be terminal.
    If you want to skip the stage of executing registered function at this time,you may define a condition function that returns boolean value,and then when register task function ,you can pass it to 'register_task_func' function.When this condition function returns false,the executing stage will be skipped.
    If you want to terminate this process,you can define a terminal function for 'register_task_func'.When the terminal function returns True,the process will be terminal.

    Attributes
    ----------
    delay_time : int
        Intervals time.
    max_times : int
        Maximum Times for executing registered function.
    times : int
        How times the registered function has been executed.

    Parameters
    ----------
    delay_time : int
        Among executing task function will sleep for [delay_time] seconds.
        Default is 10.
    max_times : int
        The settings of hive client.
        Default is 0.It doesn't work.
        When you passed negative integer,it will be looked as 0.

    Examples
    --------
    >>> from utils.ascheduler import TimeAfterTimeScheduler
    >>> def say_hello(): print("hello")
    >>> scheduler=TimeAfterTimeScheduler(delay_time=10,max_times=2)
    >>> scheduler.register_task_func(task_func=say_hello)
    >>> scheduler.run()
    hello
    hello
    >>>
    """
    def __init__(self, delay_time=10, max_times=0):
        self._scheduler = sched.scheduler(time.time, time.sleep)
        self.delay_time = delay_time
        if max_times<=0:
            self._max_times=0
        else:
            self._max_times = max_times

        self._times = 0
        self._current_event=None

    @property
    def times(self):
        "The times property - the getter"
        return self._times

    @property
    def max_times(self):
        "The max_times property - the getter"
        return self._max_times

    def register_task_func(self, task_func, condition_func=None, terminal_func=None):
        """Register task,condition and terminal functions.

        This function only receives three functions,you should make sure that
        condition and terminal function can return True or False.

        Parameters
        ----------
        task_func : function
            The task function will be executed in the process.
        condition_func : Optional[function]
            Condition function controls when task function to execute.
        terminal_func : Optional[function]
            Terminal function controls when this process ends.

        Raises
        ------
        TypeError
            These parameters aren't functions.

        """
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

        if self._max_times>0 and self._max_times<=self._times:
            return

        flag = True
        if self.condition_func is not None:
            if self.condition_func() == False:
                flag = False

        if flag:
            self.task_func()
        
        self._times=self._times+1

        self._current_event=self._scheduler.enter(self.delay_time, 0, self._perform, ())

    def run(self):
        self._current_event=self._scheduler.enter(0, 0, self._perform, ())
        self._scheduler.run()




class TimeRangeScheduler:
    """TimeRangeScheduler is a scheduler that will execute registered function between start time and end time.

    You can create an object of TimeRangeScheduler,then execute registered function.When you call 'register_task_func function',you can pass the task function and its parameters.
    If you passed number greater than 0 for 'max_times' parameter,when executed times is equal to 'max_times' the process will be terminal.
    If you want to skip the stage of executing registered function at this time,you may define a condition function that returns boolean value,and then when register task function ,you can pass it to 'register_task_func' function.When this condition function returns false,the executing stage will be skipped.
    If you want to terminate this process,you can define a terminal function for 'register_task_func'.When the terminal function returns True,the process will be terminal.

    Attributes
    ----------
    delay_time : int
        Intervals time.
    max_times : int
        Maximum Times for executing registered function.
    times : int
        How times the registered function has been executed.
    current_time : datetime
        Current executing time.

    Parameters
    ----------
    start_time : datetime
        Execute task function from start time.
    end_time : datetime
        Execute task function will be terminal after end time.
    interval_type : str
        Interval type must be a value below sequence.
        ['days','hours','minutes','seconds']
    intervals : int
        Among executing task function will sleep for [delay_time] seconds.
        Default is 1.
    delay_time : int
        Among executing task function will sleep for [delay_time] seconds.
        Default is 10.
    max_times : int
        The settings of hive client.
        Default is 0.It doesn't work.
        When you passed negative integer,it will be looked as 0.

    Examples
    --------
    >>> import datetime
    >>> from utils.ascheduler import TimeRangeScheduler
    >>> def say_hello(scheduler): print("hello ,times:%s,current_time:%s" %(scheduler.times,scheduler.current_time))
    >>> s_time=datetime.datetime.strptime("2016060112","%Y%m%d%H")
    >>> e_time=datetime.datetime.strptime("2016060123","%Y%m%d%H")
    >>> scheduler=TimeRangeScheduler(s_time,e_time,"hours",1)
    >>> scheduler.register_task_func(task_func=say_hello,task_func_args={"scheduler":scheduler})
    >>> scheduler.run()
    hello ,times:0,current_time:2016-06-01 12:00:00
    hello ,times:1,current_time:2016-06-01 13:00:00
    .....
    hello ,times:10,current_time:2016-06-01 22:00:00
    hello ,times:11,current_time:2016-06-01 23:00:00
    >>>
    >>> scheduler=TimeRangeScheduler(e_time,s_time,"hours",1)
    >>> scheduler.register_task_func(task_func=say_hello,task_func_args={"scheduler":scheduler})
    >>> scheduler.run()
    hello ,times:0,current_time:2016-06-01 23:00:00
    hello ,times:1,current_time:2016-06-01 22:00:00
    .....
    hello ,times:10,current_time:2016-06-01 13:00:00
    hello ,times:11,current_time:2016-06-01 12:00:00
    """

    def __init__(self,start_time,end_time,interval_type,intervals=1,delay_time=10, max_times=0):
        self.INTERVAL_TYPE=['days','hours','minutes','seconds']
        self._scheduler = sched.scheduler(time.time, time.sleep)
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
            self._max_times=0
        else:
            self._max_times = max_times

        self._times = 0
        self._current_event=None
        
        if start_time>=end_time:
            self._step_direction=-1
        else:
            self._step_direction=1

        self._current_time=start_time

    @property  
    def times(self):
        "The times property - the getter"
        return self._times

    @property
    def max_times(self):
        "The max_times property - the getter"
        return self._max_times

    @property  
    def current_time(self):
        "The current_time property - the getter"
        return self._current_time

    def register_task_func(self, task_func,task_func_args, condition_func=None, terminal_func=None):
        """Register task function ,task function parameters,condition and terminal functions.

        This function receives three functions and one function parameter,you should make sure that
        condition and terminal function can return True or False.

        Parameters
        ----------
        task_func : function
            The task function will be executed in the process.
        task_func_args : dict
            The 'task_func_args' will pass to 'task_func' as parameters.
        condition_func : Optional[function]
            Condition function controls when task function to execute.
        terminal_func : Optional[function]
            Terminal function controls when this process ends.

        Raises
        ------
        TypeError
            The 'task_func','condition_func' and 'terminal_func' aren't functions.
            The 'task_func_args' not be a dict.

        """
        if hasattr(task_func, '__call__') == False:
            raise TypeError("The argument of task_func should be a function.")

        if isinstance(task_func_args,dict) == False:
            raise TypeError("The argument of task_func_args should be a dict object")

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

        if self._max_times>0 and self._max_times<=self._times:
            return

        flag = True
        if self.condition_func is not None:
            if self.condition_func() == False:
                flag = False

        if self._step_direction==1:
            if self._current_time>self.end_time:
                return
        else:
            if self._current_time<self.end_time:
                return

        if flag:
            self.task_func(**self.task_func_args)

            steps={self.interval_type:self._step_direction*self.intervals}
            self._current_time=self._current_time+datetime.timedelta(**steps)

        self._times=self._times+1

        self._current_event=self._scheduler.enter(self.delay_time, 0, self._perform, ())

    def run(self):
        self._current_event=self._scheduler.enter(0, 0, self._perform, ())
        self._scheduler.run()


