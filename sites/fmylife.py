from datetime import datetime
import hashlib

from BeautifulSoup import BeautifulSoup

from web.models import Story, StoryContent
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
      items.append(StoryContent(internal_id=internal_id, content=entry,
          published_date=date))
    return items

  def generate_hash(self, entry):
    return entry.internal_id
