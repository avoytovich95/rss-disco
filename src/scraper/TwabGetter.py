import requests
from bs4 import BeautifulSoup

class TwabGetter:
  URL = 'https://www.bungie.net/en/News'

  def __init__(self, version=0):
    self.version = version
    self.events = []

  def add_event(self, event):
    self.events.append(event)
    print(self.events)

  def add_events(self, events):
    self.events = self.events + events

  def scrape(self):
    page = requests.get(self.URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    news_container = soup.find(id="news-items-container")
    news_items = news_container.find_all('a', class_="news-item")
    article_id = news_items[0]['href'].split('/')[-1]
    if int(article_id) > self.version:
      self.version = article_id
      self.__send_id(self.version)

  def __send_id(self, id):
    for event in self.events:
      event(id)