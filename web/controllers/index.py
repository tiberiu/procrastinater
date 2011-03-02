from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings

from web.models import Story

@login_required
def index(request, id=None):
  user_id = request.user.id
  story = Story.get_next_stream_story(user_id,
      sites=[1, 3, 4])
  tv_show = Story.get_next_stream_story(user_id,
      sites=[2])

  if story:
    story_content = story.content
    story.users.add(request.user)
    story.save()
  else:
    story_content = None

  t = loader.get_template('index.html')
  c = Context({
    "user": request.user,
    "entry_html": story_content,
    "tv_show": tv_show.content,
    "DEBUG": settings.DEBUG,
  })

  return HttpResponse(t.render(c))
