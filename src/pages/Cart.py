from .Menu import Item
from .Page import Page
from selenium import webdriver
from typing import List, Optional, Tuple

class Cart(Page):
  def __init__(self, driver: webdriver, baseUrl: str, previousUrl: Optional[str] = None):
    super().__init__(driver, baseUrl, self.__class__.PATH(), previousUrl)

  def verify(self, expectedItems: List[Item]) -> bool:
    itemPairs = []
    total = 0
    for name, price, _ in expectedItems:
      itemPairs.append((name, price))
      total += price

    return self.verifyTotal(total) and self.verifyItems(itemPairs)

  def verifyItems(self, itemPairs: List[Tuple[str, int]]) -> bool:
    rows = self._driver.find_elements_by_xpath("//table/tbody/tr")
    presentPairs = []
    for row in rows:
      name, price = row.find_elements_by_tag_name("td")
      name = name.text
      price = int(price.text)
      presentPairs.append((name, price))

    return sorted(presentPairs) == sorted(itemPairs)

  def verifyTotal(self, expectedTotal: int) -> bool:
    presentTotal = int(self._driver.find_element_by_id('total').text.split(' ')[-1])
    return presentTotal == expectedTotal

  @staticmethod
  def PATH() -> str:
    return '/cart'

