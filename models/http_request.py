from datetime import datetime
import logging
import socket
import urllib2

class HttpRequest(object):
  _downloaded = False
  _max_tries = 3
  _timeout = 30

  def __init__(self, url):
    self.url = url

  def opened(self):
    return self._downloaded

  def get_encoding(self):
    if not self.opened():
      logging.error("Request not opened yet")
      return None
    return self.headers['content-type'].split("charset=")[-1].split(';')[0]

  def get_content(self):
    if not self.opened():
      logging.error("Request not opened yet")
      return None
    return self.content

  def get_headers(self):
    return self.headers

  def get_header(self, key):
    if not self.opened():
      return None
    if key in self.headers:
      return self.headers[key]

    return None

  def set_timeout(self, timeout):
    self._timeout = timeout

  def set_max_tries(self, max_tries):
    self._max_tries = max_tries

  def download(self):
    self.crawl_timestamp = datetime.now()
    socket.setdefaulttimeout(self._timeout)
    num_tries = 0
    while num_tries < self._max_tries:
      if num_tries < 0:
        logging.debug("Retrying %d time" % num_tries)
      else:
        try:
          self.crawl_timestamp = datetime.now()
          req = urllib2.urlopen(self.url)
          self.content = req.read()
          self.headers = req.headers
          self.code = req.code
          self._downloaded = True

          # Break the retry loop
          break
        except (HTTPError, URLError, socket.error, ValueError), fetch_error:
          # Thanks to the balaur guys for this code
          if isinstance(fetch_error, HTTPError):
            # HTTP Error
            logging.error("HTTP Error: %s" % str(fetch_error.code))

          elif isinstance(fetch_error, URLError):
            # DNS Error or network issue
            logging.error("URL or network error: %s" % str(fetch_error.reason))

          elif isinstance(fetch_error, ValueError):
            # Most probably invalid url
            logging.error("URL error: %s" % str(fetch_error))

          else:
            # Socket error
            assert(isinstance(fetch_error, socket.error))
            logging.error("Socket Error: %s" % str(feth_error))

    return self._downloaded
