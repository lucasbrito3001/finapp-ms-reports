from abc import ABC, abstractmethod


class Factory(ABC):
    @abstractmethod
    def build(self):
        pass
