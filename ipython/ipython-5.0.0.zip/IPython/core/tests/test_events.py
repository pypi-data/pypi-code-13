import unittest
try:  # Python 3.3 +
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from IPython.core import events
import IPython.testing.tools as tt

def ping_received():
    pass

class CallbackTests(unittest.TestCase):
    def setUp(self):
        self.em = events.EventManager(get_ipython(), {'ping_received': ping_received})
    
    def test_register_unregister(self):
        cb = Mock()

        self.em.register('ping_received', cb)        
        self.em.trigger('ping_received')
        self.assertEqual(cb.call_count, 1)
        
        self.em.unregister('ping_received', cb)
        self.em.trigger('ping_received')
        self.assertEqual(cb.call_count, 1)
    
    def test_cb_error(self):
        cb = Mock(side_effect=ValueError)
        self.em.register('ping_received', cb)
        with tt.AssertPrints("Error in callback"):
            self.em.trigger('ping_received')

    def test_unregister_during_callback(self):
        invoked = [False] * 3
        
        def func1(*_):
            invoked[0] = True
            self.em.unregister('ping_received', func1)
            self.em.register('ping_received', func3)

        def func2(*_):
            invoked[1] = True
            self.em.unregister('ping_received', func2)

        def func3(*_):
            invoked[2] = True
            
        self.em.register('ping_received', func1)
        self.em.register('ping_received', func2)

        self.em.trigger('ping_received')
        self.assertEqual([True, True, False], invoked)
        self.assertEqual([func3], self.em.callbacks['ping_received'])
