import time
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def create_driver():
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get("https://www.aruodas.lt/")
    driver.maximize_window()
    return driver


def gather_information(driver, f, writer, area):
    forward = True
    while forward:
        for ad in driver.find_elements(By.XPATH, "//tbody/tr[contains(@class, 'list-row')]"):
            try:
                if area in ad.find_element(By.XPATH, ".//td[contains(@class, 'list-adress')]/h3/a").text:
                    adresas = ad.find_element(By.XPATH, ".//td[contains(@class, 'list-adress')]/h3/a").text.replace(
                        f"{area}\n", "")
                    kaina = ad.find_element(By.XPATH,
                                            ".//td[contains(@class, 'list-adress')]/div[@class='price']/span[@class='list-item-price']").text
                    kambariai = ad.find_element(By.XPATH, ".//td[contains(@class, 'list-RoomNum')]").text
                    kvadratai = ad.find_element(By.XPATH, ".//td[contains(@class, 'list-AreaOverall')]").text
                    writer.writerow([adresas, kaina, kambariai, kvadratai])
            finally:
                continue

        if (driver.find_element(By.CSS_SELECTOR, ".pagination > a:last-child").get_attribute(
                "class") == "page-bt-disabled"):
            forward = False
            f.close()
            print("Data has been gathered, check the data.csv file")
            driver.quit()
        else:
            print("Gathering data, please wait")
            driver.find_element(By.CSS_SELECTOR, ".pagination > a:last-child").click()


print("Enter the region of Vilnius you are interested it")
rajonas = input().capitalize()
d = create_driver()
d.implicitly_wait(2)
d.find_element(By.ID, "onetrust-accept-btn-handler").click()
d.find_element(By.ID, "display_FRegion").click()
d.find_element(By.XPATH, "//div[@id='options_FRegion']/ul/li[2]/label[@class='dropDownLabel']").click()
d.find_element(By.ID, "display_text_FQuartal").click()
d.switch_to.frame("fancybox-frame")
try:
    d.find_element(By.XPATH, f"//div[@id='popupContent']//label[@title='{rajonas}']").click()
except NoSuchElementException:
    print("The specified region wasn't found")
    d.quit()
    exit()
if d.find_element(By.XPATH, f"//div[@id='popupContent']//label[@title='{rajonas}']").get_attribute(
            "class") == "lb-inactive":
    print("Selected region has no data")
    print("Scrapper is shutting down")
    time.sleep(5)
    d.quit()
    exit()
d.find_element(By.XPATH, "/html//div[@id='btSaveSelected']").click()
d.switch_to.default_content()
d.find_element(By.ID, "buttonSearchForm").click()
f = open('data.csv', 'w')
writer = csv.writer(f)
writer.writerow(['Adresas', 'Kaina', 'Kambariu skaicius', 'Kvadratiniai metrai'])
gather_information(d, f, writer, rajonas)




