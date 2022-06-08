# context, fname, train, test, id, label
from dataclasses import dataclass
from abc import *

import googlemaps
import pandas as pd


@dataclass
class Dataset:
    dname : str
    sname : str
    fname : str
    train : str
    test : str
    id : str
    label : str

    @property
    def dname(self)->str:return self._dname
    @dname.setter
    def dname(self, dname): self._dname = dname
    @property
    def sname(self)->str :return self._sname
    @sname.setter
    def sname(self, sname): self._sname = sname
    @property
    def fname(self) -> str: return self._fname
    @fname.setter
    def fname(self, fname): self._fname = fname
    @property
    def train(self) -> str: return self._train
    @train.setter
    def train(self, train): self._train = train
    @property
    def test(self) -> str: return self._test
    @test.setter
    def test(self, test): self._test = test
    @property
    def id(self) -> str: return self._id
    @id.setter
    def id(self, id): self._id = id
    @property
    def label(self) -> str: return self._label
    @label.setter
    def label(self,label): self._label = label

class PrinterBase(metaclass=ABCMeta):
    @abstractmethod
    def dframe(self):
        pass

# new_file, csv, xls, json
class ReaderBase(metaclass=ABCMeta):
    @abstractmethod
    def new_file(self, file):
        pass

    @abstractmethod
    def csv(self, file):
        pass

    @abstractmethod
    def xls(self, file):
        pass

    @abstractmethod
    def json(self, file):
        pass

#Reader class
#Printer class
class Printer(PrinterBase):
    def dframe(self):
        pass

class Reader(ReaderBase):
    def new_file(self, file)-> str:
        return file.context + file.fname

    def csv(self, file) -> object:
        return pd.read_csv(f'{self.new_file(file)}', encoding='utf-8', thousands=',')

    def xls(self, file, header, cols) -> object:
        return pd.read_excel(f'{self.new_file(file)}', header=header, usecols=cols,sheet_name="")

    def json(self, file) -> object:
        return pd.read_json(f'{self.new_file(file)}', encoding='utf-8')

    def gmaps(self)->object:
        return googlemaps