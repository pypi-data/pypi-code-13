# -*- coding: utf-8 -*-

import os
import logging
import subprocess

import jinja2
import svdlib.core


logger = logging.getLogger(__name__)


def user_add(user):
    command = '/usr/sbin/useradd -mrs /bin/false %s' % user
    r = subprocess.call(
        command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        shell=True)

    if r != 0:
        logger.critical('user not created (exit code: {})'.format(r))
        return False

    if not change_mode('/home/{}'.format(user)):
        return False

    return True


def change_own(user, group, item, opts='-R'):
    command = '/bin/chown {} {}:{} {}'.format(opts, user, group, item)
    r = subprocess.call(
        command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        shell=True)

    if r != 0:
        print('Error: change owner is failed (exit code: {})'.format(r))
        return False
    return True


def change_mode(item, mode='0700'):
    command = '/bin/chmod {} {}'.format(mode, item)
    r = subprocess.call(
        command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        shell=True)

    if r != 0:
        print('Error: change mode is failed (exit code: {})'.format(r))
        return False
    return True


def ln(src, dst):
    if not os.path.exists(src):
        print('Error: file {} not exists'.format(src))
        return False

    try:
        os.symlink(src, dst)
        return True
    except FileExistsError:
        return True


def render_template(tpls_dir, tpl, dst, **kwargs):
    j2 = jinja2.Environment(loader=jinja2.FileSystemLoader(tpls_dir))
    string = j2.get_template(tpl).render(kwargs)

    with open(dst, 'w') as f:
        result = f.write(string + '%s' % os.linesep)

    change_mode(dst, '0600')

    if result == 0:
        return False
    return True


def start_node(node_name):
    svd = svdlib.core.Supervisor()
    for item in svd.reread():
        if item['name'] == node_name and item['status'] == 'available':
            r = svd.add(node_name)
            if not r['result']:
                print('Error:', r)
                return False
            break
        else:
            print('Error: supervisor: {} not available'.format(node_name))
            return False
    return True
