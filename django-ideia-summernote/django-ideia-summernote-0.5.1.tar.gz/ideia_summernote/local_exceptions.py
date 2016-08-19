class FileSizeNotSupported(Exception):
    def __init__(self, *args, **kwargs):
        super(FileSizeNotSupported, self).__init__(*args, **kwargs)