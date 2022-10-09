from selenium.webdriver.common.by import By
import web_elements_login_page
from selenium.webdriver.common.action_chains import ActionChains
web_elements_login_page.driver.implicitly_wait(3)
web_elements_login_page.email.send_keys('timonaki')
web_elements_login_page.password.send_keys('Shadowhex06')
web_elements_login_page.submit_login_form.click()
web_elements_login_page.error_check()
# next page

home_page_play = web_elements_login_page.driver.find_element(By.CSS_SELECTOR, 'a[class="nav-link-component nav-link-main-design nav-link-top-level sprite play-top"]')
web_elements_login_page.driver.fullscreen_window()
ActionChains(web_elements_login_page.driver).move_to_element(home_page_play).click(home_page_play).perform()
play_page_play_online = web_elements_login_page.driver.find_element(By.CSS_SELECTOR, 'a[class="direct-menu-item-component direct-menu-item"]')
play_page_play_online.click()
start_game = web_elements_login_page.driver.find_element(By.CSS_SELECTOR, 'button[class="ui_v5-button-component ui_v5-button-primary ui_v5-button-large ui_v5-button-full"]')
driver = web_elements_login_page.driver