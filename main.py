from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, "cookie")

timeout = time.time() + 5
five_min = time.time() + 60 * 5

items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]

while five_min > time.time():
    cookie.click()

    # get all upgrade <b> tags
    if time.time() > timeout:
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_price = [int(price.text.split("-")[1].strip().replace(",", "")) for price in all_prices
                      if price.text != ""]

        timeout = time.time() + 5

        # create a dictionary to store item's names and prices
        cookie_upgrade = {item_price[n]: item_ids[n] for n in range(len(item_price))}

        # find current cookie value
        money_element = driver.find_element(By.ID, "money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        # find upgrades that we currently can afford
        affordable_upgrades = {cost: id for cost, id in cookie_upgrade.items() if cookie_count > cost}

        # find the most expensive affordable upgrades and buy it
        highest_price_affordable_upgrade = max(affordable_upgrades)
        # print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]
        # print(to_purchase_id)
        driver.find_element(By.ID, to_purchase_id).click()

    if time.time() > five_min:
        cookie_per_second = driver.find_element(By.ID, "cps").text
        print(cookie_per_second)
        break

driver.quit()
