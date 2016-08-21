from .base import Item
from collections import namedtuple
"""
{
 "Records": [
    {
      "eventVersion": "2.0",
      "eventTime": "1970-01-01T00:00:00.000Z",
      "requestParameters": {
        "sourceIPAddress": "127.0.0.1"
      },
      "s3": {
        "configurationId": "testConfigRule",
        "object": {
          "eTag": "0123456789abcdef0123456789abcdef",
          "sequencer": "0A1B2C3D4E5F678901",
          "key": "HappyFace.jpg",
          "size": 1024
        },
        "bucket": {
          "arn": bucketarn,
          "name": "sourcebucket",
          "ownerIdentity": {
            "principalId": "EXAMPLE"
          }
        },
        "s3SchemaVersion": "1.0"
      },
      "responseElements": {
        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH",
        "x-amz-request-id": "EXAMPLE123456789"
      },
      "awsRegion": "us-east-1",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "EXAMPLE"
      },
      "eventSource": "aws:s3"
    }
  ]
}
"""
Bucket = namedtuple('Bucket', 'arn name ownerIdentity')
Key = namedtuple('Item', 'eTag sequencer key size')


class S3Item(Item):
    def process(self, event):
        self.records = event['Records']
        self.first = event['Records'][0]
        self.s3 = self.first['s3']
        self.region = self.first['awsRegion']
        self.bucket = Bucket(**self.s3['bucket'])
        self.object = Key(**self.s3['object'])
