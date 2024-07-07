'''
반응형 웹 테스트

- 크롬 브라우저의 창 너비를 조절
- 각각의 사이즈로 창의 너비가 조절될 때 마다 스크롤을 내리며 스크린샷
'''

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from math import ceil

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
service = webdriver.ChromeService(ChromeDriverManager().install())

browser = webdriver.Chrome(service=service, options=options)

browser.get('https://nomadcoders.co')
browser.maximize_window()
time.sleep(2)

window_size = browser.get_window_size()
BROWSER_HEIGHT = window_size.get('height')

# 크롬 브라우저가 지원하는 최소 너비 = 500px
sizes = [500, 960, 1366, 1920]
for size in sizes:
  browser.set_window_size(size, BROWSER_HEIGHT)
  browser.execute_script(f"window.scrollTo(0, 0)")
  time.sleep(3)
  scroll_fullsize = browser.execute_script('return document.body.scrollHeight')
  nav_bar_height = 64
  section_height = browser.execute_script('return window.innerHeight')-nav_bar_height
  total_sections = ceil(scroll_fullsize/section_height)
  for section in range(total_sections):
    browser.execute_script(f"window.scrollTo(0, {(section) * section_height})")
    time.sleep(1)
    browser.save_screenshot(f"screenshots/{size}x{section+1}.png")