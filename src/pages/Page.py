from selenium import webdriver

class Page():
  _driver: webdriver
  _url   : str
  
  def __init__(self, driver: webdriver, url: str):
    self._driver = driver
    self._url = url

  def load(self):
    self._driver.get(self._url)

