from .base import _BaseModel

def base_model_factory(get_sql_results):
    class BaseModel(_BaseModel):
        pass
    BaseModel.get_sql_results = get_sql_results
    return BaseModel
