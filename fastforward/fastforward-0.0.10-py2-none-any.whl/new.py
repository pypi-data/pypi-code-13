def output(args):
    print 'output %s' % args.remove

def make(parser):
    subparser = parser.add_subparsers(
        title='commands',
        metavar='COMMAND',
        help='description',
        )
    install_parser = subparser.add_parser(
        'install',
        help='install glance(default store: ceph)')
    install_parser.add_argument(
        '--remove',
        help='remove test',
        action='store',
        dest='remove'
    )
    install_parser.set_defaults(func=output)
