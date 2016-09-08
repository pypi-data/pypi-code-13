from zope.component import getGlobalSiteManager
from zope.component import getUtility
from zope.interface import implements

from interfaces import IFWUtils

from docker import Client
from docker.utils import kwargs_from_env

gsm = getGlobalSiteManager()

class Config(object):
    implements(IFWUtils)
    def __setitem__(self, key, val):
        self._data[key] = val
    def __getitem__(self, key):
        return self._data[key]
    def __call__(self, filename):
        super(Config, self).__init__()
        self._data = {}
        self.config = ConfigParser.ConfigParser()
        self.config.read(filename)
        for section in self.config.sections():
            self._data[section] = {}
            for option in self.config.options(section):
                self._data[section][option] = \
                    self.config.get(section, option)
        self['paths']['HERE'] = HERE
        return self._data
config = Config()
gsm.registerUtility(config, IFWUtils, 'config')

#class SetMainEnv(object):
#    implements(IFWUtils)
#    def __call__(self):
#        config_file_path = getUtility(IFWUtils, 'get_config_path')()
#        config = getUtility(IFWUtils, 'config')(config_file_path)
#        docker_environ = config.get('docker_environ')
#        #os.environ.update(docker_environ)  
#set_main_env = SetMainEnv()
#gsm.registerUtility(set_main_env, IFWUtils, 'set_main_env')

class DockerClient(object):
    implements(IFWUtils)
    def __init__(self):
        #getUtility(IFWUtils, 'set_main_env')()
        self.client = Client(**kwargs_from_env(assert_hostname=False))
    def __call__(self):
        return self.client
docker_client = DockerClient()
gsm.registerUtility(docker_client, IFWUtils, 'docker_client')

class GetAllContainers(object):
    def __call__(self):
        cli = \
            getUtility(IFWUtils, 'docker_client')()
        return cli.containers(all=True)
get_all_containers = GetAllContainers()
gsm.registerUtility(get_all_containers, IFWUtils, 'get_all_containers')

class ContainersByName(object):
    def __call__(self):
        cli = \
            getUtility(IFWUtils, 'docker_client')()
        get_all_containers = \
            getUtility(IFWUtils, 'get_all_containers')
        data = {}
        for c in get_all_containers():
            data[c.get('Names')[0][1:]] = c
        return data
containers_by_name = ContainersByName()
gsm.registerUtility(containers_by_name, IFWUtils, 'containers_by_name')

class GetContainerNames(object):
    def __call__(self):    
        containers_by_name = \
            getUtility(IFWUtils, 'containers_by_name')
        return containers_by_name().keys()
get_container_names = ContainersByName()
gsm.registerUtility(get_container_names, IFWUtils, 'get_container_names')

class GetContainerIdByName(object):
    def __call__(self, name):
        cli = \
            getUtility(IFWUtils, 'docker_client')()
        containers_by_name = \
            getUtility(IFWUtils, 'get_container_names')
        return containers_by_name()[name].get('Id')
get_container_id_by_name = GetContainerIdByName()
gsm.registerUtility(get_container_id_by_name, IFWUtils, \
        'get_container_id_by_name')

class RemoveContainerByName(object):
    def __call__(self, name):
        cli = \
            getUtility(IFWUtils, 'docker_client')()
        get_container_id_by_name = \
            getUtility(IFWUtils, 'get_container_id_by_name')
        container_id = get_container_id_by_name(name)
        cli.stop(container=container_id)
        cli.remove_container(container=container_id, v=True)
remove_container_by_name = RemoveContainerByName()
gsm.registerUtility(remove_container_by_name, IFWUtils, \
        'remove_container_by_name')

class TearDownContainers(object):
    def __call__(self, reset=False):
        cli = \
            getUtility(IFWUtils, 'docker_client')()
        get_container_names = \
            getUtility(IFWUtils, 'get_container_names')
        remove_container_by_name = \
            getUtility(IFWUtils, 'remove_container_by_name')
        for name in get_container_names():
            print "TEARING DOWN",name
            if reset:
                remove_container_by_name(name)
            else:
                if not name in getUtility(IFWUtils, 'data_containers')().keys():
                    remove_container_by_name(name)
tear_down_containers = TearDownContainers()
gsm.registerUtility(tear_down_containers, IFWUtils, 'tear_down_containers')
