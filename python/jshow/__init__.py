from .jshow import *
from .main import add

__all__ = ['add']

__doc__ = jshow.__doc__
if hasattr(jshow, "__all__"):
	__all__ = jshow.__all__