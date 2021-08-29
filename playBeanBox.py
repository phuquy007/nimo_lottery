import pymongo
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time

# Connect to Mongo
CONNECTION_STRING = "mongodb+srv://Ryan:trantran2312@cluster0.pwc6h.mongodb.net/NimoLottery?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client["NimoLottery"]
boxCollection = db["BeanBoxes"]

# Selenium load the website
chrome_options = Options()
# chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=10x10")  
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:\chromedriver\chromedriver.exe")
url = 'https://www.nimo.tv/mkt/act/super/bean_box_lottery'
driver.get(url)
time.sleep(2)

# try:
# box1 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[1]")

# main_window_handle = None
# while not main_window_handle:
#     main_window_handle = driver.current_window_handle

# box1.click()
# time.sleep(1)

# print(main_window_handle)
# print(driver.window_handles)
# login_window_handle = None
# while not login_window_handle:
#     for handle in driver.window_handles:
#         if handle != main_window_handle:
#             login_window_handle = handle
#             break
# print(login_window_handle)
# driver.switch_to.window(login_window_handle)
# print("in here")

# checkbox = driver.find_element_by_xpath("//*[@id='container']/div[3]/div/div[2]/div/div[2]/div/div[2]/div/div[4]/span")
# confirm = driver.find_element_by_xpath("//*[@id='container']/div[3]/div/div[2]/div/div[2]/div/div[2]/div/div[2]")

# areacode = driver.find_element_by_xpath("//i[contains(@class,'nimo-icon-caret-down')]")
# phoneNumber = driver.find_element_by_xpath("//input[contains(@class,'phone-number-input')]")
# password = driver.find_element_by_xpath("//input[@placeholder = 'Enter Password']")
# loginButton = driver.find_element_by_xpath("//button[contains(@class,'nimo-login-body-button')]")
# areacode.click()
# time.sleep(0.1)
# vietnameAreaCode = driver.find_element_by_xpath("//div[text()='Vietnam']")
# vietnameAreaCode.click()
# time.sleep(0.1)
# phoneNumber.send_keys("363688557")
# time.sleep(0.1)
# password.send_keys("4blablablabla")
# time.sleep(0.1)
# loginButton.click()

# closeDown = driver.find_element_by_xpath("//i[contains(@class,'SaleGoldBeanNoticeModal__close')]")
# closeDown.click()
# time.sleep(0.5)
# driver.execute_script("window.scrollTo(0, 450)") 

def Login():
    closeDown = driver.find_element_by_xpath("//i[contains(@class,'SaleGoldBeanNoticeModal__close')]")
    closeDown.click()
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, 450)") 
    box1 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[1]")
    box1.click()
    time.sleep(1)
    areacode = driver.find_element_by_xpath("//i[contains(@class,'nimo-icon-caret-down')]")
    phoneNumber = driver.find_element_by_xpath("//input[contains(@class,'phone-number-input')]")
    password = driver.find_element_by_xpath("//input[@placeholder = 'Enter Password']")
    loginButton = driver.find_element_by_xpath("//button[contains(@class,'nimo-login-body-button')]")
    areacode.click()
    time.sleep(0.1)
    vietnameAreaCode = driver.find_element_by_xpath("//div[text()='Vietnam']")
    vietnameAreaCode.click()
    time.sleep(0.1)
    phoneNumber.send_keys("363688557")
    time.sleep(0.1)
    password.send_keys("4blablablabla")
    time.sleep(0.1)
    loginButton.click() 
    time.sleep(2.5)
    
    closeDown = driver.find_element_by_xpath("//i[contains(@class,'SaleGoldBeanNoticeModal__close')]")
    closeDown.click()
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, 420)") 

Login()

time.sleep(1)

box1 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div/div/div[2]")
print(box1.text)

