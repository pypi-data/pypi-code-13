from botor import Botor
from botor.aws.iam import get_role_managed_policies, get_role_inline_policies, get_role_instance_profiles
from bozor.aws.iam import _get_name_from_structure, modify, _conn_from_arn


def _get_base(role, **conn):
    """
    Determine whether the boto get_role call needs to be made or if we already have all that data
    in the role object.
    :param role: dict containing (at the very least) role_name and/or arn.
    :param conn: dict containing enough information to make a connection to the desired account.
    :return: Camelized dict describing role containing all all base_fields.
    """
    base_fields = frozenset(['Arn', 'AssumeRolePolicyDocument', 'Path', 'RoleId', 'RoleName', 'CreateDate'])
    needs_base = False

    for field in base_fields:
        if field not in role:
            needs_base = True
            break

    if needs_base:
        role_name = _get_name_from_structure(role, 'RoleName')
        role = Botor.go('iam.client.get_role', RoleName=role_name, **conn)
        role = role['Role']

        # cast CreateDate from a datetime to something JSON serializable.
        role.update(dict(CreateDate=str(role['CreateDate'])))

    return role


def get_role(role, output='camelized', **conn):
    """
    Orchestrates all the calls required to fully build out an IAM Role in the following format:

    {
        "Arn": ...,
        "AssumeRolePolicyDocument": ...,
        "CreateDate": ...,  # str
        "InlinePolicies": ...,
        "InstanceProfiles": ...,
        "ManagedPolicies": ...,
        "Path": ...,
        "RoleId": ...,
        "RoleName": ...,
    }

    :param role: dict containing (at the very least) role_name and/or arn.
    :param output: Determines whether keys should be returned camelized or underscored.
    :param conn: dict containing enough information to make a connection to the desired account.
    Must at least have 'assume_role' key.
    :return: dict containing a fully built out role.
    """
    role = modify(role, 'camelized')
    if role.get('Arn'):  # otherwise, account_number can be included in **conn
        conn.update(_conn_from_arn(role.get('Arn')))
    role = _get_base(role, **conn)
    role.update(
        {
            'managed_policies': get_role_managed_policies(role, **conn),
            'inline_policies': get_role_inline_policies(role, **conn),
            'instance_profiles': get_role_instance_profiles(role, **conn)
        }
    )
    return modify(role, format=output)