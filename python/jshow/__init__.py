from .cmd import run

__all__ = ['run']

__doc__ = jshow.__doc__
if hasattr(jshow, "__all__"):
	__all__ = jshow.__all__