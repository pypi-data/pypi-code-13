import unittest
from supervisor_event_listeners.fseventwatcher import PollableFileSystemEventHandler, FSEventWatcher


class TestPollableFileSystemEventHandler(unittest.TestCase):
    def test_mark_unmark_activity_occurred(self):
        event_handler = PollableFileSystemEventHandler(True, True, True, True)
        prev = event_handler.mark_activity_occurred()
        self.assertEqual(prev, False)
        prev = event_handler.mark_activity_occurred()
        self.assertEqual(prev, True)

    def test_unmark_activity_occurred(self):
        event_handler = PollableFileSystemEventHandler(True, True, True, True)
        prev = event_handler.unmark_activity_occurred()
        self.assertEqual(prev, False)
        prev = event_handler.mark_activity_occurred()
        prev = event_handler.unmark_activity_occurred()
        self.assertEqual(prev, True)

    def test_on_moved(self):
        event_handler = PollableFileSystemEventHandler(True, False, False, False)
        event_handler.on_moved(None)
        self.assertEqual(event_handler.unmark_activity_occurred(), True)
        event_handler = PollableFileSystemEventHandler(False, False, False, False)
        event_handler.on_moved(None)
        self.assertEqual(event_handler.unmark_activity_occurred(), False)

    def test_on_created(self):
        event_handler = PollableFileSystemEventHandler(False, True, False, False)
        event_handler.on_created(None)
        self.assertEqual(event_handler.unmark_activity_occurred(), True)
        event_handler = PollableFileSystemEventHandler(False, False, False, False)
        event_handler.on_created(None)
        self.assertEqual(event_handler.unmark_activity_occurred(), False)

    def test_on_deleted(self):
        event_handler = PollableFileSystemEventHandler(False, False, True, False)
        event_handler.on_deleted(None)
        self.assertEqual(event_handler.unmark_activity_occurred(), True)
        event_handler = PollableFileSystemEventHandler(False, False, False, False)
        event_handler.on_deleted(None)
        self.assertEqual(event_handler.unmark_activity_occurred(), False)

    def test_on_modified(self):
        event_handler = PollableFileSystemEventHandler(False, False, False, True)
        event_handler.on_modified(None)
        self.assertEqual(event_handler.unmark_activity_occurred(), True)
        event_handler = PollableFileSystemEventHandler(False, False, False, False)
        event_handler.on_modified(None)
        self.assertEqual(event_handler.unmark_activity_occurred(), False)
