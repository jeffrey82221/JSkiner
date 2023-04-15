import pytest
from jskiner.schema import (
    Int,
    Float,
    Atomic,
    Non,
    Optional,
    Record,
    Array,
    Union,
    Str,
    UniformRecord,
    FieldSet,
    Bool,
    Unknown,
)
from jskiner.reduce import SchemaReducer
@pytest.fixture
def basic_schema():
    return Record(
        {
            "info": Record(
                {
                    "author": Optional(Atomic(Str())),
                    "downloads": UniformRecord(
                        FieldSet({"last_day", "last_month", "last_week"}), Atomic(Int())
                    ),
                    "home_page": Optional(Atomic(Str())),
                    "project_urls": Optional(
                        UniformRecord(
                            FieldSet(
                                {
                                    "API Reference",
                                    "source code",
                                }
                            ),
                            Atomic(Str()),
                        )
                    ),
                    "release_url": Atomic(Str()),
                    "yanked_reason": Optional(Atomic(Str())),
                }
            ),
            "last_serial": Atomic(Int()),
            "urls": Array(
                Record(
                    {
                        "comment_text": Optional(Atomic(Str())),
                        "digests": UniformRecord(
                            FieldSet({"blake2b_256", "md5", "sha256"}), Atomic(Str())
                        ),
                        "downloads": Atomic(Int()),
                        "yanked_reason": Optional(Atomic(Str())),
                    }
                )
            ),
            "vulnerabilities": Array(
                Record(
                    {
                        "aliases": Array(Atomic(Str())),
                        "withdrawn": Atomic(Non()),
                    }
                )
            ),
        }
    )
@pytest.fixture
def union_schema():
    return Union(
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


def test_reduce(basic_schema, union_schema):
    assert isinstance(basic_schema, Record)
    assert isinstance(union_schema, Union)
    reducer = SchemaReducer()
    assert reducer.reduce([basic_schema.__repr__(), basic_schema.__repr__()]) == basic_schema.__repr__()
    # ans = reducer.reduce([union_schema.__repr__(), basic_schema.__repr__()])
    #assert isinstance(ans, Union)


