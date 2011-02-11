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

    # FIXME: This is bad, I think we should use pickling :)
    self.content = unicode(self.content)

  @staticmethod
  def load(story_id):
    story = session.query(Story).filter(Story.id==story_id).one()
    return story

  def __repr__(self):
    return "<Story source_site=%s hash=%s content=%s>" % (
        repr(self.source_site), repr(self.hash), repr(self.content))

mapper(Story, stories_table)
