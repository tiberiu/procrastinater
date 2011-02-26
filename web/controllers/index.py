from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from web.models import Story

@login_required
def index(request, id=None):
  try:
    id = int(id)
  except ValueError:
    id = 0

  story = Story.objects.get(pk=id)
  story_content = story.content

  t = loader.get_template('index.html')
  c = Context({
    "id": id,
    "next_id": id + 1,
    "user": request.user,
    "entry_html": story_content.content
  })

  return HttpResponse(t.render(c))
