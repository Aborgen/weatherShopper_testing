from .Page import Page
from selenium import webdriver
from typing import Optional

class Confirmation(Page):
  def __init__(self, driver: webdriver, baseUrl: str, previousUrl: Optional[str] = None):
    super().__init__(driver, baseUrl, self.__class__.PATH(), previousUrl)

  def status(self) -> bool:
    text = self._driver.find_element_by_xpath("//div[@class='container top-space-50']/div[1]/h2").text
    return 'SUCCESS' in text

  @staticmethod
  def PATH() -> str:
    return '/confirmation'
