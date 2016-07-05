from __future__ import unicode_literals, division, absolute_import

from argparse import ArgumentParser, ArgumentTypeError

from sqlalchemy.orm.exc import NoResultFound

from flexget import options
from flexget.event import event
from flexget.logger import console
from flexget.manager import Session
from flexget.plugins.list.entry_list import get_entry_lists, get_list_by_exact_name, get_entries_by_list_id, \
    get_entry_by_id, get_entry_by_title, EntryListList, EntryListEntry


def attribute_type(attribute):
    if attribute.count('=') != 1:
        raise ArgumentTypeError('Received attribute in wrong format: %s, '
                                'should be in keyword format like `imdb_id=tt1234567`' % attribute)
    name, value = attribute.split('=', 2)
    return {name: value}


def do_cli(manager, options):
    """Handle entry-list subcommand"""
    if options.list_action == 'all':
        entry_list_lists()
        return

    if options.list_action == 'list':
        entry_list_list(options)
        return

    if options.list_action == 'show':
        entry_list_show(options)
        return

    if options.list_action == 'add':
        entry_list_add(options)
        return

    if options.list_action == 'del':
        entry_list_del(options)
        return

    if options.list_action == 'purge':
        entry_list_purge(options)
        return


def entry_list_lists():
    """ Show all entry lists """
    with Session() as session:
        lists = get_entry_lists(session=session)
        console('Existing entry lists:')
        console('-' * 20)
        for entry_list in lists:
            console(entry_list.name)


def entry_list_list(options):
    """List entry list"""
    with Session() as session:
        try:
            entry_list = get_list_by_exact_name(options.list_name, session=session)
        except NoResultFound:
            console('Could not find entry list with name {}'.format(options.list_name))
            return
        console('Entries for list `{}`:'.format(options.list_name))
        console('-' * 79)
        for entry in get_entries_by_list_id(entry_list.id, order_by='added', descending=True, session=session):
            console('{:2d}: {}, {} fields'.format(entry.id, entry.title, len(entry.entry)))


def entry_list_show(options):
    with Session() as session:
        try:
            entry_list = get_list_by_exact_name(options.list_name, session=session)
        except NoResultFound:
            console('Could not find entry list with name {}'.format(options.list_name))
            return

        try:
            entry = get_entry_by_id(entry_list.id, int(options.entry), session=session)
        except NoResultFound:
            console(
                'Could not find matching entry with ID {} in list `{}`'.format(int(options.entry), options.list_name))
            return
        except ValueError:
            entry = get_entry_by_title(entry_list.id, options.entry, session=session)
            if not entry:
                console(
                    'Could not find matching entry with title `{}` in list `{}`'.format(options.entry,
                                                                                        options.list_name))
                return

        console('Showing fields for entry ID {}'.format(options.list_name))
        console('-' * 79)
        for k, v in sorted(entry.entry.items()):
            console('{}: {}'.format(k.upper(), v))


def entry_list_add(options):
    with Session() as session:
        try:
            entry_list = get_list_by_exact_name(options.list_name, session=session)
        except NoResultFound:
            console('Could not find entry list with name `{}`, creating'.format(options.list_name))
            entry_list = EntryListList(name=options.list_name)
            session.add(entry_list)
        session.merge(entry_list)
        session.commit()
        title = options.entry_title
        entry = {'title': options.entry_title, 'original_url': options.original_url}
        db_entry = get_entry_by_title(list_id=entry_list.id, title=title, session=session)
        if db_entry:
            console("Entry with the title `{}` already exist with list `{}`. Will replace identifiers if given".format(
                title, entry_list.name))
            output = 'Successfully updated entry `{}` to entry list `{}` '.format(title, entry_list.name)
        else:
            console("Adding entry with title `{}` to list `{}`".format(title, entry_list.name))
            db_entry = EntryListEntry(entry=entry, entry_list_id=entry_list.id)
            session.add(db_entry)
            output = 'Successfully added entry `{}` to entry list `{}` '.format(title, entry_list.name)
        if options.attributes:
            console('Adding attributes to entry `{}`'.format(title))
            for identifier in options.attributes:
                for k, v in identifier.items():
                    entry[k] = v
            db_entry.entry = entry
        console(output)


def entry_list_del(options):
    with Session() as session:
        try:
            entry_list = get_list_by_exact_name(options.list_name)
        except NoResultFound:
            console('Could not find entry list with name `{}`'.format(options.list_name))
            return
        try:
            db_entry = get_entry_by_id(entry_list.id, int(options.entry), session=session)
        except NoResultFound:
            console(
                'Could not find matching entry with ID {} in list `{}`'.format(int(options.entry), options.list_name))
            return
        except ValueError:
            db_entry = get_entry_by_title(entry_list.id, options.entry, session=session)
            if not db_entry:
                console(
                    'Could not find matching entry with title `{}` in list `{}`'.format(options.entry,
                                                                                        options.list_name))
                return
        console('Removing entry `%s` from list %s' % (db_entry.title, options.list_name))
        session.delete(db_entry)


def entry_list_purge(options):
    with Session() as session:
        try:
            entry_list = get_list_by_exact_name(options.list_name)
        except NoResultFound:
            console('Could not find entry list with name `{}`'.format(options.list_name))
            return
        console('Deleting list %s' % options.list_name)
        session.delete(entry_list)


@event('options.register')
def register_parser_arguments():
    # Common option to be used in multiple subparsers
    entry_parser = ArgumentParser(add_help=False)
    entry_parser.add_argument('entry_title', help="Title of the entry")
    entry_parser.add_argument('original_url', help="URL of the entry")

    global_entry_parser = ArgumentParser(add_help=False)
    global_entry_parser.add_argument('entry', help='Can be entry title or ID')

    attributes_parser = ArgumentParser(add_help=False)
    attributes_parser.add_argument('--attributes', metavar='<attributes>', nargs='+', type=attribute_type,
                                   help='Can be a string or a list of string with the format imdb_id=XXX,'
                                        ' tmdb_id=XXX, etc')
    list_name_parser = ArgumentParser(add_help=False)
    list_name_parser.add_argument('list_name', nargs='?', default='entries', help='Name of entry list to operate on')
    # Register subcommand
    parser = options.register_command('entry-list', do_cli, help='view and manage entry lists')
    # Set up our subparsers
    subparsers = parser.add_subparsers(title='actions', metavar='<action>', dest='list_action')
    subparsers.add_parser('all', help='Shows all existing entry lists')
    subparsers.add_parser('list', parents=[list_name_parser], help='List entries from a list')
    subparsers.add_parser('show', parents=[list_name_parser, global_entry_parser],
                          help='Show entry fields.')
    subparsers.add_parser('add', parents=[list_name_parser, entry_parser, attributes_parser],
                          help='Add an entry to a list')
    subparsers.add_parser('del', parents=[list_name_parser, global_entry_parser],
                          help='Remove an entry from a list using its title or ID')
    subparsers.add_parser('purge', parents=[list_name_parser],
                          help='Removes an entire list with all of its entries. Use this with caution')
