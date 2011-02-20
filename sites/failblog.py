from datetime import datetime
import hashlib

from BeautifulSoup import BeautifulSoup

from web.models import Story, StoryContent
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
      items.append(StoryContent(internal_id=internal_id, content=entry,
          published_date=date))
    return items

  def generate_hash(self, entry):
    return entry.internal_id
