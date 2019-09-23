from selenium import webdriver
from typing import Optional

class Page():
  _driver     : webdriver
  _baseUrl    : str
  _path       : str
  _previousUrl: str
  
  def __init__(self, driver: webdriver, baseUrl: str, path: str, previousUrl: Optional[str] = None):
    self._driver = driver
    self._baseUrl = baseUrl
    self._path = path
    self._previousUrl = previousUrl
    self._pageTrail()
    # If previousUrl is None, that means the driver has yet to 'get' a page.
    if self._previousUrl != None:
      self._verifyPage()

  def load(self):
    self._driver.get(self._baseUrl + self._path)
    self._verifyPage()

  def _pageTrail(self):
    fullUrl = self._baseUrl + self._path
    if self._previousUrl == None:
      print(f"Start:\t{fullUrl}")
    else:
      print("-----")
      print(f"From:\t{self._previousUrl}")
      print(f"To:\t{fullUrl}")


  def _verifyPage(self):
    assert self._driver.current_url.rstrip('//') == self._baseUrl + self._path
