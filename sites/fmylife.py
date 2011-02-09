from datetime import datetime
import hashlib

from BeautifulSoup import BeautifulSoup

from sql import *
from models import *
from sites.base import Site

class Fmylife(Site):
  site_id = 4

  def get_link(self, page_id):
    return "http://www.fmylife.com?page=%s" % page_id

  def parse_page(self, page, encoding="UTF-8"):
    soup = BeautifulSoup(page)
    posts = soup.find("div", {"id": "wrapper"}).\
        findAll("div", {"class": "post"})

    items = []
    for post in posts:
      if not post.has_key("id"):
        continue

      internal_id = post["id"]
      date = datetime.now()
      text = post.find("p").next.string
      entry = unicode(str(text), encoding)
      items.append(Story(self.site_id, entry, internal_id,
                         date, date))
    return items
