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
time.sleep(15)

# try:
box1 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[1]")
box2 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[2]")
box3 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[3]")
box4 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[4]")
box5 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[5]")
box6 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[6]")
box7 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[7]")
box8 = driver.find_element_by_xpath("//*[@id='container']/div/div[4]/div/div[8]")

key50 = driver.find_element_by_xpath("//*[@id='container']/div/div[5]/div[2]/div[1]")
key500 = driver.find_element_by_xpath("//*[@id='container']/div/div[5]/div[2]/div[2]")
key1k = driver.find_element_by_xpath("//*[@id='container']/div/div[5]/div[2]/div[3]")
key5k = driver.find_element_by_xpath("//*[@id='container']/div/div[5]/div[2]/div[4]")

main_window_handle = None
while not main_window_handle:
    main_window_handle = driver.current_window_handle

key500.click()
time.sleep(0.3)
box1.click()
time.sleep(0.5)

# print(main_window_handle)
# print(driver.window_handles)
# popup_window_handle = None
# while not popup_window_handle:
#     for handle in driver.window_handles:
#         if handle != main_window_handle:
#             popup_window_handle = handle
#             break
# print(popup_window_handle)
# driver.switch_to.window(popup_window_handle)
# print("in here")

checkbox = driver.find_element_by_xpath("//*[@id='container']/div[3]/div/div[2]/div/div[2]/div/div[2]/div/div[4]/span")
confirm = driver.find_element_by_xpath("//*[@id='container']/div[3]/div/div[2]/div/div[2]/div/div[2]/div/div[2]")
# close = driver.find_element_by_xpath("//*[@class='nimo-box-lottery__modal-close']")

checkbox.click()
time.sleep(0.2)
confirm.click()
driver.switch_to.window(main_window_handle)



