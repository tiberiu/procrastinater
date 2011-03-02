from datetime import datetime
import hashlib
import re
import logging

from BeautifulSoup import BeautifulSoup

from web.models import Story, StoryContent
from sites.base import Site

class Fmylife(Site):
  site_id = 4

  def get_link(self, page_id):
    if page_id == 1:
      return "http://www.fmylife.com"
    else:
      return "http://www.fmylife.com?page=%s" % (page_id - 1)

  def parse_page(self, page, encoding="UTF-8"):
    soup = BeautifulSoup(unicode(page, encoding),
        convertEntities=BeautifulSoup.HTML_ENTITIES)
    posts = soup.find("div", {"id": "wrapper"}).\
        findAll("div", {"class": "post"})

    items = []
    for post in posts:
      if not post.has_key("id"):
        continue

      internal_id = post["id"]

      regex = re.compile('On (?P<month>\d+)/(?P<day>\d+)/(?P<year>\d+)')
      str_date = post.find('div', {"class": "right_part"})\
          .findAll('p')[1].next
      matches = regex.search(str_date)
      day = matches.group('day')
      month = matches.group('month')
      year = matches.group('year')
      try:
        date = datetime(int(year), int(month), int(day))
      except ValueError:
        logging.critical("Invalid parsed date")
        logging.critical("From %s parsed year = %s, day = %s, month = %s" %
            (str_date, year, day, month))
        date = datetime(1970, 1, 1)

      text = post.find("p").next.string
      entry = unicode(str(text), encoding)
      items.append(StoryContent(internal_id=internal_id, content=entry,
          published_date=date))
    return items

  def generate_hash(self, entry):
    return entry.internal_id
