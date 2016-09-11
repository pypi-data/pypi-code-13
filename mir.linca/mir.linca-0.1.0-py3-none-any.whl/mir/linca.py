import argparse
import asyncio
from concurrent.futures import CancelledError
import logging
import os
import signal

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level='INFO')
    args = parse_args()
    os.makedirs(args.dest_dir, exist_ok=True)

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, cancel_all_tasks)
    try:
        loop.run_until_complete(watch_and_link(args.watch_dir, args.dest_dir))
    except CancelledError:
        pass
    finally:
        loop.close()


def cancel_all_tasks():
    tasks = asyncio.Task.all_tasks()
    for task in tasks:
        task.cancel()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('watch_dir', type=os.path.normpath)
    parser.add_argument('dest_dir', type=os.path.normpath)
    return parser.parse_args()


async def watch_and_link(watch_dir, dest_dir):
    logger.info('linca %s %s', watch_dir, dest_dir)
    proc = await asyncio.create_subprocess_exec(
        'inotifywait', '-m', '--format', '%e//%f', watch_dir,
        stdout=asyncio.subprocess.PIPE,
    )
    async for line in proc.stdout:
        line = line[:-1]  # remove newline
        logger.debug('Got %r', line)
        notify_event = NotifyEvent.from_output(watch_dir, line)
        logger.debug('Got %r', notify_event)
        await process_event(notify_event, dest_dir)


async def process_event(notify_event, dest_dir):
    if (notify_event.events & {'create', 'moved_to'} and
        notify_event.file != '' and
        'delete' not in notify_event.events):
        src = os.path.join(notify_event.watched_file, notify_event.file)
        dst = os.path.join(dest_dir, notify_event.file)
        await smart_link(src, dst)


async def smart_link(src, dst):
    logger.info('Linking %s %s', src, dst)
    if os.path.isdir(src):
        proc = await asyncio.create_subprocess_exec(
            'cp', '-alT', src, dst,
        )
        await proc.wait()
    elif os.path.isfile(src):
        os.link(src, dst)
    else:
        logger.error('Unknown type %s', src)


class NotifyEvent:

    def __init__(self, watched_file, events, file):
        self.watched_file = watched_file
        self.events = set(events)
        self.file = file

    @classmethod
    def from_output(cls, watched_file, output_line):
        assert isinstance(output_line, bytes)
        output_line = output_line.decode()
        events, file = output_line.split('//')
        return cls(
            watched_file,
            (event.lower() for event in events.split(',')),
            file,
        )

    def __repr__(self):
        return 'NotifyEvent({})'.format(', '.join(
            repr(x)
            for x in (self.watched_file, self.events, self.file)
        ))

if __name__ == '__main__':
    main()
