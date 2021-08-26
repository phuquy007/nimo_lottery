import pymongo
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
from readFile import readFile
from enum import Enum

# Selenium load the website
chrome_options = Options()
# chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=800x600")  
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:\chromedriver\chromedriver.exe")
url = 'https://www.nimo.tv/mkt/act/super/bean_box_lottery'
driver.get(url)
time.sleep(2)


box1 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[1]")
box2 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[2]")
box3 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[3]")
box4 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[4]")
box5 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[5]")
box6 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[6]")
box7 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[7]")
box8 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[8]")

main_window_handle = None
while not main_window_handle:
    main_window_handle = driver.current_window_handle

time.sleep(0.5)
box1.click()
time.sleep(0.5)

signin_window_handle = None
while not signin_window_handle:
    for handle in driver.window_handles:
        if handle != main_window_handle:
            signin_window_handle = handle
            break

driver.switch_to_window(signin_window_handle)
loginForm = driver.find_element_by_xpath("//*[@class='nimo-login-content-wrapper']")
areaCode = driver.find_element_by_xpath("//*[@class='nimo-login-body-area-code']")
phoneNumber = driver.find_element_by_xpath("//*[@class='phone-number-input']")
password = driver.find_element_by_xpath("//*[text()='Enter Password']")
loginButton = driver.find_element_by_xpath("//*[@class='nimo-login-body-button']")

driver.switch_to_window(main_window_handle)