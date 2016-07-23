import warnings

from notifier_pushbullet import PushBullet_


def read_job(job):
    extensions = {'timeline': '.tml',
                  'threads': '.trd'}
    if job in set(extensions):
        return job, extensions[job]
    else:
        raise LookupError('Job not found. Options: timeline threads.')


def read_notifier(notifier_type, credential_fp=None):
    notifier_types = ['pushbullet']
    if notifier_type.lower() not in set(notifier_types):
        raise LookupError('Notifier type not found. Options: pushbullet.')

    if notifier_type.lower() == 'pushbullet':
        with open(credential_fp, 'r') as i:
            access_token = next(i).strip()
        return PushBullet_(access_token)


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
