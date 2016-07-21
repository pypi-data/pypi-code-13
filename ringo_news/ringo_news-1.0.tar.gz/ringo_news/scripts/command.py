#!/usr/bin/env python
# encoding: utf-8
import os
import argparse
import transaction
from ringo.model.user import User
from ringo.scripts.db import (
    do_import,
    get_importer,
    get_session
)
from ringo_news.model import News


def add_news_parser(subparsers, parent):
    p = subparsers.add_parser('news',
                              help='Management of the news extension',
                              parents=[parent])
    sp = p.add_subparsers(help='News command help')
    add_parser = sp.add_parser('add',
                               help=('Adds or Updates news items.'),
                               parents=[parent])
    add_parser.add_argument('jsonfile', help="JSON file with news")
    add_parser.add_argument('--loadbyid',
                            action="store_true",
                            help="Load news by id and not by uuid")
    add_parser.set_defaults(func=handle_add_command)
    del_parser = sp.add_parser('del',
                               help=('Deletes a given news items.'),
                               parents=[parent])
    del_parser.add_argument('id', help="ID of the news item to be deleted")
    del_parser.set_defaults(func=handle_del_command)


def handle_add_command(args):
    path = []
    path.append(args.config)
    session = get_session(os.path.join(*path))
    importer = get_importer(session, 'news', 'json')
    # On default all users will see new added items.
    users = session.query(User).all()
    with open(args.jsonfile) as f:
        data = f.read()
        items, created, updated = do_import(session, importer, data,
                                            use_uuid=(not args.loadbyid))
        for item, action in items:
            # Add all new items to the session
            if action.find("CREATE") > -1:
                item.users = users

    try:
        transaction.commit()
        print "Updated %s news, Created %s news" % (updated, created)
    except Exception as e:
        print str(e)
        print "Loading data failed!"


def handle_del_command(args):
    path = []
    path.append(args.config)
    session = get_session(os.path.join(*path))
    try:
        item = session.query(News).filter(News.id == args.id).one()
        session.delete(item)
        transaction.commit()
        print "Succesfully deleted"
    except Exception as e:
        print str(e)
        print "Can not delete!"
