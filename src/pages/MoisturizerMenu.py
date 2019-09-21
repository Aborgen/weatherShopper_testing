from .Menu import Item, Menu
from .Page import Page
from enum import Enum
from selenium import webdriver
from typing import List, NamedTuple, Optional

class Categories(Enum):
  ALOE   = 'aloe'
  ALMOND = 'almond'

class MoisturizerMenu(Page, Menu):
  def __init__(self, driver: webdriver, baseUrl: str, path: str, previousUrl: Optional[str] = None):
    super().__init__(driver, baseUrl, self.__class__.PATH(), previousUrl)

  # Splits all products on page into available categories and sorts them by
  # price ascending.
  def digest(self) -> List[Item]:
    products = {}
    container = self._driver.find_element_by_xpath(f"//div[@class='container']")
    for name, member in Categories.__members__.items():
      value = member.value
      title = value.title()
      # NOTE: Find nodes containing title first. From observation, it
      #       appears much more likely to see products with Aloe rather
      #       than aloe. Implementation of xpath used by driver may or
      #       may not perform short circuit evalutation on logical expressions.
      path = f".//*[contains(text(), '{title}') or contains(text(), '{value}')]//parent::div"
      elements = container.find_elements_by_xpath(path)
      items = []
      for element in elements:
        tags = element.find_elements_by_tag_name('p')
        name = tags[0].text
        price = tags[1].text.split(' ')[-1]
        button = element.find_element_by_tag_name('button')
        items.append(Item(name, price, button.click))

      products[value] = sorted(items, key=lambda item : item.price)

    return products

  def toCart(self) -> Page:
    button = self._driver.find_element_by_xpath("//button[contains(text(), 'Cart')]")
    button.click()
    return button

  @staticmethod
  def PATH() -> str:
    return '/moisturizer'
    
