from datetime import timedelta, datetime

from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings

from web.models import Story

@login_required
def index(request, id=None):
  user_id = request.user.id
  story = Story.get_next_stream_story(user_id)

  # It's good like this until we figure a way to keep a history
  # of viewed shows
  today = datetime.today()
  week = timedelta(days=7)
  past_episodes = Story.get_episodes_by_range(today - week, today, user_id)
  next_episodes = Story.get_episodes_by_range(today, today + week, user_id)

  if story:
    story_content = story.content
    story.users.add(request.user)
    story.save()
  else:
    story_content = None

  template = loader.get_template('index.html')
  context = Context({
    "user": request.user,
    "entry_html": story_content,
    "past_episodes": past_episodes,
    "next_episodes": next_episodes,
    "DEBUG": settings.DEBUG,
  })

  return HttpResponse(template.render(context))
