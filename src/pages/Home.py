from .MoisturizerMenu import MoisturizerMenu
from .Page import Page
from .SunscreenMenu import SunscreenMenu
from selenium import webdriver

class Home(Page):
  _path = '/'

  def __init__(self, driver: webdriver, url: str):
    super().__init__(driver, url)  

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
    return MoisturizerMenu(self._driver, self._url + self._path)

  def toSunscreenMenu(self) -> Page:
    button = self._driver.find_element_by_xpath("//button[contains(text(), 'sunscreen')]")
    button.click()
    return SunscreenMenu(self._driver, self._url + self._path)

