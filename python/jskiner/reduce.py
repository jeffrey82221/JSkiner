from typing import Iterable

exec("from .schema import *")


class SchemaReducer:
    def __init__(self, schema_str="Unknown()"):
        self._schema = eval(schema_str)

    def reduce(self, schema_string_generator: Iterable[str]) -> str:
        try:
            for schema_string in schema_string_generator:
                self._schema |= eval(schema_string)
            return self._schema.__repr__()
        except BaseException as e:
            p1 = self._schema.__repr__()
            p2 = schema_string
            print("Reduce Error:")
            print("self._schema:\n", p1)
            print("schema_string:\n", p2)
            raise e
