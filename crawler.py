#!/usr/bin/env python

import urllib2
from datetime import datetime
import logging

from BeautifulSoup import BeautifulSoup

from sql import *
from models import *
from sites import *

class Crawler(object):
  def __init__(self):
    self.sites = [
        ('failbook', Failbook()),
        #TODO: ('tv.com', TVcom())
        ('failblog', Failblog()),
        ('fmylife', Fmylife())
    ]

  def download_page(self, url):
    request = HttpRequest(url)
    success = request.download()
    if not success:
      return None
    else:
      return request

  def crawl_site(self, site):
    site_class = site[1]
    page_id = 1
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

      logging.info("Wrote %d item. Should continue? %d " %
          (count, should_continue))
      if not should_continue:
        next_page = False
      else:
        page_id += 1

  def crawl(self):
    for site in self.sites:
      self.crawl_site(site)

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  crawler = Crawler()
  crawler.crawl()
