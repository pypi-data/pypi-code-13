from user_service.models.model_base import ModelBase
from user_service.models.property_types import PropertyTypes, create_property


class DatedModelBase(ModelBase):
    created = create_property(PropertyTypes.DateTime, required=True, auto_now_add=True)
    updated = create_property(PropertyTypes.DateTime, required=True, auto_now=True)
