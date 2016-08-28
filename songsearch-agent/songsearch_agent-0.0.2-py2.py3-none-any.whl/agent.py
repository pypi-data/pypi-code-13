import random
import time

import requests


class InvalidAPIKeyError(Exception):
    """when the api key is wrong"""


class SubmitError(Exception):
    """when we can't submit the result"""


ops_exceptions = ()  # XXX timeout errors, misc sporadic ssl errors


_UAS = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 '
    '(KHTML, like Gecko) Version/9.1.2 Safari/601.7.7',

    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.1) '
    'Gecko/20100101 Firefox/46.1',

    'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601'
    '.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G34 Safari/601.2',

    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 '
    'Firefox/47.1',

    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.1) Gecko/20100101 '
    'Firefox/50.1',
)

def realistic_request(url, verify=True):
    headers = {
        'Accept': (
            'text/html,application/xhtml+xml,application/xml,text/xml'
            ';q=0.9,*/*;q=0.8'
        ),
        'User-Agent': random.choice(_UAS),
        'Accept-Language': 'en-US,en;q=0.5',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    return requests.get(url, headers=headers, verify=verify)


class Runner:

    def __init__(
        self,
        api_key,
        domain,
        use_http=False,
        verbose=False,
        gently=False,
    ):
        self.api_key = api_key
        self.domain = domain
        self.use_http = use_http
        self.verbose = verbose
        self.gently = gently

    def get_url(self, path):
        url = self.use_http and 'http://' or 'https://'
        url += self.domain
        url += path
        return url

    def repeat(self):
        while True:
            try:
                fetch_url = self.get_url('/api/downloader/next/')
                if self.verbose:
                    print('Fetching next URL from ', fetch_url)

                next_url_response = requests.get(fetch_url, headers={
                    'API-Key': self.api_key
                })
                if next_url_response.status_code == 403:
                    raise InvalidAPIKeyError(self.api_key)
                elif next_url_response.status_code == 429:
                    if self.verbose:
                        print("Taking a biiig pause til there's more to do")
                    time.sleep(60)
                    continue

                next_url = next_url_response.json()['url']
                if self.verbose:
                    print('Next URL to download:', next_url)

                response = realistic_request(next_url)
                if response.status_code != 200:
                    if self.verbose:
                        print(
                            'Failed to download', next_url,
                            'Status code:', response.status_code
                        )
                html = str(response.content)

                if self.verbose:
                    print('Downloaded {} bytes'.format(
                        format(len(html), ',')
                    ))

                submit_url = self.get_url('/api/downloader/submit/')
                payload = {'url': next_url, 'html': html}
                submit_response = requests.post(
                    submit_url,
                    data=payload,
                    headers={
                        'API-Key': self.api_key
                    }
                )

                if submit_response.status_code == 403:
                    raise InvalidAPIKeyError(self.api_key)
                elif (
                    submit_response.status_code >= 400 and
                    submit_response.status_code < 500
                ):
                    raise SubmitError(submit_response.status_code)

                if self.verbose:
                    print(
                        'Response after submitting:',
                        str(next_url_response.json())
                    )
                sleep_time = random.random() * 10
                if self.gently:
                    sleep_time *= 5
                if self.verbose:
                    print('Sleeping for', round(sleep_time, 2), 'seconds')
                time.sleep(sleep_time)

                if self.verbose:
                    print('\n')

            except ops_exceptions:
                if self.verbose:
                    print('Operational error, sleeping for a bit')
                    time.sleep(10)


def run(*args, **kwargs):
    runner = Runner(*args, **kwargs)
    runner.repeat()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'api_key',
        help="package (e.g. some-package==1.2.3 or just some-package)"
    )
    parser.add_argument(
        "-v, --verbose",
        help="Verbose output",
        action="store_true",
        dest='verbose',
    )
    parser.add_argument(
        "-g, --gently",
        help='Longer delay between each loop',
        action="store_true",
        dest='gently',
    )
    parser.add_argument(
        '-d, --domain',
        help='Domain name to send to',
        action='store',
        default='songsear.ch',
        dest='domain',
    )
    parser.add_argument(
        "--http",
        help="Use http instead of https",
        action="store_true",
        # dest='',
    )

    args = parser.parse_args()
    return run(
        args.api_key,
        domain=args.domain,
        use_http=args.http,
        gently=args.gently,
        verbose=args.verbose,
    )


if __name__ == '__main__':
    sys.exit(main())
