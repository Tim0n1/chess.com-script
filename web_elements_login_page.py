from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()
driver.get('https://www.chess.com/login')
submit_login_form = driver.find_element(by='id', value='login')
email = driver.find_element(By.ID, 'username')
password = driver.find_element(By.ID, 'password')
def error_check():
    try:
        error_element = driver.find_element(By.CLASS_NAME, 'authentication-login-error')
        print(error_element.text)
    except Exception:
        print('Successful login!')
#home_page_play = driver.find_element(By.CLASS_NAME, 'nav-link-component nav-link-main-design nav-link-top-level sprite play-top')