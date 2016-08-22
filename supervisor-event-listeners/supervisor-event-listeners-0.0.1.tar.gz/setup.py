from setuptools import setup

setup(
    name="supervisor-event-listeners",
    version="0.0.1",
    packages=["supervisor_event_listeners"],
    install_requires=["supervisor", "watchdog"],
    tests_require=["mock"],
    test_suite="test",
    entry_points="""\
    [console_scripts]
    fseventwatcher = supervisor_event_listeners.fseventwatcher:main
    processrestarter = supervisor_event_listeners.processrestarter:main
    eventexec = supervisor_event_listeners.eventexec:main
    """
)
