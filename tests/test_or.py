from jskiner.schema import Int, Float, Atomic, Non, Optional, Record, Array, Union


def test_or():
    assert Atomic(Int()) | Atomic(Int()) == Atomic(Int())
    assert Atomic(Int()) | Atomic(Non()) == Optional(Atomic(Int()))
    assert Atomic(Float()) | Atomic(Int()) == Union(
        {Atomic(Int()), Atomic(Float())})
    assert Atomic(Int()) | Array(Atomic(Float())) == Union(
        {Atomic(Int()), Array(Atomic(Float()))})
    assert Atomic(Int()) | Array(Atomic(Float())) == Union(
        {Array(Atomic(Float())), Atomic(Int())})
    assert Union({Atomic(Int()), Atomic(Non())}) | Atomic(
        Int()) == Optional(Atomic(Int()))
    assert Record({'a': Atomic(Int()),
                   'b': Atomic(Non())}) | Record({'b': Atomic(Float()),
                                                  'a': Atomic(Non())}) == Record({'a': Optional(Atomic(Int())),
                                                                                  'b': Optional(Atomic(Float()))})
    assert Array(
        Atomic(
            Int())) | Array(
        Atomic(
            Non())) == Array(
        Optional(
            Atomic(
                Int())))
