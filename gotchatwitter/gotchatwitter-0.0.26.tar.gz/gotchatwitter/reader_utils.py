import warnings
import csv


def read_job(job):
    extensions = {'timeline': '.tml',
                  'threads': '.trd'}
    if job in set(extensions):
        return job, extensions[job]
    else:
        raise LookupError('Job not found. Options: timeline threads.')


def read_notifier(notifier_type, credential_fp=None):

    if not notifier_type:
        from notifier_print import Print_
        return Print_()

    notifier_types = ['pushbullet']
    if notifier_type.lower() not in set(notifier_types):
        raise LookupError('Notifier type not found. Options: pushbullet.')

    if notifier_type.lower() == 'pushbullet':
        from notifier_pushbullet import PushBullet_
        with open(credential_fp, 'r') as i:
            access_token = next(i).strip()
        return PushBullet_(access_token)


def read_input(inputs, input_column=0, input_delimiter=',', input_start_from=None, **kwargs):
    # return input_fp, input_list
    input_fp = ''

    if isinstance(inputs, list):
        input_fp = '_'

    if isinstance(inputs, str):
        input_fp = inputs
        with open(input_fp, 'r') as i:
            csvreader = csv.reader(i, delimiter=input_delimiter)
            if isinstance(input_column, int):
                inputs = [line[input_column] for line in csvreader if line]
            if isinstance(input_column, dict):
                inputs = [line[input_column.get('tid', 1)] + '@' +
                          line[input_column.get('uid', input_column.get('screen_name', 0))]
                          for line in csvreader if line]

    if input_start_from:
        try:
            start_index = inputs.index(input_start_from)
        except:
            warnings.warn('Start from value %s is not found.' % input_start_from, Warning)
            start_index = 0
    else:
        start_index = 0
    return input_fp, inputs[start_index:]


def read_header(job, **kwargs):
    readers = {'timeline': _read_header_timeline(**kwargs)}
    return readers[job]


def _read_header_timeline(**kwargs):
    default = ['status', 'uid', 'screen_name', 'tid', 'timestamp', 'text', 'media',
               'language', 'n_retweets', 'n_likes',
               'location_id', 'location_name']
    header = kwargs.get('output_header', default)
    other_ = set(header) - set(default)
    if other_:
        warnings.warn('header %s not found' % other_)
    return header
