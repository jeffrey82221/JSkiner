from jskiner.schema import Int, Float, Atomic, Record, Array, Union


def test_eq():
    assert Int() == Int()
    assert Float() == Float()
    assert Atomic(Int()) == Atomic(Int())
