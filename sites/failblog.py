from datetime import datetime
import hashlib

from BeautifulSoup import BeautifulSoup

from sql import *
from models import *
from sites.base import Site

class Failblog(Site):
  site_id = 3

  def get_link(self, page_id):
    return "http://failblog.org/page/%s" % page_id

  def parse_page(self, page, encoding="UTF-8"):
    soup = BeautifulSoup(page)
    posts = soup.findAll("div", {"class": "post"})

    items = []
    for post in posts:
      #The post div has and id that looks like id="post-99312"
      internal_id = post["id"]

      date = datetime.now()
      p = post.find("div", {"class": "md"}).find("p")
      entry = unicode(str(p), encoding)
      items.append(Story(self.site_id, entry, internal_id,
                         date, date))
    return items
