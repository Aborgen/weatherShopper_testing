from .Page import Page
from abc import ABC, abstractmethod
from typing import List, NamedTuple

class Item(NamedTuple):
  name      : str
  price     : str
  addToCart : object

class Menu(ABC):
  @abstractmethod
  def digest(self) -> List[Item]:
    pass

  @abstractmethod
  def toCart(self) -> Page:
    pass

