from kivy.uix.widget import Widget
from kivy.properties import AliasProperty, BooleanProperty, \
                            ListProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior

from .action import Action
from .helpers import debug_print
import time
import threading
from transitions.extensions import HierarchicalMachine as Machine

class KeyMachine(Widget):
    STATES = [
        'initial',
        'configuring',
        'configured',
        'loading',
        'failed',
        {
            'name': 'loaded',
            'children': [
                'no_config',
                'no_actions',
                'running',
                'protecting_repeat'
            ]
        }
    ]

    TRANSITIONS = [
        {
            'trigger': 'configure',
            'source': 'initial',
            'dest': 'configuring'
        },
        {
            'trigger': 'fail',
            'source': 'configuring',
            'dest': 'failed',
            'after': 'key_loaded_callback'
        },
        {
            'trigger': 'success',
            'source': 'configuring',
            'dest': 'configured',
            'after': 'load'
        },
        {
            'trigger': 'no_config',
            'source': 'configuring',
            'dest': 'loaded_no_config',
            'after': 'key_loaded_callback'
        },
        {
            'trigger': 'load',
            'source': 'configured',
            'dest': 'loading'
        },
        {
            'trigger': 'fail',
            'source': 'loading',
            'dest': 'failed',
            'after': 'key_loaded_callback'
        },
        {
            'trigger': 'success',
            'source': 'loading',
            'dest': 'loaded',
            'after': 'key_loaded_callback'
        },
        {
            'trigger': 'no_actions',
            'source': 'loading',
            'dest': 'loaded_no_actions',
            'after': 'key_loaded_callback'
        },
        {
            'trigger': 'reload',
            'source': ['loaded','failed'],
            'dest': 'configuring',
            'after': 'key_loaded_callback'
        },
        {
            'trigger': 'run',
            'source': 'loaded',
            'dest': 'loaded_running',
            'after': ['run_actions', 'finish'],
            # if a child, like loaded_no_actions, has no transitions, then it
            # is bubbled to the parent, and we don't want that.
            'conditions': ['is_loaded']
        },
        {
            'trigger': 'finish',
            'source': 'loaded_running',
            'dest': 'loaded_protecting_repeat'
        },
        {
            'trigger': 'repeat_protection_finished',
            'source': 'loaded_protecting_repeat',
            'dest': 'loaded'
        },
    ]

    state = StringProperty("")

    def __init__(self, key, **kwargs):
        self.key = key

        Machine(model=self, states=self.STATES,
                transitions=self.TRANSITIONS, initial='initial',
                ignore_invalid_triggers=True, queued=True)
        super(KeyMachine, self).__init__(**kwargs)

    # Machine states / events
    def is_loaded_or_failed(self):
        return self.is_loaded(allow_substates=True) or self.is_failed()

    def is_loaded_inactive(self):
        return self.is_loaded_no_config() or self.is_loaded_no_actions()

    def on_enter_configuring(self):
        if self.key.key_sym in self.key.parent.key_config:
            self.key.config = self.key.parent.key_config[self.key.key_sym]

            self.key.actions = []
            for key_action in self.key.config['actions']:
                self.key.add_action(key_action[0], **key_action[1])

            if 'description' in self.key.config['properties']:
                self.key.set_description(self.key.config['properties']['description'])
            else:
                self.key.unset_description()
            if 'color' in self.key.config['properties']:
                self.key.set_color(self.key.config['properties']['color'])
            else:
                self.key.unset_color()
            self.success()
        else:
            self.no_config()

    def on_enter_loading(self):
        if len(self.key.actions) > 0:
            for action in self.key.actions:
                action.load()
        else:
            self.no_actions()

    def run_actions(self, modifiers):
        self.key.parent.parent.ids['KeyList'].append(self.key.key_sym)
        debug_print("running actions for {}".format(self.key.key_sym))
        start_time = time.time()
        self.key.parent.start_running(self.key, start_time)
        for self.key.current_action in self.key.actions:
            if self.key.parent.keep_running(self.key, start_time):
                self.key.list_actions()
                self.key.current_action.run(start_time)
        self.key.list_actions(last_action_finished=True)

        self.key.parent.finished_running(self.key, start_time)

    def on_enter_loaded_protecting_repeat(self, modifiers):
        if self.key.repeat_delay > 0:
            self.key.protecting_repeat_timer = threading.Timer(
                    self.key.repeat_delay,
                    self.key.repeat_protection_finished)
            self.key.protecting_repeat_timer.start()
        else:
            self.key.repeat_protection_finished()

    # Callbacks
    def key_loaded_callback(self):
        self.key.parent.key_loaded_callback()


