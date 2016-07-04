import types
from multiprocessing.dummy import Pool
import search_engine_app
from  search_engine_app.utils.Trace import Trace


class ThreadPoolService:
    
    @staticmethod
    def processTasksWithArguments(pool_size,arguments_array,user_callable):

        """
        Process concurency tasks with arguments.
        Apply `callable` to each element in `arguments_array`, response the list of results if all tasks was finished

        @type Integer: int
        @param pool_size: amount of threads in the pool must be positive number

        @type List: list
        @param arguments_array: list of arguments that will be mapped to callable

        @type callable: callable
        @param user_callable: function that should applyied on arguments_array
        """
        Trace.thread_trace("START processTasksWithArguments")
        if not isinstance(pool_size, int) or pool_size <= 0:
            raise TypeError('pool_size must be positive number')
        if not isinstance(arguments_array, list) or len(arguments_array) == 0:
                raise TypeError('arguments_array should be not empty list')
        if not isinstance(user_callable, types.FunctionType):
            raise TypeError('user_callable should be ninstance of callable')

        threadPool = Pool(pool_size)
        Trace.thread_trace("\tSTART threadPool.map")
        results_array = threadPool.map(user_callable, arguments_array)
        threadPool.close()
        threadPool.join()
        Trace.thread_trace("\tEND threadPool.map")
        Trace.thread_trace("END processTasksWithArguments")
        return results_array
