import re
import datetime
import logging

from BeautifulSoup import BeautifulSoup

from sites.base import Parser
from web.models import Story, StoryContent, EntryType

class TVcom(Parser):
  site_id = 2

  shows = [
      ("House", "22374", "4",),
      ("Lie to Me", "75671", "5"),
      ("The Mentalist", "75200", "6"),
      ("Top Gear", "27682", "7"),
      ("How I Met Your Mother", "33700", "8"),
      ("The Big Bang Theory", "58056", "9"),
      ("Grey's Anatomy", "24440", "10"),
      ("The Office", "22343", "11"),
      ("The Simpsons", "146", "12"),
      ("South Park", "344", "13"),
      ("Family Guy", "348", "14"),
      ("American Dad!", "21935", "15"),
      ("Two and a Half Men", "17206", "16")
  ]

  def get_link(self, page_id):
    # Get the (page_id)th show url
    show_name, show_id = self.shows[page_id - 1][:2]
    slug_show_name = re.sub("[^\w\s-]", "", show_name.strip().lower())
    slug_show_name = re.sub("[-\s]+", "-", slug_show_name)

    url = "http://www.tv.com/%s/show/%s/episode.html?season=All" % (
        slug_show_name, show_id)
    return url

  def parse_page(self, page_id, page, encoding):
    logging.info("Parsing tv show %s" % self.shows[page_id - 1][0])
    now = datetime.datetime.now()
    soup = BeautifulSoup(unicode(page, encoding),
        convertEntities=BeautifulSoup.HTML_ENTITIES)

    episodes = soup.findAll("li", {"class": "episode"})

    items = []
    for episode in episodes:
      content = {}
      # Extract title and synopsis
      try:
        content["title"] = episode.find("h3").a.string.strip()
      except:
        logging.warn("Unable to extract an episode's title. Skipping...")
        continue

      content["synopsis"] = " ".join(aux.strip() for aux in
          episode.find("p", {"class": "synopsis"}).findAll(text=True))
      # Extract thumbnail url
      content["thumbnail"] = episode.find(True,
          {"class": lambda aux: "THUMBNAIL" in aux.split()}).find("img")["src"]

      # Extract episode rating
      rating_div = episode.find("div", {"class": "global_score"})
      content["rating"] = rating_div.find("span", {"class": "number"}) \
          .string.strip()
      if content["rating"] != "N/A":
        content["rating_description"] = rating_div.find("span",
            {"class": "description"}).string.strip()
        content["rating_votes"] = rating_div.find("span",
            {"class": "ratings_count"}).string.strip()

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

      # Extract episode's internal properties (entry type and show id)
      regexp = re.compile("^.*/episode/(\d+)/summary.*$")
      content["show_name"] = self.shows[page_id - 1][0]
      content["show_id"] = self.shows[page_id - 1][1]
      content["show_type"] = self.shows[page_id - 1][2]

      content["episode_id"] = regexp.search(
          episode.find("h3").a["href"]).group(1)

      items.append(StoryContent(
          published_date=content.get("air_date", now), **content))

    return items

  def handle_page(self, page_id, page, encoding="UTF-8"):
    crawled_date = datetime.datetime.now()
    entries = self.parse_page(page_id, page, encoding)

    cnt = 0
    items_to_save = []
    for entry in entries:
      if not self.check_content(entry):
        continue

      hash = self.generate_hash(entry)
      entry_type = self.get_entry_type(entry)
      story = Story(source_site=self.site_id, content=entry, hash=hash,
          date=entry.published_date, crawled_date=crawled_date,
          entry_type=entry_type)
      if not self.should_save(story):
        logging.debug("Hash %s already exists" % story.hash)
        continue

      items_to_save.append(story)

    return (items_to_save, page_id < len(self.shows))

  def get_entry_type(self, entry):
    return EntryType.objects.get(id=entry.show_type)

  def should_save(self, entry):
    # Since we need to be able to update older entries, should_save returns
    # True if the item stored in the database is different than the current one
    try:
      old_entry = Story.objects.get(hash=entry.hash)
      if entry.content == old_entry.content:
        return False

      entry.id = old_entry.id
      return True
    except Story.DoesNotExist:
      return True

  def generate_hash(self, entry):
    return "%s-%s" % (entry.show_id, entry.episode_id)
