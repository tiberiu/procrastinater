from datetime import datetime
import hashlib

from BeautifulSoup import BeautifulSoup

from sql import *
from models import *
from sites.base import Site

class Failbook(Site):
  site_id = 1

  def get_link(self, page_id):
    return "http://failbook.failblog.org/page/" + str(page_id)

  def parse_page(self, page, encoding="UTF-8"):
    #TODO: This only takes the images
    #Should also parse other fields like title, date etc.
    soup = BeautifulSoup(page)

    fails = []
    posts = soup.findAll("div", {"class": "post"})
    for post in posts:
      entry = post.findAll("div", {"class": "md"})
      if len(entry) > 0:
        imgs = entry[0].findAll("img");
        if len(imgs):
          fails.append(imgs[0])

    date = datetime.now()
    items = []
    for fail in fails:
      content = unicode(str(fail), encoding)
      items.append(Story(self.site_id, content, self.item_hash_function,
                         date, date))

    return items

  @staticmethod
  def item_hash_function(item):
    src = item.content.split("src=")[-1].split("\"")[1]
    hash = hashlib.md5()
    hash.update(src)
    return hash.hexdigest()
