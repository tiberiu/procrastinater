from datetime import datetime
import hashlib

from BeautifulSoup import BeautifulSoup

from web.models import Story, StoryContent
from sites.base import Site

class Failbook(Site):
  site_id = 1

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
    return "http://failbook.failblog.org/page/" + str(page_id)

  def parse_page(self, page, encoding="UTF-8"):
    soup = BeautifulSoup(unicode(page, encoding),
        convertEntities=BeautifulSoup.HTML_ENTITIES)

    items = []
    posts = soup.findAll("div", {"class": "post"})
    for post in posts:
      entry = post.findAll("div", {"class": "md"})
      if len(entry) > 0:
        imgs = entry[0].findAll("img");
        if len(imgs):
          img = unicode(str(imgs[0]), encoding);
        else:
          continue

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

      items.append(StoryContent(content=img, title=title, published_date=date))

    return items

  def generate_hash(self, entry):
    src = entry.content.split("src=")[-1].split("\"")[1]
    hash = hashlib.md5()
    hash.update(src)
    return hash.hexdigest()
