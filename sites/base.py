from datetime import datetime
import cPickle
import logging

from django.utils.encoding import force_unicode

from web.models import Story, StoryContent, EntryType

class Parser(object):
  def get_link(self, page_id):
    raise NotImplementedError()

  def parse_page(self, page, encoding="UTF-8"):
    raise NotImplementedError()

  def generate_hash(self, content):
    raise NotImplementedError()

  def handle_page(self, page_id, page, encoding="UTF-8"):
    entries = self.parse_page(page, encoding)
    crawled_date = datetime.now()

    cnt = 0
    should_continue = False
    items_to_save = []
    for entry in entries:
      if not self.check_content(entry):
        continue

      # build entry
      hash = self.generate_hash(entry)
      type = self.get_entry_type(entry)
      story = Story(source_site=self.site_id, content=entry, hash=hash,
          date=entry.published_date, crawled_date=crawled_date, entry_type=type)

      if not self.should_save(story):
        logging.debug("Hash %s already exists" % story.hash)
        continue

      should_continue = True
      items_to_save.append(story)

    return (items_to_save, should_continue)

  def should_save(self, entry):
    nr = Story.objects.filter(hash=entry.hash).count()
    if nr > 0:
      return False
    return True

  def get_mandatory_fields(self):
    return ['published_date']

  def get_entry_type(self, entry):
    return EntryType.objects.get(id=self.entry_type)

  def check_content(self, content):
    if not isinstance(content, StoryContent):
      logging.error("Content must be an instance of StoryContent, %s received"
        % content.__class__)
      return False

    for field in self.get_mandatory_fields():
      if not getattr(content, field, None):
        logging.error("Missing content field: " + field)
        return False

    return True

  def save_item(self, entry):
    entry.save()
    return True
