#!/usr/bin/env python

# Configure django environment
if __name__ == "__main__":
  import os
  import sys
  sys.path.append(os.path.dirname(os.path.abspath(__file__)))
  os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

from datetime import datetime
import logging
from optparse import OptionParser
import urllib2

from BeautifulSoup import BeautifulSoup

from http_request import HttpRequest
from sites import *

class Crawler(object):
  def __init__(self, options):
    self.sites = [
        ('failbook', Failbook()),
        ('tv.com', TVcom()),
        ('failblog', Failblog()),
        ('fmylife', Fmylife()),
    ]
    self.site = options.site
    self.start_page = options.page
    self.force_recrawl = options.force_recrawl

  def download_page(self, url):
    request = HttpRequest(url)
    success = request.download()
    if not success:
      return None
    else:
      return request

  def crawl_site(self, site):
    # TODO: Take into account the force recrawl parameter
    site_class = site[1]
    page_id = self.start_page
    next_page = True
    while next_page:
      url = site_class.get_link(page_id)
      if not url:
        break

      logging.info("Trying to download page %s" % url)
      req = self.download_page(url)
      if req is None:
        # Page could not be downloaded
        # Stopping the crawl process to avoid infinite loop
        break

      encoding = req.get_encoding()
      content = req.get_content()
      logging.info("Page downloaded. Encoding = " + encoding)
      count, should_continue = site_class.handle_page(page_id, content,
                                                      encoding)

      logging.info("Wrote %d item. Should continue? %s " %
          (count, should_continue))
      if not should_continue:
        next_page = False
      else:
        page_id += 1

  def crawl(self):
    for site in self.sites:
      if not self.site or self.site == site[0]:
        self.crawl_site(site)


if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  parser = OptionParser()
  parser.add_option("-s", "--site", dest="site")
  parser.add_option("-p", "--page", dest="page", type="int", default=1)
  parser.add_option("-f", "--force-recrawl", action="store_true",
      dest="force_recrawl")

  (options, args) = parser.parse_args()

  crawler = Crawler(options)
  crawler.crawl()
