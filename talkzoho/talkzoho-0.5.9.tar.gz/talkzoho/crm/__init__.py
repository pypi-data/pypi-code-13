ENVIRON_AUTH_TOKEN  = 'ZOHO_CRM_AUTH_TOKEN'
BASE_URL            = "https://crm.zoho."
API_PATH            = "/crm/private/json"
SCOPE               = 'crmapi'
MAX_PAGE_SIZE       = 200
REQUESTS_PER_SECOND = None

from .contacts.get_contact import get_contact  # noqa
from .accounts.get_account import get_account  # noqa
from .potentials.get_protential import get_potential  # noqa
from .leads.get_lead import get_lead  # noqa
from .get_module import get_module  # noqa

from .contacts.filter_contacts import filter_contacts  # noqa
from .accounts.filter_accounts import filter_accounts  # noqa
from .potentials.filter_potentials import filter_potentials  # noqa
from .leads.filter_leads import filter_leads  # noqa
from .filter_module import filter_module  # noqa
