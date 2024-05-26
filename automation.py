from selenium.webdriver.chrome.options import Options
from selenium import webdriver

def automate():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get('http://127.0.0.1:8000/plot')
