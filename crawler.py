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
    self.sites = {
        'failbook': Failbook(),
        'tv.com': TVcom(),
        'failblog': Failblog(),
        'fmylife': Fmylife(),
    }
    self.site = options.site
    self.start_page = options.page
    self.force_recrawl = options.force_recrawl
    self.first_page = options.first_page
    self.dry_run = options.dry_run
    self.verbose = options.verbose

    if self.verbose:
      logging.basicConfig(level=logging.DEBUG)
    else:
      logging.basicConfig(level=logging.INFO)

  def download_page(self, url):
    request = HttpRequest(url)
    success = request.download()
    if not success:
      return None
    else:
      return request

  def crawl_site(self, site_class):
    # TODO: Take into account the force recrawl parameter
    page_id = self.start_page
    next_page = True
    items = []
    while next_page:
      url = site_class.get_link(page_id)
      if not url:
        break

      logging.debug("Trying to download page %s" % url)
      req = self.download_page(url)
      if req is None:
        # Page could not be downloaded
        # Stopping the crawl process to avoid infinite loop
        break

      encoding = req.get_encoding()
      content = req.get_content()
      logging.debug("Page downloaded. Encoding = " + encoding)
      page_items, should_continue = site_class.handle_page(page_id, content,
                                                      encoding)

      logging.info("Got %d items. Should continue? %s " %
          (len(page_items), should_continue))
      items.extend(page_items)
      if not should_continue or self.first_page:
        next_page = False
      else:
        page_id += 1
    return items

  def save_items(self):
    import random
    choices = []
    for key in self.items.keys():
      if len(self.items[key]):
        choices.append(key)

    cnt = 0
    while len(choices):
      site_name = random.choice(choices)
      site_class = self.sites[site_name]
      item = self.items[site_name].pop()

      if not site_class.should_save(item):
        continue

      if not site_class.save_item(item):
        continue

      cnt += 1
      logging.debug("Wrote item from %s" % site_name)

      choices = []
      for key in self.items.keys():
        if len(self.items[key]):
          choices.append(key)

    logging.info("Wrote %d items" % cnt)

  def crawl(self):
    if self.dry_run:
      logging.info("This is just a dry run so nothing will be saved in " +
          "the database")

    self.items = {}
    for site_name in self.sites.keys():
      site_class = self.sites[site_name]
      if not self.site or self.site == site_name:
        logging.info("Crawling site %s" % site_name)
        site_items = self.crawl_site(site_class)
        self.items[site_name] = site_items

    if not self.dry_run:
      self.save_items()

if __name__ == '__main__':
  parser = OptionParser()
  parser.add_option("-s", "--site", dest="site")
  parser.add_option("-p", "--page", dest="page", type="int", default=1)
  parser.add_option("-f", "--force-recrawl", action="store_true",
      dest="force_recrawl")
  parser.add_option("-o", "--first-page", action="store_true",
      dest="first_page")
  parser.add_option("-d", "--dry-run", action="store_true",
      dest="dry_run")
  parser.add_option("-v", "--verbose", action="store_true",
      dest="verbose")

  (options, args) = parser.parse_args()

  crawler = Crawler(options)
  crawler.crawl()
