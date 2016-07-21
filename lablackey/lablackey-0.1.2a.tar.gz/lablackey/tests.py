from django.conf import settings
from django.core import mail

def _check(a,b):
  success = sorted(a) == sorted(b)
  if not success:
    raise ValueError("\ndesired: %s \nactual  : %s"%(sorted(a),sorted(b)))
  return success

def check_subjects(subjects,outbox=None):
  if not outbox:
    outbox = mail.outbox
  outbox_subjects = [m.subject.replace(settings.EMAIL_SUBJECT_PREFIX,'') for m in outbox]
  return _check(subjects,outbox_subjects)

def check_recipients(recipients,outbox=None):
  if not outbox:
    outbox = mail.outbox
  outbox_recipients = [m.recipients() for m in outbox]
  return _check(recipients,outbox_recipients)
