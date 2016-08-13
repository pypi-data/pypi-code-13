"""
Do competitive benchmarks against other backup software
"""

import functools
import os
import subprocess

import pytest

from .archiver import changedir

ROUNDS = 3
FILES = 500


def cmd(args, env=None):
    rc = subprocess.check_output(args, shell=True, env=env)
    os.sync()  # make sure everything is on-disk and noone is cheating
    return rc


def clearcache(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        os.sync()  # make sure all is on disk
        # Linux specific: forget all (disk/fs) caches
        cmd("sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'")
        return f(*args, **kwargs)
    return wrapper


@pytest.yield_fixture(scope='session')
def testdata(request, tmpdir_factory):
    count, size = FILES, 1000*1000
    p = tmpdir_factory.mktemp('data')
    # do not use a binary zero (\0) to avoid sparse detection
    compressible = b'x' * size
    for i in range(count):
        # use new random for each file to avoid dedup here
        uncompressible = os.urandom(size)
        with open(str(p.join(str(i))), "wb") as f:
            data = compressible if i % 2 else uncompressible
            f.write(data)
    yield str(p)
    p.remove(rec=1)


@pytest.yield_fixture
def borg_env(request, tmpdir):
    repo = str(tmpdir.join('repository'))
    env = dict(
        BORG_REPOSITORY=repo,
        BORG_PASSPHRASE='123456',
        BORG_CHECK_I_KNOW_WHAT_I_AM_DOING='YES',
        BORG_DELETE_I_KNOW_WHAT_I_AM_DOING='YES',
        BORG_UNKNOWN_UNENCRYPTED_REPO_ACCESS_IS_OK='yes',
        BORG_KEYS_DIR=str(tmpdir.join('keys')),
        BORG_CACHE_DIR=str(tmpdir.join('cache')),
    )
    env.update(os.environ)
    cmd('borg init --encryption none $BORG_REPOSITORY', env=env)
    yield env
    tmpdir.remove(rec=1)


@pytest.yield_fixture
def borg_archive(request, borg_env, testdata):
    archive = '$BORG_REPOSITORY::test'
    cmd('borg create --compression none %s %s' % (archive, testdata), env=borg_env)
    yield archive
    cmd('borg delete %s' % archive, env=borg_env)


def test_borg_create_none(benchmark, borg_env, testdata):
    i = 0

    @clearcache
    def setup():
        nonlocal i
        archive = "archive_%d" % i
        i += 1
        return ('borg create $BORG_REPOSITORY::%s %s' % (archive, testdata), ), dict(env=borg_env)

    out = benchmark.pedantic(cmd, setup=setup, rounds=ROUNDS)


def test_borg_extract(benchmark, borg_env, borg_archive, tmpdir):
    i = 0

    @clearcache
    def setup():
        nonlocal i
        extract_dir = tmpdir.mkdir("borg_extract_%d" % i)
        i += 1
        return ('cd %s ; borg extract %s' % (extract_dir, borg_archive), ), dict(env=borg_env)

    out = benchmark.pedantic(cmd, setup=setup, rounds=ROUNDS)


@pytest.yield_fixture
def obnam_env(request, tmpdir):
    repo = str(tmpdir.join('repository'))
    env = dict(
        OBNAM_REPOSITORY=repo,
    )
    env.update(os.environ)
    yield env
    tmpdir.remove(rec=1)


@pytest.yield_fixture
def obnam_archive(request, obnam_env, testdata):
    cmd('obnam backup -r $OBNAM_REPOSITORY %s' % testdata, env=obnam_env)
    yield None
    ...


def test_obnam_create_none(benchmark, obnam_env, testdata):
    @clearcache
    def setup():
        return ('obnam backup -r $OBNAM_REPOSITORY --lru-size=1024 --upload-queue-size=512 %s' % testdata, ), \
               dict(env=obnam_env)

    out = benchmark.pedantic(cmd, setup=setup, rounds=ROUNDS)


def test_obnam_extract(benchmark, obnam_env, obnam_archive, tmpdir):
    i = 0

    @clearcache
    def setup():
        nonlocal i
        extract_dir = tmpdir.mkdir("obnam_extract_%d" % i)
        i += 1
        return ('obnam restore -r $OBNAM_REPOSITORY --to %s' % extract_dir, ), dict(env=obnam_env)

    benchmark.pedantic(cmd, setup=setup, rounds=ROUNDS)
