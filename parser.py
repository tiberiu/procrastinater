from BeautifulSoup import BeautifulSoup

input = open("output.html")
html = "".join(input)

soup = BeautifulSoup(html)
fails = soup.findAll("img", {"class": "event-item-lol-image"})

output = open("fails.html", "w")
for fail in fails:
  output.write(str(fail) + "<br />\n")
