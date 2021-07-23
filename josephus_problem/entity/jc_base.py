from abc import ABC, abstractmethod


class JcBase(ABC):
    @abstractmethod
    def __init__(self, container, start_index, interval):
        pass

    @abstractmethod
    def __iter__(self):
        pass
