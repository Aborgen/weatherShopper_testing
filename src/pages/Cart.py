from .Menu import Item
from .Page import Page
from selenium import webdriver
from typing import List, Optional

class Cart(Page):
  def __init__(self, driver: webdriver, baseUrl: str, previousUrl: Optional[str] = None):
    super().__init__(driver, baseUrl, self.__class__.PATH(), previousUrl)

  def verifyItems(self, expectedItems: List[Item]):
    rows = self._driver.find_elements_by_xpath("//table/tbody/tr")
    presentItems = []
    for row in rows:
      item = tuple(x.text for x in row.find_elements_by_tag_name("td"))
      presentItems.append(item)
    
    allPresent = True
    for name, price, _ in expectedItems:
      if (name, price) not in presentItems:
        allPresent = False
        break

    return allPresent

  @staticmethod
  def PATH() -> str:
    return '/cart'

