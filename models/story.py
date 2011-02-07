import hashlib

from sqlalchemy.orm import mapper

from sql import *

class Story(object):
  def __init__(self, source_site, content, date=None, crawled_date=None):
    self.source_site = source_site
    self.content = content
    self.date = date
    self.crawled_date = crawled_date
    self.hash = self._generate_hash()

  def _generate_hash(self):
    src = self.content.split("src=")[-1].split("\"")[1]
    hash = hashlib.md5()
    hash.update(src)
    return hash.hexdigest()

mapper(Story, stories_table)
