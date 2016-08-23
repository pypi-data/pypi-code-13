from credentials import get_nova_creds
from novaclient.client import Client

credentials = get_nova_creds()
nova_client = Client(**credentials)
vms = nova_client.servers.list()

for vm in vms:
        if vm.status in 'ERROR':
                vm.reset_state()
