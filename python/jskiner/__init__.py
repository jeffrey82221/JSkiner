from .cmd import run
from . import schema
from .jskiner import InferenceEngine

__doc__ = jskiner.__doc__
if hasattr(jskiner, "__all__"):
    __all__ = jskiner.__all__

if __name__ == '__main__':
    print(run)
    print(schema)
    print(InferenceEngine)
