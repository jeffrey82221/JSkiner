from . import jskiner
from . import schema  # noqa: F401

class InferenceEngine:
    def __init__(self, cpu_cnt=1):
        self._engine = jskiner.InferenceEngine(cpu_cnt)
    def run(self, batch):
        return eval(self._engine.run(batch))

__doc__ = jskiner.__doc__
if hasattr(jskiner, "__all__"):
    __all__ = jskiner.__all__
    __all__.append('schema')
    __all__.append('InferenceEngine')
