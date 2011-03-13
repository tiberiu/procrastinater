from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User

from web.pickle_field import PickledObjectField

class Story(models.Model):
  source_site = models.IntegerField()
  content = PickledObjectField()
  hash = models.CharField(max_length=128, unique=True)
  date = models.DateTimeField()
  crawled_date = models.DateTimeField(auto_now=True)
  users = models.ManyToManyField(User)

  @staticmethod
  def get_episodes_by_range(start_date, end_date):
    #FIXME: We need a better way than hardcoding this
    shows_sites_id = [2]
    episodes = Story.objects.filter(date__gt=start_date,
        date__lte=end_date,
        source_site__in=shows_sites_id)
    for episode in episodes:
      if 'air_date' in episode.content.__dict__:
        yield episode.content

  @staticmethod
  def get_next_stream_story(user_id):
    #FIXME: We need a better way than hardcoding this
    stream_sites_id = [1, 3, 4]

    # I found no better way of doing this but with a raw query
    # and using a subquery

    # user_id should be an int
    if not isinstance(user_id, int):
      try:
        user_id = int(user_id)
      except:
        raise ValueError

    # Get stories read by user
    subquery = "SELECT web_story.id \
          FROM web_story \
          LEFT JOIN web_story_users \
            ON web_story_users.story_id = web_story.id \
          WHERE web_story_users.user_id = '%d'" % user_id


    # Get the first story that isn't in the first query
    query = "SELECT * \
          FROM web_story \
          WHERE \
            web_story.id NOT IN (%s) AND \
            web_story.source_site IN (%s) \
          ORDER BY id DESC \
          LIMIT 1" % (subquery, ','.join(map(str, stream_sites_id)))

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
