# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4 ft=python fenc=UTF-8 ai
# tests/test_pcrunner.py

from pcrunner.main import Check
from pcrunner.main import parse_pcrunner_args


class Test_Check(object):
    def setup_class(self):
        self.check = Check(
            'PROCESS_SERVICE_CHECK_RESULT',
            'dummy check',
            '/usr/local/bin/check_dummy 0 -s 3',
            'localhost',
        )

    def test_Check_attributes(self):
        assert self.check.result_type == 'PROCESS_SERVICE_CHECK_RESULT'
        assert self.check.name == 'dummy check'
        assert self.check.command == '/usr/local/bin/check_dummy 0 -s 3'
        assert self.check.hostname == 'localhost'
        assert self.check.pid is None
        assert self.check.process is None
        assert self.check.returncode == 3
        assert self.check.terminated is False
        assert self.check.stdout == ''
        assert self.check.stderr == ''
        assert self.check.performance_data == ''
        assert self.check.starttime == 0
        assert self.check.endtime == 0


def test_parse_pcrunners_args_short():
    '''
    Test the short command-line arguments to pcrunner.
    '''
    args = parse_pcrunner_args(
        [
            '-c', '/etc/config.yml',
            '-n', 'http://nagios.example.com:5668/queue',
            '-u', 'john',
            '-p', 'secret03',
            '-o', '/etc/commandfile.yml',
            '-H', 'server.example.com',
            '-i', '300',
            '-m', '4',
            '-e', '500',
            '-r', '/var/spool/pcrunner.res',
            '-d', '/var/spool/pcrunner/resultstuf',
            '-f', '/var/run/pidfile.pid',
            '-t', '5',
            '-s', '442',
            '-l', '/var/log/logfile.log',
            '-v',
            'stop',
        ]
    )
    assert vars(args) == {
        'config_file': '/etc/config.yml',
        'nsca_web_url': 'http://nagios.example.com:5668/queue',
        'nsca_web_username': 'john',
        'nsca_web_password': 'secret03',
        'command_file': '/etc/commandfile.yml',
        'hostname': 'server.example.com',
        'interval': 300,
        'max_procs': 4,
        'lines_per_post': 500,
        'result_file': '/var/spool/pcrunner.res',
        'result_dir': '/var/spool/pcrunner/resultstuf',
        'pid_file': '/var/run/pidfile.pid',
        'http_timeout': 5,
        'max_line_size': 442,
        'log_file': '/var/log/logfile.log',
        'verbose': True,
        'daemon': 'stop',
        'version': False,
    }

    '''
    Test the long command-line arguments to pcrunner.
    '''
    args = parse_pcrunner_args(
        [
            '--config-file', '/etc/config.yml',
            '--nsca_web_url', 'http://nagios.example.com:5668/queue',
            '--nsca-web-username', 'john',
            '--nsca-web-password', 'secret03',
            '--command-file', '/etc/commandfile.yml',
            '--hostname', 'server.example.com',
            '--interval', '300',
            '--max-procs', '4',
            '--lines-per-post', '500',
            '--result-file', '/var/spool/pcrunner.res',
            '--result-dir', '/var/spool/pcrunner/resultstuf',
            '--pid-file', '/var/run/pidfile.pid',
            '--http-timeout', '5',
            '--max-line-size', '442',
            '--log-file', '/var/log/logfile.log',
            '--verbose',
            'start',
        ]
    )
    assert vars(args) == {
        'config_file': '/etc/config.yml',
        'nsca_web_url': 'http://nagios.example.com:5668/queue',
        'nsca_web_username': 'john',
        'nsca_web_password': 'secret03',
        'command_file': '/etc/commandfile.yml',
        'hostname': 'server.example.com',
        'interval': 300,
        'max_procs': 4,
        'lines_per_post': 500,
        'result_file': '/var/spool/pcrunner.res',
        'result_dir': '/var/spool/pcrunner/resultstuf',
        'pid_file': '/var/run/pidfile.pid',
        'http_timeout': 5,
        'max_line_size': 442,
        'log_file': '/var/log/logfile.log',
        'verbose': True,
        'daemon': 'start',
        'version': False,
    }


def test_parse_pcrunners_args_empty():
    '''
    Test the long command-line arguments to pcrunner.
    '''
    args = parse_pcrunner_args([])
    assert vars(args) == {
        'command_file': None,
        'config_file': None,
        'daemon': None,
        'hostname': None,
        'http_timeout': None,
        'interval': None,
        'lines_per_post': None,
        'log_file': None,
        'max_line_size': None,
        'max_procs': None,
        'nsca_web_password': None,
        'nsca_web_url': None,
        'nsca_web_username': None,
        'pid_file': None,
        'result_dir': None,
        'result_file': None,
        'verbose': False,
        'version': False,
    }
