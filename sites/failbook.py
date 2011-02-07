from datetime import datetime

from BeautifulSoup import BeautifulSoup

from sql import *
from models import *
from sites.base import Site

class Failbook(Site):
  def __init__(self, min_date=None):
    super(self.__class__, self).__init__()
    self.site_id = 1

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
      items.append(Story(self.site_id, content, date, date))

    return items
