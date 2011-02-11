from django.db import models

class Story(models.Model):
  source_site = models.IntegerField()
  content = models.TextField()
  hash = models.CharField(max_length=128, unique=True)
  date = models.DateTimeField()
  crawled_date = models.DateTimeField(auto_now=True)

  def __unicode__(self):
    return u"<Story id=%s source_site=%s hash=%s>" % (self.id,
        self.source_site, self.hash)

  class Meta:
    verbose_name_plural = "stories"
