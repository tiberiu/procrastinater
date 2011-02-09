import collections

from sqlalchemy.orm import mapper

from sql import *

class Story(object):
  def __init__(self, source_site, content, item_hash,
               date=None, crawled_date=None):
    self.source_site = source_site
    self.content = content
    self.date = date
    self.crawled_date = crawled_date

    if isinstance(item_hash, collections.Callable):
      self.hash = item_hash(self)
    else:
      self.hash = item_hash

mapper(Story, stories_table)
