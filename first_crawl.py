from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()

chrome_options.add_argument("--window-size=1920x1080")  
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:\chromedriver\chromedriver.exe")

url = 'https://www.nimo.tv/mkt/act/super/box_lottery'
driver.get(url)
time.sleep(2)

elements = driver.find_elements_by_css_selector(".")