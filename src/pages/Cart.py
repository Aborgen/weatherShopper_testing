from .Menu import Item
from .Page import Page
from selenium import webdriver
from typing import List, Optional, Tuple

class Cart(Page):
  def __init__(self, driver: webdriver, baseUrl: str, previousUrl: Optional[str] = None):
    super().__init__(driver, baseUrl, self.__class__.PATH(), previousUrl)

  def verify(self, expectedItems: List[Item]):
    itemPairs = []
    total = 0
    for name, price, _ in expectedItems:
      itemPairs.append((name, price))
      total += int(price)

    return self.verifyTotal(total) and self.verifyItems(itemPairs)

  def verifyItems(self, itemPairs: List[Tuple[str, str]]):
    rows = self._driver.find_elements_by_xpath("//table/tbody/tr")
    presentPairs = []
    for row in rows:
      item = tuple(x.text for x in row.find_elements_by_tag_name("td"))
      presentPairs.append(item)
    
    return sorted(itemPairs) == sorted(presentPairs)

  def verifyTotal(self, expectedTotal: int):
    presentTotal = self._driver.find_element_by_id('total').text.split(' ')[-1]
    return expectedTotal == int(presentTotal)

  @staticmethod
  def PATH() -> str:
    return '/cart'

