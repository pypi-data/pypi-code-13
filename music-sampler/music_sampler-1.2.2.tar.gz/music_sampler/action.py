from transitions.extensions import HierarchicalMachine as Machine
from .helpers import debug_print, error_print
from . import actions

class Action:
    STATES = [
        'initial',
        'loading',
        'failed',
        {
            'name': 'loaded',
            'children': ['running']
        }
    ]

    TRANSITIONS = [
        {
            'trigger': 'load',
            'source': 'initial',
            'dest': 'loading'
        },
        {
            'trigger': 'fail',
            'source': 'loading',
            'dest': 'failed',
            'after': 'poll_loaded'
        },
        {
            'trigger': 'success',
            'source': 'loading',
            'dest': 'loaded',
            'after': 'poll_loaded'
        },
        {
            'trigger': 'run',
            'source': 'loaded',
            'dest': 'loaded_running',
            'after': 'finish_action',
            # if a child has no transitions, then it is bubbled to the parent,
            # and we don't want that. Not useful in that machine precisely.
            'conditions': ['is_loaded']
        },
        {
            'trigger': 'finish_action',
            'source': 'loaded_running',
            'dest': 'loaded'
        }
    ]

    def __init__(self, action, key, **kwargs):
        Machine(model=self, states=self.STATES,
                transitions=self.TRANSITIONS, initial='initial',
                ignore_invalid_triggers=True, queued=True)

        self.action = action
        self.key = key
        self.mapping = key.parent
        self.arguments = kwargs
        self.sleep_event = None
        self.waiting_music = None

    def is_loaded_or_failed(self):
        return self.is_loaded(allow_substates=True) or self.is_failed()

    def callback_music_loaded(self, success):
        if success:
            self.success()
        else:
            self.fail()

    # Machine states / events
    def on_enter_loading(self):
        if hasattr(actions, self.action):
            if 'music' in self.arguments:
                self.arguments['music'].subscribe_loaded(
                        self.callback_music_loaded)
            else:
                self.success()
        else:
            error_print("Unknown action {}".format(self.action))
            self.fail()

    def on_enter_loaded_running(self, key_start_time):
        debug_print(self.description())
        if hasattr(actions, self.action):
            getattr(actions, self.action).run(self,
                    key_start_time=key_start_time, **self.arguments)

    def poll_loaded(self):
        self.key.callback_action_ready(self,
                self.is_loaded(allow_substates=True))

    # This one cannot be in the Machine state since it would be queued to run
    # *after* the wait is ended...
    def interrupt(self):
        if getattr(actions, self.action, None) and\
                hasattr(getattr(actions, self.action), 'interrupt'):
            return getattr(getattr(actions, self.action), 'interrupt')(
                    self, **self.arguments)

    # Helpers
    def music_list(self, music):
        if music is not None:
            return [music]
        else:
            return self.mapping.open_files.values()

    def description(self):
        if hasattr(actions, self.action):
            return getattr(actions, self.action)\
                    .description(self, **self.arguments)
        else:
            return _("unknown action {}").format(self.action)
