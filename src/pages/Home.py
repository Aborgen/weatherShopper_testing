from .MoisturizerMenu import MoisturizerMenu
from .Page import Page
from .SunscreenMenu import SunscreenMenu
from selenium import webdriver
from typing import Optional

class Home(Page):
  def __init__(self, driver: webdriver, baseUrl: str, previousUrl: Optional[str]= None):
    super().__init__(driver, baseUrl, self.__class__.path(), previousUrl)

  def getTemperature(self) -> int:
    degrees = self._driver.find_element_by_id('temperature').text.split(' ')[0]
    try:
      degrees = int(degrees)
    except:
      raise ValueError('Cannot find a number where expected')

    return degrees

  def toMoisturizerMenu(self) -> Page:
    button = self._driver.find_element_by_xpath("//button[contains(text(), 'moisturizer')]")
    button.click()
    previousUrl = self._baseUrl + self._path
    return MoisturizerMenu(self._driver, self._baseUrl, previousUrl)

  def toSunscreenMenu(self) -> Page:
    button = self._driver.find_element_by_xpath("//button[contains(text(), 'sunscreen')]")
    button.click()
    previousUrl = self._baseUrl + self._path
    return SunscreenMenu(self._driver, self._baseUrl, previousUrl)

  @staticmethod
  def path() -> str:
    return ''
    
