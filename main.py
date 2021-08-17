import requests
import dryscrape
from bs4 import BeautifulSoup
from selenium import webdriver

url = 'https://www.nimo.tv/mkt/act/super/box_lottery'

# session = dryscrape.Session()
# session.visit(url)
# response = session.body()
# soup = BeautifulSoup(response)
# resultsRow = soup.find_all('div', {'class': 'nimo-box-lottery__box nimo-box-lottery__sudoku-box nimo-box-lottery__last-result__box'})

driver = webdriver.Chrome()
driver.get(url)
p_element = driver.find_element_by_class_name(class_='nimo-box-lottery__box nimo-box-lottery__sudoku-box nimo-box-lottery__last-result__box')
print(p_element.text)

results = []
