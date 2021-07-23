from abc import ABC, abstractmethod


class ReaderBase(ABC):
    @abstractmethod
    def __next__(self):
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def read(self, line_num):
        pass

    @abstractmethod
    def readline(self):
        pass
