from src.utils import newspaper, json, csv, colorama, News, bcolors, Fore
from src.helpers import db_connect, google
#initialize colorama for terminal linting
colorama.init()

#connect to database and set collection
conn = db_connect()
db = conn.news_scraper_py
collection = db.articlesgoogle

# Query article links from database
# article_links = list(db.articlelinks.find({}, {"_id": 0,"link":1}))

# Google news links
article_links = google('COVID-19 articles', 100)


#Start scraping article
print(f"{colorama.Fore.CYAN}\nStarting scraper...{bcolors.ENDC}")
i = 0
while i < len(article_links):
  for link in article_links[i]:
    link = article_links[i][link]
  print(f"{bcolors.HEADER}\nCrawling {link}{bcolors.ENDC}")
  try:
    article = News(link)

    if article.content == "":
      print(f"{bcolors.FAIL}Skipped article: No content parsed.{bcolors.ENDC}")
      continue

    collection.insert_one(article.news_dict)
    print (f"{bcolors.OKGREEN}Scraped article {article.headline}{bcolors.ENDC}")
  except:
    print(f"{bcolors.FAIL}Skipped article{bcolors.ENDC}")
    pass
  i += 1