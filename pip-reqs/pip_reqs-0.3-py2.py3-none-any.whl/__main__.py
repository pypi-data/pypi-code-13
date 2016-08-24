import os
import shutil
import contextlib
import tempfile

import click

import requests

from pip.req import parse_requirements, RequirementSet
from pip.download import is_file_url, is_dir_url, is_vcs_url
from pip.index import PackageFinder


@contextlib.contextmanager
def temporary_directory(*args, **kwargs):
    d = tempfile.mkdtemp(*args, **kwargs)
    try:
        yield d
    finally:
        if os.path.exists(d):
            shutil.rmtree(d)


def link_req_to_str(req):
    if req.editable:
        return '-e {}'.format(req.link.url)
    else:
        return req.link.url


class RequirementsParser(object):
    def __init__(self):
        self.session = requests.Session()
        self.finder = PackageFinder(
            find_links=[],
            index_urls=[],
            session=self.session,
            process_dependency_links=False,
        )

    def _get_local_deps(self, req):
        rs = RequirementSet(
            build_dir=None,
            src_dir=None,
            download_dir=None,
            session=self.session,
        )
        return rs._prepare_file(self.finder, req)

    def _process_requirement(self, req):
        ext_reqs, loc_reqs = [], []
        if req.link:
            if is_vcs_url(req.link):
                # TODO: Is this needed or even supported?
                raise NotImplementedError(
                    'Requirement `{}` is not in a supported format'
                    .format(str(req))
                )
            elif is_file_url(req.link):
                if is_dir_url(req.link):
                    loc_reqs.append(link_req_to_str(req))
                    for subreq in self._get_local_deps(req):
                        ext_sub, loc_sub = self._process_requirement(subreq)
                        ext_reqs.extend(ext_sub)
                        loc_reqs.extend(loc_sub)
                else:
                    # TODO: Is this needed or even supported?
                    raise NotImplementedError(
                        'Requirement `{}` is not in a supported format'
                        .format(str(req))
                    )
            else:
                ext_reqs.append(link_req_to_str(req))
        else:
            ext_reqs.append(str(req.req))

        return ext_reqs, loc_reqs

    def parse(self, reqs_filepath):
        ext_reqs, loc_reqs = [], []
        for raw_req in parse_requirements(reqs_filepath, session=self.session):
            ext_subreqs, loc_subreqs = self._process_requirement(raw_req)
            ext_reqs.extend(ext_subreqs)
            loc_reqs.extend(loc_subreqs)
        return ext_reqs, loc_reqs


class WheelsproxyClient(object):
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def compile(self, requirements_in):
        r = self.session.post(
            self.base_url + '+compile/',
            data=requirements_in,
        )
        r.raise_for_status()
        return r.content

    def resolve(self, compiled_reqs):
        r = self.session.post(
            self.base_url + '+resolve/',
            data=compiled_reqs,
        )
        r.raise_for_status()
        return r.content


@click.group()
@click.option('--wheelsproxy', '-w', envvar='WHEELSPROXY_URL', required=True)
@click.pass_context
def main(ctx, wheelsproxy):
    ctx.obj = WheelsproxyClient(wheelsproxy)


@main.command()
@click.pass_obj
@click.argument('infile', default='requirements.in', required=False,
                type=click.Path(exists=True))
@click.argument('outfile', default='requirements.txt', required=False,
                type=click.File('wb', lazy=True))
def compile(obj, infile, outfile):
    parser = RequirementsParser()
    ext_reqs, local_reqs = parser.parse(infile)
    compiled_reqs = obj.compile('\n'.join(ext_reqs))
    outfile.write(compiled_reqs)
    outfile.write('\n'.join([
        '',
        '# The following packages are available only locally.',
        '# Their dependencies *have* been considered while',
        '# resolving the full dependency tree:',
    ] + local_reqs))
    outfile.write('\n')


@main.command()
@click.pass_obj
@click.argument('infile', default='requirements.txt', required=False,
                type=click.File('rb'))
@click.argument('outfile', default='requirements.urls', required=False,
                type=click.File('wb', lazy=True))
def resolve(obj, infile, outfile):
    outfile.write(obj.resolve(infile.read()))


if __name__ == '__main__':
    main()
