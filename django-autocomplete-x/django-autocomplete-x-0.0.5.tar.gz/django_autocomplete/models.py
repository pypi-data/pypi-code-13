from django.db import models
import widgets

class AutocompleteRelation(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        super(AutocompleteRelation, self).__init__(*args, **kwargs)
    # end def

    def formfield(self, **kwargs):
        field = super(AutocompleteRelation, self).formfield(**kwargs)
        widget = field.widget
        field.widget = widgets.AutocompleteWidget(
            model=self.rel, 
            list_display=['name', 'pk'], 
            search_fields=['name'], 
            format_data='%(name)s'
        )
        return field
    # end def
# end class