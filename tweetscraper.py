from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from bs4 import BeautifulSoup


options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver', options=options)
driver.implicitly_wait(10)

url = "https://twitter.com/takadagod/"
driver.get(url)

# articleタグが読み込まれるまで待機（最大15秒）
WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.TAG_NAME, 'article')))
while True:
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")# 下までスクロール
  elems_articles = driver.find_elements(By.TAG_NAME, 'article')# ツイートの article を参照

# 各ツイートをパース
  for elem_article in elems_articles:
    try:
      html = elem_article.get_attribute('innerHTML')
      soup = BeautifulSoup(html, features='lxml')
      results = soup.findAll("div", {"data-testid" : "tweetText"})
      tweet_text = results[0].get_text()
      print(tweet_text+"\n")
      f = open('takadakenshi.txt', 'a')
      f.write(tweet_text+"\n")
      f.close()
    except Exception as e:
      print (e)
