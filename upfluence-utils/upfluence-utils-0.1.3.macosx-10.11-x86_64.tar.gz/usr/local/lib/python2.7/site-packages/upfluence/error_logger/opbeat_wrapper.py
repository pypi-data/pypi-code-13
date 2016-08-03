import socket
import opbeat.base


class Client(object):
    def __init__(self, organization_id, app_id, secret_token, hostname=None,
                 extra={}):
        self.extra = extra
        self.base_service = None
        self._client = opbeat.base.Client(
            organization_id=organization_id, app_id=app_id,
            secret_token=secret_token,
            hostname=hostname or socket.gethostname())

    def _build_base_extra(self):
        extras = {}
        versions = self.base_service.getInterfaceVersion()
        versions.update({
            self.base_service.getName(): self.base_service.getVersion()})

        for name, version in versions.iteritems():
            if version.git_version:
                gitver = version.git_version
                extras.update(
                    {'{}_git_version'.format(name): '{}/commit/{}'.format(
                        gitver.remote, gitver.commit)})
            if version.semantic_version:
                semver = version.semantic_version
                extras.update(
                    {'{}_semantic_version'.format(name): '{}.{}.{}'.format(
                        semver.major, semver.minor, semver.patch)})

        return extras

    def capture_exception(self, *args, **kwargs):
        kwargs['extra'] = dict(kwargs.get('extra', {}), **self.extra)
        self._client.capture_exception(*args, **kwargs)
