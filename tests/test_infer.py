import pytest
from jskiner import InferenceEngine
from jskiner.schema import (
    Atomic,
    Int,
    Float,
    Array,
    Record,
    Optional,
    Union,
    Non,
    Unknown,
    UniformRecord,
    FieldSet,
)


@pytest.fixture
def engine():
    return InferenceEngine()


@pytest.fixture
def test_data():
    return [
        (["1"], Atomic(Int())),
        (["1.2"], Atomic(Float())),
        (["[1]"], Array(Atomic(Int()))),
        (['{"a": 1, "b": 2.0}'], Record({"a": Atomic(Int()), "b": Atomic(Float())})),
        (["1", "null"], Optional(Atomic(Int()))),
        (["1", "1.2", "null"], Union({Atomic(Float()), Atomic(Int()), Atomic(Non())})),
        (
            ['{"a": 1, "b": 2.0}', '{"a": 1, "b": 5.0}'],
            Record({"a": Atomic(Int()), "b": Atomic(Float())}),
        ),
        ([], Unknown()),
        (
            ['{"1": {"a": 5, "b": 6.0}, "2": {"a": 34, "b": 3.0 } }'],
            UniformRecord(
                FieldSet({"1", "2"}), Record({"a": Atomic(Int()), "b": Atomic(Float())})
            ),
        ),
        (
            ['{"1": [{"a": 5, "b": 6.0}], "2": [{"a": 34, "b": 3.0 }] }'],
            UniformRecord(
                FieldSet({"1", "2"}),
                Array(Record({"a": Atomic(Int()), "b": Atomic(Float())})),
            ),
        ),
        (
            ['{"1": [{"a": 5, "b": 6.0}], "2": [] }'],
            UniformRecord(
                FieldSet({"1", "2"}),
                Array(Record({"a": Atomic(Int()), "b": Atomic(Float())})),
            ),
        ),
        (
            ['{"1": [{"a": 5, "b": 6.0}], "2": [{"a": 34, "b": null }] }'],
            UniformRecord(
                FieldSet({"1", "2"}),
                Array(Record({"a": Atomic(Int()), "b": Optional(Atomic(Float()))})),
            ),
        ),
        (['{"\\"apple\\"": 1}'], Record({'"apple"': Atomic(Int())})),
        (['{"\\"apple\\"\\\\n": 1}'], Record({'"apple"\\n': Atomic(Int())})),
        (
            ['{"1\\n": {"a": 5, "b": 6.0}, "2": {"a": 34, "b": 3.0 } }'],
            UniformRecord(
                FieldSet({"1\n", "2"}),
                Record({"a": Atomic(Int()), "b": Atomic(Float())}),
            ),
        ),
    ]


def test_schema_class_ok(test_data):
    for _, schema_str in test_data:
        assert schema_str.__repr__() == str(schema_str)
        assert schema_str == schema_str
        assert eval(str(schema_str)) == eval(str(schema_str))


def test_inference_ok(engine, test_data):
    for json_list, schema_str in test_data:
        assert engine.run(json_list) == schema_str


def test_reduce_ok(engine):
    assert engine.reduce([Atomic(Int())]) == Atomic(Int())
    assert engine.reduce([Atomic(Int()), Atomic(Non())]) == Optional(Atomic(Int()))