class Key(ButtonBehavior, Widget):

    key_sym = StringProperty(None)
    custom_color = ListProperty([0, 1, 0])
    description_title = StringProperty("")
    description = ListProperty([])
    machine_state = StringProperty("")

    def get_alias_line_cross_color(self):
        if not self.is_failed() and (
                not self.is_loaded(allow_substates=True)\
                or self.is_loaded_running()\
                or self.is_loaded_protecting_repeat()):
            return [120/255, 120/255, 120/255, 1]
        else:
            return [0, 0, 0, 0]

    def set_alias_line_cross_color(self):
        pass

    line_cross_color = AliasProperty(
            get_alias_line_cross_color,
            set_alias_line_cross_color,
            bind=['machine_state'])

    def get_alias_line_color(self):
        if self.is_loaded_running():
            return [0, 0, 0, 1]
        else:
            return [120/255, 120/255, 120/255, 1]

    def set_alias_line_color(self):
        pass

    line_color = AliasProperty(get_alias_line_color, set_alias_line_color,
            bind=['machine_state'])

    def get_alias_color(self):
        if self.is_loaded_inactive():
            return [1, 1, 1, 1]
        elif self.is_loaded_protecting_repeat():
            return [*self.custom_color, 100/255]
        elif self.is_loaded_running():
            return [*self.custom_color, 100/255]
        elif self.is_loaded(allow_substates=True):
            return [*self.custom_color, 1]
        elif self.is_failed():
            return [0, 0, 0, 1]
        else:
            return [*self.custom_color, 100/255]
    def set_alias_color(self):
        pass

    color = AliasProperty(get_alias_color, set_alias_color,
            bind=['machine_state', 'custom_color'])

    def __getattr__(self, name):
        if hasattr(self.machine, name):
            return getattr(self.machine, name)
        else:
            raise AttributeError

    def machine_state_changed(self, instance, machine_state):
        self.machine_state = self.machine.state

    def __init__(self, **kwargs):
        self.actions = []
        self.current_action = None
        self.machine = KeyMachine(self)
        self.machine.bind(state=self.machine_state_changed)

        super(Key, self).__init__(**kwargs)

    # Kivy events
    def on_key_sym(self, key, key_sym):
        if key_sym != "":
            self.configure()

    def on_press(self):
        self.list_actions()

    # This one cannot be in the Machine state since it would be queued to run
    # *after* the loop is ended...
    def interrupt(self):
        self.current_action.interrupt()

    # Callbacks
    def callback_action_ready(self, action, success):
        if not success:
            self.fail()
        elif all(action.is_loaded_or_failed() for action in self.actions):
            self.success()

    # Setters
    def set_description(self, description):
        if description[0] is not None:
            self.description_title = str(description[0])
        self.description = []
        for desc in description[1 :]:
            if desc is None:
                self.description.append("")
            else:
                self.description.append(str(desc).replace(" ", " "))

    def unset_description(self):
        self.description_title = ""
        self.description = []

    def set_color(self, color):
        color = [x / 255 for x in color]
        self.custom_color = color

    def unset_color(self):
        self.custom_color = [0, 1, 0]

    # Helpers
    @property
    def repeat_delay(self):
         if hasattr(self, 'config') and\
                 'repeat_delay' in self.config['properties']:
             return self.config['properties']['repeat_delay']
         else:
             return 0

    # Actions handling
    def add_action(self, action_name, **arguments):
        self.actions.append(Action(action_name, self, **arguments))

    def list_actions(self, last_action_finished=False):
        not_running = (not self.is_loaded_running())
        current_action_seen = False
        action_descriptions = []
        for action in self.actions:
            if not_running:
                state = "inactive"
            elif last_action_finished:
                state = "done"
            elif current_action_seen:
                state = "pending"
            elif action == self.current_action:
                current_action_seen = True
                state = "current"
            else:
                state = "done"
            action_descriptions.append([action.description(), state])
        self.parent.parent.ids['ActionList'].update_list(
                self,
                action_descriptions)
