from jskiner.schema import (
    Int,
    Float,
    Atomic,
    Record,
    Array,
    Union,
    Optional,
    Non,
    UnionRecord,
)


def test_eq():
    assert Int() == Int()
    assert Float() == Float()
    assert Int() != Float()
    assert Atomic(Int()) == Atomic(Int())
    assert Array(Atomic(Int())) != Array(Atomic(Float()))
    assert Record({"a": Atomic(Int()), "b": Atomic(Float())}) == Record(
        {"b": Atomic(Float()), "a": Atomic(Int())}
    )
    assert Union({Atomic(Int()), Atomic(Non())}) == Optional(Atomic(Int()))
    assert UnionRecord(
        {
            Record({"a": Atomic(Int()), "b": Atomic(Float())}),
            Record({"a": Atomic(Int()), "c": Atomic(Float())}),
        }
    ) == Record({"a": Atomic(Int()), "b": Atomic(Float()), "c": Atomic(Float())})
