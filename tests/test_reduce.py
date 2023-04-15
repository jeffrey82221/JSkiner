import pytest
from jskiner.schema import (
    Int,
    Atomic,
    Non,
    Optional,
    Record,
    Array,
    Str,
    UniformRecord,
    UnionRecord,
    FieldSet,
    Unknown,
)
from jskiner.reduce import SchemaReducer


@pytest.fixture
def basic_schema():
    return Record(
        {
            "info": Record(
                {
                    "author": Atomic(Str()),
                    "downloads": UniformRecord(
                        FieldSet({"last_day", "last_month", "last_week"}),
                        Atomic(Int()),
                    ),
                    "home_page": Atomic(Str()),
                    "project_urls": Optional(
                        UniformRecord(
                            FieldSet(
                                {
                                    "Bug Reports",
                                    "Travis CI",
                                }
                            ),
                            Atomic(Str()),
                        )
                    ),
                    "release_url": Atomic(Str()),
                    "yanked_reason": Atomic(Non()),
                }
            ),
            "last_serial": Atomic(Int()),
            "urls": Array(
                Record(
                    {
                        "comment_text": Atomic(Str()),
                        "digests": UniformRecord(
                            FieldSet({"blake2b_256", "md5", "sha256"}),
                            Atomic(Str()),
                        ),
                        "downloads": Atomic(Int()),
                        "yanked_reason": Atomic(Non()),
                    }
                )
            ),
            "vulnerabilities": Array(Unknown()),
        }
    )


@pytest.fixture
def union_schema():
    return UnionRecord(
        {
            Record(
                {
                    "info": Record(
                        {
                            "author": Atomic(Str()),
                            "downloads": UniformRecord(
                                FieldSet({"last_day", "last_month", "last_week"}),
                                Atomic(Int()),
                            ),
                            "home_page": Atomic(Str()),
                            "project_urls": Optional(
                                UniformRecord(
                                    FieldSet(
                                        {
                                            "Bug Reports",
                                            "Travis CI",
                                        }
                                    ),
                                    Atomic(Str()),
                                )
                            ),
                            "release_url": Atomic(Str()),
                            "yanked_reason": Atomic(Non()),
                        }
                    ),
                    "last_serial": Atomic(Int()),
                    "urls": Array(
                        Record(
                            {
                                "comment_text": Atomic(Str()),
                                "digests": UniformRecord(
                                    FieldSet({"blake2b_256", "md5", "sha256"}),
                                    Atomic(Str()),
                                ),
                                "downloads": Atomic(Int()),
                                "yanked_reason": Atomic(Non()),
                            }
                        )
                    ),
                    "vulnerabilities": Array(Unknown()),
                }
            ),
            Record({"message": Atomic(Str())}),
        }
    )


@pytest.fixture
def special_schema():
    return Record({"message": Atomic(Str())})


def test_reduce(basic_schema, union_schema, special_schema):
    assert isinstance(basic_schema, Record)
    assert isinstance(special_schema, Record)
    assert isinstance(union_schema, UnionRecord)
    reducer = SchemaReducer()
    assert (
        reducer.reduce([basic_schema.__repr__(), basic_schema.__repr__()])
        == basic_schema.__repr__()
    )
    ans = reducer.reduce([union_schema.__repr__(), basic_schema.__repr__()])
    assert isinstance(eval(ans), UnionRecord)
    ans = reducer.reduce([union_schema.__repr__(), union_schema.__repr__()])
    assert isinstance(eval(ans), UnionRecord)
    assert (
        reducer.reduce(
            [basic_schema.__repr__(), special_schema.__repr__()]
        ) == union_schema.__repr__()
    )
    assert (
        reducer.reduce(
            [
                basic_schema.__repr__(),
                special_schema.__repr__(),
                union_schema.__repr__(),
            ]
        ) == union_schema.__repr__()
    )
    assert (
        reducer.reduce(
            [
                basic_schema.__repr__(),
                union_schema.__repr__(),
                special_schema.__repr__(),
            ]
        ) == union_schema.__repr__()
    )
    assert (
        reducer.reduce(
            [union_schema.__repr__(), basic_schema.__repr__(), basic_schema.__repr__()]
        ) == union_schema.__repr__()
    )
