from abc import abstractmethod
from typing import Self

# We don't use __deepcopy__ because we want to force all subclasses to implement their own clone method
class Cloneable(object):

    @abstractmethod
    def clone(self) -> Self:
        raise NotImplementedError
