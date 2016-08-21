from pastpy._dbf_table import _DbfTable
from pastpy.models.object import Object


class ObjectDbfTable(_DbfTable):
    def _map_record(self, record):
        object_builder = Object.Builder()
        for field_name in self.field_names:
            self._map_record_field(
                field_name=field_name,
                field_value=record[field_name],
                struct_builder=object_builder,
                struct_type=Object
            )
        return object_builder.build()
