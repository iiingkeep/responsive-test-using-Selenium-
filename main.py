'''
반응형 웹 테스트

- 크롬 브라우저의 창 너비를 조절
- 각각의 사이즈로 창의 너비가 조절될 때 마다 스크롤을 내리며 스크린샷
'''

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from math import ceil
import os

class ResponsiveTester:
  
  def __init__(self, urls):
    self.urls = urls
    self.options = webdriver.ChromeOptions()
    self.options.add_experimental_option('detach', True)
    self.service = webdriver.ChromeService(ChromeDriverManager().install())
    self.browser = webdriver.Chrome(service=self.service, options=self.options)
    self.browser.maximize_window()
    self.sizes = [500, 960, 1366, 1920] 

  def makedirs(self, url):
    self.website_name = url.split('.')[1]
    if not os.path.exists(f"screenshots/{self.website_name}"):
      os.makedirs(f"screenshots/{self.website_name}")
    return self.website_name


  def screenshot(self, url, website_name):
    self.browser.get(url)
    time.sleep(2)
    window_size = self.browser.get_window_size()
    BROWSER_HEIGHT = window_size.get('height')

    for size in self.sizes:
      self.browser.set_window_size(size, BROWSER_HEIGHT)
      self.browser.execute_script(f"window.scrollTo(0, 0)")
      time.sleep(3)
      scroll_fullsize = self.browser.execute_script('return document.body.scrollHeight')
      section_height = self.browser.execute_script('return window.innerHeight')
      total_sections = ceil(scroll_fullsize/section_height)
      for section in range(total_sections):
        self.browser.execute_script(f"window.scrollTo(0, {(section) * section_height})")
        time.sleep(1)
        self.browser.save_screenshot(f"screenshots/{self.website_name}/{size}x{section+1}.png")

  def start(self):
    for url in self.urls:
      self.makedirs(url)
      self.screenshot(url, self.website_name)


urls = ['https://www.mcst.go.kr/kor/main.jsp', 
        'https://www.nts.go.kr/',
        'https://www.mpm.go.kr/mpm/']
responsive_test = ResponsiveTester(urls)
responsive_test.start()