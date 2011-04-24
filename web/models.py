from datetime import datetime, timedelta
import logging

from django.db import models
from django.contrib.auth.models import User

from web.pickle_field import PickledObjectField

class EntryType(models.Model):
  type_name = models.CharField(max_length=128)
  followers = models.ManyToManyField(User)

  def __unicode__(self):
    return u"type_name=%s type_id=%s" % (self.type_name,
      self.id)

  def get_type(id):
    return EntryType.objects.get(id=id)

  @staticmethod
  def get_user_types(user_id):
    return EntryType.objects.filter(followers=user_id)

  @staticmethod
  def get_types(ids=None):
    if not ids:
      return EntryType.objects.all()
    else:
      return EntryType.objects.filter(id__in=ids)

  def add_follower(self, user_id):
    user = User.objects.get(id=user_id)
    self.followers.add(user)
    return self.save()

  def remove_follower(self, user_id):
    user = User.objects.get(id=user_id)
    self.followers.remove(user)
    return self.save()

class Story(models.Model):
  source_site = models.IntegerField()
  content = PickledObjectField()
  hash = models.CharField(max_length=128, unique=True)
  date = models.DateTimeField()
  crawled_date = models.DateTimeField(auto_now=True)
  entry_type = models.ForeignKey(EntryType)
  users = models.ManyToManyField(User)

  # Fuck, fuck, fuck
  @staticmethod
  def _read_stories_subquery(user_id):
    subquery = "SELECT web_story.id \
          FROM web_story \
          LEFT JOIN web_story_users \
            ON web_story_users.story_id = web_story.id \
          WHERE web_story_users.user_id = '%d'" % user_id
    return subquery

  @staticmethod
  def _entrytype_subquery(user_id):
    subquery = "SELECT web_entrytype.id \
          FROM web_entrytype \
          LEFT JOIN web_entrytype_followers \
            ON web_entrytype_followers.entrytype_id = web_entrytype.id \
          WHERE web_entrytype_followers.user_id = '%d'" % user_id
    return subquery

  @staticmethod
  def get_episodes_by_range(start_date, end_date, user_id):
    #FIXME: We need a better way than hardcoding this
    shows_sites_id = [2]

    entrytypes = EntryType.objects.filter(followers__id=user_id)

    episodes = Story.objects.filter(date__gt=start_date,
        date__lte=end_date, entry_type__in=entrytypes)
    ret = []
    for episode in episodes:
      if 'air_date' in episode.content.__dict__:
        ret.append(episode.content)
    return ret

  @staticmethod
  def get_next_stream_story(user_id):
    #FIXME: We need a better way than hardcoding this
    sites_id = [1, 3, 4]

    # user_id should be an int
    if not isinstance(user_id, int):
      try:
        user_id = int(user_id)
      except:
        raise ValueError

    # I found no better way of doing this but with a raw query
    # and using a subquery

    # Get stories read by user
    # No query is being done here
    # These functions just return the string for the subquery
    read_stories_subquery = Story._read_stories_subquery(user_id)
    # Get entry types followed by user
    entrytype_subquery = Story._entrytype_subquery(user_id)

    # Get the first story that isn't in the first query
    query = "SELECT * \
          FROM web_story \
          WHERE \
            web_story.id NOT IN (%s) AND \
            web_story.entry_type_id IN (%s) AND \
            web_story.source_site IN (%s) \
          ORDER BY id DESC \
          LIMIT 1" % (read_stories_subquery, entrytype_subquery,
              ','.join(map(str, sites_id)))

    try:
      story = list(Story.objects.raw(query))[0]
      return story
    except IndexError:
      # No results
      return None

  def __unicode__(self):
    return u"<Story id=%s source_site=%s hash=%s>" % (self.id,
        self.source_site, self.hash)

  class Meta:
    verbose_name_plural = "stories"

class StoryContent():
  def __init__(self, **kwargs):
    for key in kwargs:
      setattr(self, key, kwargs[key])

  def __unicode__(self):
    import pprint
    return u"<StoryContent\n%s>" % (pprint.pformat(self.__dict__, indent=4))
