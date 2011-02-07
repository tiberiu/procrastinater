import urllib2
from datetime import datetime
import logging

from BeautifulSoup import BeautifulSoup

from sql import *
from models import *
from sites import *

class Crawler(object):
  def __init__(self):
    self.sites = [('failbook', Failbook())]

  def get_encoding(self, req):
    return req.headers['content-type'].split('charset=')[-1].split(';')[0]

  def download_page(self, url):
    # This should actually if the download was succesfull and stuff
    # Set headers, user agent
    return urllib2.urlopen(url)

  def crawl_site(self, site):
    site_class = site[1]
    page_id = 90
    next_page = True
    while next_page:
      url = site_class.get_link(page_id)
      logging.info("Trying to download page %s" % url)
      req = self.download_page(url)
      if req is None:
        # Page could not be downloaded
        # Stopping the crawl process to avoid infinite loop
        break

      encoding = self.get_encoding(req)
      content = req.read()
      logging.info("Page downloaded. Encoding = " + encoding)
      count, should_continue = site_class.handle_page(content, encoding)

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
