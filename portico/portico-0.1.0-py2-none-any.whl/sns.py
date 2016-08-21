from .base import Item

"""
{
  "Records": [
    {
      "EventVersion": "1.0",
      "EventSubscriptionArn": eventsubscriptionarn,
      "EventSource": "aws:sns",
      "Sns": {
        "SignatureVersion": "1",
        "Timestamp": "1970-01-01T00:00:00.000Z",
        "Signature": "EXAMPLE",
        "SigningCertUrl": "EXAMPLE",
        "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
        "Message": "Hello from SNS!",
        "MessageAttributes": {
          "Test": {
            "Type": "String",
            "Value": "TestString"
          },
          "TestBinary": {
            "Type": "Binary",
            "Value": "TestBinary"
          }
        },
        "Type": "Notification",
        "UnsubscribeUrl": "EXAMPLE",
        "TopicArn": topicarn,
        "Subject": "TestInvoke"
      }
    }
  ]
}
"""


class SnsItem(Item):
    def process(self, event):
        self.records = event['Records']
        self.first = event['Records'][0]
        self.message = self.first['Sns']['Message']
        self.message_id = self.first['Sns']['MessageId']
        self.attributes = self.first['Sns']['MessageAttributes']
        self.subject = self.first['Sns']['Subject']
        self.topic_arn = self.first['Sns']['TopicArn']
