from hark.models import BaseModel

class FolderShare(BaseModel):
    fields = ['host_path', 'guest_path', 'protocol']
    required = ['host_path', 'guest_path', 'protocol']
