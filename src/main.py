from pages.Home import Home
from selenium import webdriver
import sys

if __name__ == '__main__':
  driver = webdriver.Firefox()
  homePage = Home(driver, 'http://localhost:5000')
  homePage.load()

  temperature = homePage.getTemperature()
  # If temperature is below 19 degrees, shop for moisturizers.
  # If temperature is above 34 degrres, shop for sunscreen.
  # We are given no instruction on what to do otherwise, so simply exit.
  if temperature < 19:
    menu = homePage.toMoisturizerMenu()
  elif temperature > 34:
    menu = homePage.toSunscreenMenu()
  else:
    sys.exit(0)

  products = menu.digest()
  # For each category, add the least expensive item
  for category, items in products.items():
    cheapestItem = items[0]
    cheapestItem.addToCart()


