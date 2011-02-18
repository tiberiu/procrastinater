from datetime import datetime
import logging

from web.models import Story

class Site(object):
  def get_link(self, page_id):
    raise NotImplementedError()

  def parse_page(self, page, encoding="UTF-8"):
    raise NotImplementedError()

  def handle_page(self, page_id, page, encoding="UTF-8"):
    entries = self.parse_page(page, encoding)

    cnt = 0
    should_continue = False
    for entry in entries:
      if not self.should_save(entry):
        logging.debug("Hash %s already exists" % entry.hash)
        continue

      if self.save_item(entry) == True:
        should_continue = True
        cnt += 1

    return (cnt, should_continue)

  def should_save(self, entry):
    nr = Story.objects.filter(hash=entry.hash).count()
    if nr > 0:
      return False
    return True

  def save_item(self, entry):
    entry.save()
    return True
