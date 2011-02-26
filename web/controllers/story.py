from django.template import Context, loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from web.models import Story

@login_required
def view(request, story_id):
  story = Story.objects.get(pk=story_id)
  story_content = story.content
  t = loader.get_template('view_story.html')
  c = Context({
    "story": story_content,
    "user": request.user
  })
  return HttpResponse(t.render(c))
