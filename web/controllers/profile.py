import logging

from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from web.models import EntryType

@login_required
def edit(request):
  user_id = request.user.id

  entry_types = EntryType.get_types()
  user_types = EntryType.get_user_types(user_id)

  template = loader.get_template('edit_profile.html');
  context = Context({
    'user': request.user,
    'entry_types': entry_types,
    'user_types': user_types
  });

  return HttpResponse(template.render(context))

def save(request):
  user_id = request.user.id

#  old_pass = request.POST['old_pass']
#  new_pass = request.POST['new_pass']
#  confirm = request.POST['confirm']

  # TODO: Change Password

  type_ids = request.POST.getlist('types')

  types = EntryType.get_types(type_ids)
  user_types = EntryType.get_user_types(user_id)

  to_remove = []
  to_add = []

  # Remove user from following entry types that he doesn't want
  for type in user_types:
    if type not in types:
      type.remove_follower(user_id)

  # Add user as follower to additional entry types
  for type in types:
    if type not in user_types:
      type.add_follower(user_id)

  return HttpResponseRedirect('/profile')
