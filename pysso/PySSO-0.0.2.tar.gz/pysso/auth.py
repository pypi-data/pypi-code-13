import time
import hashlib


def sign( method, uri, args, sign_key, time_stamp = None ):
    '''
    Use key to sign the request.
    Will return a new dictionary which contain all the k-v pair of old args and 'time' and 'sign'  
    '''
    if time_stamp == None:
        time_stamp = str(int(time.time()))

    args = args.copy()
    args['time'] = time_stamp
    args_keys = list(args.keys())
    args_keys.sort()

    args_str = ''
    for key in args_keys:
        if len(args_str) != 0:
            args_str += '&'

        args_str += key + '=' + str(args[key])

    str_to_sign = method + uri + '?' + args_str + sign_key
    #print('str_to_sign:',str_to_sign)

    m = hashlib.md5()
    m.update(str_to_sign.encode('utf-8'))

    #print('md5:%s'%m.hexdigest())
    args['sign'] = m.hexdigest()
    return args


def verify( method, uri, args, sign_key, allow_time_range=60 ):
    args = args.copy()
    
    request_sign = args.get('sign')
    request_time = args.get('time')
    if sign == None or request_time == None:
        return False

    if abs( float(request_time) - time.time()) > allow_time_range:
        print('request time was error.')
        return False

    del args['sign']
    del args['time']

    args_after_sign = sign( method, uri, args, sign_key, request_time )
    if args_after_sign['sign'] != request_sign:
        print( 'sign error.%s != %s'%(request_sign, args_after_sign['sign']) )
        return False

    return True
