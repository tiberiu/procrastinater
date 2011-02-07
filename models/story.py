from sqlalchemy.orm import mapper

from sql import *

class Story(object):
  def __init__(self, source_site, content, hash_function,
               date=None, crawled_date=None):
    self.source_site = source_site
    self.content = content
    self.date = date
    self.crawled_date = crawled_date
    self.hash = hash_function(self)

mapper(Story, stories_table)
