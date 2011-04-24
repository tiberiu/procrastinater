from datetime import datetime
import hashlib

from BeautifulSoup import BeautifulSoup

from web.models import Story, StoryContent, EntryType
from sites.base import Parser

class Failblog(Parser):
  site_id = 3
  entry_type = 2

  months = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
  }


  def get_link(self, page_id):
    return "http://failblog.org/page/%s" % page_id

  def parse_page(self, page, encoding="UTF-8"):
    soup = BeautifulSoup(unicode(page, encoding),
        convertEntities=BeautifulSoup.HTML_ENTITIES)
    posts = soup.findAll("div", {"class": "post"})

    items = []
    for post in posts:
      #The post div has and id that looks like id="post-99312"
      internal_id = post["id"]

      title = post.find('h2').a.string.strip()
      str_date = post.find('div', {"class": "postsubtitle"})\
          .find('div', {"class": "right"}).string.strip()

      month = str_date.split('. ')[0]
      day = str_date.split('. ')[1].split(',')[0]
      year = str_date.split('. ')[1].split(',')[1]

      if not self.months.has_key(month):
        # Still saving the object for future reparsing
        date = datetime(1970, 1, 1)
        logging.debug("%s not defined as a month", month)
      else:
        try:
          date = datetime(int(year), self.months[month], int(day));
        except ValueError:
          date = datetime(1970, 1, 1)
          logging.debug("Invalid parsed date")

      p = post.find("div", {"class": "md"}).find("p")
      entry = unicode(p)
      items.append(StoryContent(internal_id=internal_id, title=title,
          content=entry, published_date=date))
    return items

  def generate_hash(self, entry):
    return entry.internal_id
