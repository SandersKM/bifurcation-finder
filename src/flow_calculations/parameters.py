import typing

class Parameters:

    def __init__(self, h: float, alpha: float):
        self._h: float = h
        self._alpha: float = alpha

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, value):
        self._h = value

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        self._alpha = value
