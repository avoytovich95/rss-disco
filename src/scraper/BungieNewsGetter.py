import requests
from bs4 import BeautifulSoup
from scraper import NewsType, URL, NEWS_URL

class BungieNewsGetter:

  def __init__(self, version=0, twab_only=False, ignore=None):
    self.version = version
    self.twab_only = twab_only
    self.events = []
    if ignore is None:
      self.ignore = []
    else:
      self.ignore = ignore

  def add_event(self, event):
    self.events.append(event)
    print(self.events)

  def add_events(self, events):
    self.events = self.events + events

  def get_version(self):
    return self.version

  def scrape(self):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    news_container = soup.find(id="news-items-container")
    news_items = news_container.find_all('a', class_="news-item")
    article_id = news_items[0]['href'].split('/')[-1]
    if int(article_id) > self.version:
      self.version = int(article_id)
      self.__send_id(self.version)

  def __send_id(self, id):
    page = requests.get(NEWS_URL % id)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find('title')
    if NewsType.TWAB.value in title:
      return
    elif self.__check_ignore(title):
      return
    else:
      for event in self.events:
        event(id)

  def __check_ignore(self, title):
    for i in self.ignore:
      if i in title:
        return True
    return False
