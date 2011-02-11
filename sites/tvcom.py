import re
import datetime
import logging

from BeautifulSoup import BeautifulSoup

from sites.base import Site
from models import Story
from sql import session

class TVcom(Site):
  site_id = 2

  shows = [
      ("House", "22374"),
      ("Lie to Me", "75671"),
      ("The Mentalist", "75200"),
      ("Top Gear", "27682"),
      ("How I Met Your Mother", "33700"),
      ("The Big Bang Theory", "58056"),
      ("Grey's Anatomy", "24440"),
      ("The Office", "22343"),
      ("The Simpsons", "146"),
      ("South Park", "344"),
      ("Family Guy", "348"),
      ("American Dad!", "21935"),
      ("Two and a Half Men", "17206")
  ]

  def get_link(self, page_id):
    # Get the (page_id)th show url
    show_name, show_id = self.shows[page_id - 1]
    slug_show_name = re.sub("[^\w\s-]", "", show_name.strip().lower())
    slug_show_name = re.sub("[-\s]+", "-", slug_show_name)

    url = "http://www.tv.com/%s/show/%s/episode.html?season=All" % (
        slug_show_name, show_id)
    return url

  def parse_page(self, page_id, page, encoding):
    now = datetime.datetime.now()
    soup = BeautifulSoup(unicode(page, encoding),
        convertEntities=BeautifulSoup.HTML_ENTITIES)

    episodes = soup.findAll("li", {"class": "episode"})

    items = []
    for episode in episodes:
      content = {}
      # Extract title and synopsis
      content["title"] = episode.find("h3").a.string.strip()
      content["synopsis"] = " ".join(aux.strip() for aux in
          episode.find("p", {"class": "synopsis"}).findAll(text=True))
      # Extract thumbnail url
      content["thumbnail"] = episode.find(True,
          {"class": lambda aux: "THUMBNAIL" in aux.split()}).find("img")["src"]

      # Extract episode rating
      rating_div = episode.find("div", {"class": "global_score"})
      content["rating"] = rating_div.find("span", {"class": "number"}).string
      if content["rating"] != "N/A":
        content["rating_description"] = rating_div.find("span",
            {"class": "description"}).string
        content["rating_votes"] = rating_div.find("span",
            {"class": "ratings_count"}).string

      # Extract season and episode number as well as air date from meta info
      meta = episode.find("div", {"class": "meta"}).string.strip()
      season_regexp = re.compile("^Season\s+(\d+)")
      episode_regexp = re.compile("^Season\s+\d+,\s+Episode\s+(\d+)")
      air_date_regexp = re.compile("Aired:\s+(\d+)/(\d+)/(\d+)$")
      try:
        content["season"] = season_regexp.search(meta).group(1)
      except:
        pass
      try:
        content["episode"] = episode_regexp.search(meta).group(1)
      except:
        pass
      try:
        month, day, year = map(int, air_date_regexp.search(meta).groups())
        content["air_date"] = datetime.date(year, month, day)
      except:
        pass

      # Extract episode's internal id for our hash
      regexp = re.compile("^.*/episode/(\d+)/summary.*$")
      content["show_id"] = self.shows[page_id - 1][1]
      content["episode_id"] = regexp.search(
          episode.find("h3").a["href"]).group(1)

      items.append(Story(self.site_id, content, self.item_hash_function,
                         now, now))

    return items

  def handle_page(self, page_id, page, encoding="UTF-8"):
    entries = self.parse_page(page_id, page, encoding)

    cnt = 0
    for entry in entries:
      if not self.should_save(entry):
        logging.debug("Hash %s already exists" % entry.hash)
        continue

      if self.save_item(entry) == True:
        cnt += 1

    return (cnt, page_id < len(self.shows))

  def should_save(self, entry):
    # Since we need to be able to update older entries, should_save returns
    # True if the item stored in the database is different than the current one
    old_entry = session.query(Story).filter(Story.hash==entry.hash).first()
    return not old_entry or entry.content != old_entry.content

  @staticmethod
  def item_hash_function(item):
    return "%s-%s" % (item.content["show_id"], item.content["episode_id"])
