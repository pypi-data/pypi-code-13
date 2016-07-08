from botor import Botor
from botor.aws.iam import get_user_inline_policies
from botor.aws.iam import get_user_access_keys
from botor.aws.iam import get_user_login_profile
from botor.aws.iam import get_user_managed_policies
from botor.aws.iam import get_user_mfa_devices
from botor.aws.iam import get_user_signing_certificates
from bozor.aws.iam import _get_name_from_structure, modify, _conn_from_arn


def _get_base(user, **conn):
    base_fields = frozenset(['Arn', 'CreateDate', 'Path', 'UserId', 'UserName'])
    needs_base = False
    for field in base_fields:
        if field not in user:
            needs_base = True
            break

    if needs_base:
        user_name = _get_name_from_structure(user, 'UserName')
        user = Botor.go('iam.client.get_user', UserName=user_name, **conn)
        user = user['User']

        # cast CreateDate from a datetime to something JSON serializable.
        user.update(dict(CreateDate=str(user['CreateDate'])))

    return user


def get_user(user, output='camelized', **conn):
    """
    Orchestrates all the calls required to fully build out an IAM User in the following format:

    {
        "Arn": ...,
        "AccessKeys": ...,
        "CreateDate": ...,  # str
        "InlinePolicies": ...,
        "ManagedPolicies": ...,
        "MFADevices": ...,
        "Path": ...,
        "UserId": ...,
        "UserName": ...,
        "SigningCerts": ...
    }

    :param user: dict containing (at the very least) user_name and/or arn.
    :param output: Determines whether keys should be returned camelized or underscored.
    :param conn: dict containing enough information to make a connection to the desired account.
    Must at least have 'assume_role' key.
    :return: dict containing fully built out user.
    """
    user = modify(user, 'camelized')
    if user.get('Arn'):
        conn.update(_conn_from_arn(user.get('Arn')))
    user = _get_base(user, **conn)
    user.update(
        {
            'access_keys': get_user_access_keys(user, **conn),
            'inline_policies': get_user_inline_policies(user, **conn),
            'managed_policies': get_user_managed_policies(user, **conn),
            'mfa_devices': get_user_mfa_devices(user, **conn),
            'login_profile': get_user_login_profile(user, **conn),
            'signing_certificates': get_user_signing_certificates(user, **conn)
        }
    )
    return modify(user, format=output)
