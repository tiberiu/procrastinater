from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from web.models import Story

@login_required
def index(request, id=None):
  user_id = request.user.id
  story = Story.get_next_stream_story(user_id)
 
  if story:
    story_content = story.content
    story.users.add(request.user)
    story.save()
  else:
    story_content = None

  t = loader.get_template('index.html')
  c = Context({
    "user": request.user,
    "entry_html": story_content
  })

  return HttpResponse(t.render(c))
