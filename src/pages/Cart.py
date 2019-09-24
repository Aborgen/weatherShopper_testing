from .Menu import Item
from .Page import Page
from datetime import datetime
from enum import Enum
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing import List, NamedTuple, Optional, Tuple

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

  def pay(self):
    button = self._driver.find_element_by_xpath("//button[@type='submit']")
    button.click()
    try:
      modal = WebDriverWait(self._driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, 'stripe_checkout_app')))
    except:
      raise Exception

    return Payment(self._driver).pay()

class Payment():
  class Credentials(NamedTuple):
    email         : str
    cardNumber    : str
    expirationDate: str
    CVC           : str
    ZIP           : str

  class Fields(Enum):
    EMAIL = 0
    CARD = 1
    DATE = 2
    CVC = 3

  _creds: Credentials
  _driver: webdriver

  def __init__(self, driver: webdriver):
    self._driver = driver
    self._creds = self._initCredentials()

  def pay(self):
    fields = self._driver.find_elements_by_xpath("//form[@class='Modal-form']//div[@class='Textbox-inputRow']/input")
    fields[self.Fields.EMAIL.value].send_keys(self._creds.email)
    fields[self.Fields.CARD.value].send_keys(self._creds.cardNumber)
    fields[self.Fields.DATE.value].send_keys(self._creds.expirationDate)
    fields[self.Fields.CVC.value].send_keys(self._creds.CVC)

    # Zipcode input appears for some card numbers
    zipcodeField = None
    try:
      zipcodeField = WebDriverWait(self._driver, 2).until(EC.presence_of_element_located((By.XPATH, "//form[@class='Modal-form']//div[@class='Textbox-inputRow']/input[@placeholder='ZIP Code']")))
    except:
      zipcodeField = None
    
    if zipcodeField:
      zipcodeField.send_keys(self._creds.ZIP)

    # Submit
    button = self._driver.find_element_by_xpath("//button[@type='submit']")
    button.click()
    return button

  def _initCredentials(self):
    email = "Test@test.test"
    cardNumber = "4242424242424242"
    now = datetime.now()
    expirationDate = f"{now.month}{now.year}"
    CVC = "000"
    ZIP = "55555"
    return self.Credentials(email, cardNumber, expirationDate, CVC, ZIP)


