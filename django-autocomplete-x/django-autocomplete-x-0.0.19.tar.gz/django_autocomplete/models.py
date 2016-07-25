from django.db import models
import widgets

class AutocompleteRelation(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        super(AutocompleteRelation, self).__init__(*args, **kwargs)
    # end def

# end class