from serializable import (
    object_to_serializable_representation,
    object_from_serializable_representation,
    Serializable,
)
from nose.tools import eq_
import pickle

class A(Serializable):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_dict(self):
        return {"x": self.x, "y": self.y}

instance = A(1, 2)

def test_serialize_object_with_helpers():
    instance_reconstructed = object_from_serializable_representation(
        object_to_serializable_representation(instance))
    eq_(instance, instance_reconstructed)

def test_json():
    eq_(instance, A.from_json(instance.to_json()))

def test_pickle():
    eq_(instance, pickle.loads(pickle.dumps(instance)))
