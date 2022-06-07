import requests
import bs4
import random
import webbrowser
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc


def FootLockerUrlGen(model):
    URL = f'https://www.footlocker.com/product/~/{model}.html'
    return URL


if __name__ == '__main__':
    print("[1]FootLocker")
    Store = int(input("Select a Number: "))
    Model = input("Model Num: ")

    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    if Store == 1:
        url = FootLockerUrlGen(Model)
        res = requests.get(url, headers=header)
        page = bs4.BeautifulSoup(res.text, "lxml")
        clean = page.title.string.replace(" | Foot Locker", "")
        listofsizesraw = page.select(".ProductDetails-form__sizes")
        listofsizesraw[0].getText()
        Sizes = str(listofsizesraw[0].getText().replace('Select a Size', ""))
        nums = ""
        count = 1
        print(f"Sizes for the {clean} include:")
        for i in Sizes:
            if count % 4 == 0:
                print(f"Size {nums + str(i)}")
                nums = ""
                count += 1
            else:
                nums = nums + str(i)
                count += 1
        print(f"Link to your shoe: https://www.footlocker.com/product/~/{Model}.html")
        size = input("What size would you like? (Ex: '4.5'): ")
        driver = uc.Chrome()
        driver.fullscreen_window()

        email = "*****"
        password = "*****"
        driver.get(
            "https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/%3Fgws_rd%3Dssl&ec=GAZAmgQ")
        time.sleep(1.5)
        driver.find_element(By.NAME, "identifier").send_keys(email, Keys.ENTER)
        time.sleep(4.5)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
        driver.find_element(By.NAME, "password").send_keys(password, Keys.ENTER)
        # log into gmail to trick Footlocker when we log in to the site

    if Store == 1:
        driver.switch_to.new_window("tab")
        driver.get(f'{url}')
        time.sleep(10)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "bluecoreCloseButton")))
            button = driver.find_element(By.NAME, 'bluecoreCloseButton')
            button.click()
        except TimeoutError:
            pass
        sign = driver.find_element(By.XPATH,
                                   "//button[@type='button'][@class='Link Link-underline c-header-ribbon__link']")
        sign.click()
        time.sleep(5)
        driver.find_element(By.NAME, "uid").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys("******", Keys.ENTER)
        time.sleep(20)
        try:
            sign = driver.find_element(By.XPATH,
                                       "//button[@type='button'][@class='Link Link-underline c-header-ribbon__link']")
            sign.click()
            time.sleep(5)
            driver.find_element(By.NAME, "uid").send_keys(email)
            driver.find_element(By.NAME, "password").send_keys("*****", Keys.ENTER) 
            # Logs in twice due to false login the first time
            time.sleep(5)
        except NoSuchElementException:
            pass

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "touAgreeBtn")))
        driver.find_element(By.ID, "touAgreeBtn").click()
        time.sleep(10)
        ActionChains(driver).scroll(0, 0, 0, 500).perform()
        time.sleep(1)
        button2 = driver.find_element(By.XPATH, f"//button[@aria-label='Size: 0{size}']");
        button2.click()
        ActionChains(driver).scroll(110, 0, 0, 0, ).perform()
        time.sleep(1)
        button3 = driver.find_element(By.XPATH, "//button[@type='submit']")
        button3.click()
        time.sleep(15)
        try:
            button4 = driver.find_element(By.XPATH, "//div[@class='geetest_radar_tip']")
            button4.click()
        except NoSuchElementException:
            print("Element didn't exist")

        time.sleep(9000)
