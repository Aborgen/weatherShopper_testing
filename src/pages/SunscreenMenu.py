from .Cart import Cart
from .Menu import Item, Menu
from .Page import Page
from enum import Enum
from selenium import webdriver
from typing import List, NamedTuple, Optional

class Categories(Enum):
  SPF30 = 'spf30'
  SPF50 = 'spf50'

class SunscreenMenu(Page, Menu):
  def __init__(self, driver: webdriver, baseUrl: str, previousUrl: Optional[str] = None):
    super().__init__(driver, baseUrl, self.__class__.PATH(), previousUrl)

  # Splits all products on page into available categories and sorts them by
  # price ascending.
  def digest(self) -> List[Item]:
    products = {}
    container = self._driver.find_element_by_xpath(f"//div[@class='container']")
    for name, member in Categories.__members__.items():
      spf = member.value.rstrip('0123456789')
      factor = member.value[len(spf):]
      lower = f"{spf}-{factor}"
      upper = f"{spf.upper()}-{factor}"
      # NOTE: Find nodes containing only upper case first. From observation, it
      #       appears much more likely to see products with SPF rather
      #       than spf. Implementation of xpath used by driver may or
      #       may not perform short circuit evalutation on logical expressions.
      path = f".//*[contains(text(), '{upper}') or contains(text(), '{lower}')]//parent::div"
      elements = container.find_elements_by_xpath(path)
      items = []
      for element in elements:
        tags = element.find_elements_by_tag_name('p')
        name = tags[0].text
        price = int(tags[1].text.split(' ')[-1])
        button = element.find_element_by_tag_name('button')
        items.append(Item(name, price, button.click))

      products[lower] = sorted(items, key=lambda item : item.price)

    return products

  def toCart(self) -> Page:
    button = self._driver.find_element_by_xpath("//button[contains(text(), 'Cart')]")
    button.click()
    previousUrl = self._baseUrl + self._path
    return Cart(self._driver, self._baseUrl, previousUrl)

  @staticmethod
  def PATH() -> str:
    return '/sunscreen'

