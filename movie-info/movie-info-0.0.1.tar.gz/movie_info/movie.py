import omdb
import optparse

def get_parsed_args():
    parser = optparse.OptionParser()
    parser.add_option('-m', '--movie_name', action='store_true', default=False, dest='clean')
    parser.add_option('-v', '--verbose', action='store_true', default=False, dest='verbose',
                      help='Print out stacktraces for errors in checks')

    try:
        options, args = parser.parse_args()
    except SystemExit:
        options, args = optparse.Values({'movie_name': False}), []
    return options, args

def get_movie_info(movie_name):
    omdb.set_default('tomatoes', True)
    movie_obj = omdb.title(movie_name)
    for category,info in movie_obj.iteritems():
        print "{0}{1}{2}".format(category.upper(),' : ',info)

def main():
    options, args = get_parsed_args()
    movie_name = None
    if len(args) == 0:
        print('Please specify the movie name')
        return
    elif args:
        movie_name = args[0]

    get_movie_info(movie_name)

if __name__ == '__main__':
    main()
