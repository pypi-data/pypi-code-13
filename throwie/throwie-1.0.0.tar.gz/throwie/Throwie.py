import boto3
import botocore.exceptions


class Throwie(object):

    def __init__(self, instances_filter_name, instances_filter_values):
        self._ec2_resource = boto3.resource('ec2')
        self._ec2_client = boto3.client('ec2')
        if not isinstance(instances_filter_name, str):
            raise ValueError('instances_filter_name must be a string, "{}" is given'.format(
                type(instances_filter_name)))

        if not isinstance(instances_filter_values, list):
            raise ValueError('instances_filter_values must be a list, "{}" is given'.format(
                type(instances_filter_values)))

        self._ec2_resourceIds = self._filter_instances(instances_filter_name, instances_filter_values)

    def _filter_instances(self, filter_name, filter_values):
        try:
            return [resource.id for resource in self._ec2_resource.instances.filter(Filters=[
                {
                    'Name':   filter_name,
                    'Values': filter_values
                }
            ])]
        except botocore.exceptions.ClientError as e:
            print "Error: {}".format(e.response['Error']['Message'])
            exit(1)

    def _add_tags(self, tags):
        try:
            return self._ec2_client.create_tags(Resources=self._ec2_resourceIds, Tags=tags)
        except botocore.exceptions.ClientError as e:
            print "Error: {}".format(e.response['Error']['Message'])
            exit(1)

    def _remove_tags(self, tags):
        try:
            return self._ec2_client.delete_tags(Resources=self._ec2_resourceIds, Tags=tags)
        except botocore.exceptions.ClientError as e:
            print "Error: {}".format(e.response['Error']['Message'])
            exit(1)

    def _convert_dict_to_tags(self, tags, keep_value=True):
        if keep_value:
            return [{'Key': key, 'Value': value} for key, value in tags.items()]
        else:
            return [{'Key': key} for key, value in tags.items()]

    def tag_instances(self, tags, prefix=None):
        self._remove_tags(self._convert_dict_to_tags(tags, False))
        self._add_tags(self._convert_dict_to_tags(tags))

        return 'Instances:\n {}\nTags: \n {}'.format(
            self._ec2_resourceIds, self._convert_dict_to_tags(tags))
