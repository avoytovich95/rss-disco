from time import struct_time
import feedparser
from typing import List
from feedparser.util import FeedParserDict

class RSS:
  """A class that scrapes an RSS url, and delivers articles that have been published after the saved
  date.

  Attributes:
    url (str): the rss url to retrieve articles from
    last_date (struct_time): the date of the last article retrieved
  """

  def __init__(self, url: str, last_date: struct_time = None) -> None:
    """The RSS constructor that set the url and date of last article. Date defaults to none of no
    previous article was retrieved.

    Args:
        url (str): RSS url to scrape
        last_date (struct_time, optional): time of previous article. Defaults to None.
    """
    self.url = url
    self.last_date = last_date

  def scrape(self) -> List[FeedParserDict]:
    """Scrapes the RSS url, collects all articles that have been posted past the saved date, and
    returns a list of FeedParserDicts.

    Returns:
        list[FeedParserDict]: list of FeedParserDicts containing article info
    """
    return_entries: list[FeedParserDict] = []

    feed = feedparser.parse(self.url)
    entries: list[FeedParserDict] = feed.entries
    entries.sort(key=lambda entry: entry.published_parsed)
    for entry in entries:
      if self.last_date is None or self.last_date < entry.published_parsed:
        self.last_date = entry.published_parsed
        return_entries.append(entry)
        self.__store_date(entry.published_parsed)

    return return_entries

  def __store_date(self, date: struct_time) -> None:
    """Stores the latest date of the last RSS article posted.

    Args:
        date (struct_time): date to store
    """
    print(type(date))
    pass


rss = RSS('https://www.bungie.net/en/Rss/NewsByCategory?category=all&currentpage=1&itemsPerPage=8&FILENAME=NewsRss&LOCALE=en')
rss.scrape()
# print(rss.scrape())