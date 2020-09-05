import nltk
import newspaper
from newspaper import Article
from newsplease import NewsPlease
from .helpers import (catch, news_content, unicode)
from src.compare import Compare
from src.content import Content
from src.title import Title
from src.author import Author

class News:

  def __init__(self, url: str) -> bool:

    self.url = url

    #NewsPlease Scraper

    newsplease = catch('None', lambda: NewsPlease.from_url(self.url, timeout=6))

    #Newspaper3K Scraper

    article = catch('None', lambda: Article(self.url, timeout=6, MIN_WORD_COUNT=600))
    catch('None', lambda: article.download())
    catch('None', lambda: article.parse())
    catch('None', lambda: article.nlp())

    #Content Scraper (self code)
    content = catch('None', lambda: Content(article.html, article.title))

    #Title Scraper (self code)
    title = catch('None', lambda: Title(article.html))

    #Author Scraper (self code)
    author = catch('None', lambda: Author(article.html))
  

    if all([newsplease, article]) == None:
        raise ValueError("No Content")

    # News Content
    self.content = catch('None', lambda: news_content(article.text) if (article.text != None and len(article.text) > 600) 
      else news_content(newsplease.maintext) if (newsplease.maintext != None and len(newsplease.maintext) > 600) 
      else content.check(article.text) if (content.text() != None and len(article.text) < 600)
      else news_content(article.text) if article.text != None
      else  'None'
    )

    # News Author
    self.authors = catch('list', lambda: author.name if (author.name != None and author.name not in newsplease.authors) 
      else newsplease.authors if len(newsplease.authors) != 0 else article.authors if len(
      article.authors) != 0 else ['None'])

    # News Published Date
    self.published_date = catch('None', lambda: str(newsplease.date_publish) if str(newsplease.date_publish) != 'None' else
      article.meta_data['article']['published_time'] if article.meta_data['article']['published_time'] != None else 'None')

    # News Image
    self.image_url = catch('None', lambda: newsplease.image_url if newsplease.image_url != None else article.top_image
      if article.top_image != None else 'None')
    

    # News Headline
    self.headline = catch('None', lambda: unicode(title.text()) if title.text() != None else
            unicode(article.title) if article.title != None else 
            unicode(newsplease.title) if newsplease.title != None else 'None')

    # News Keywords
    self.keywords = catch('list', lambda: article.keywords)

    # Dict
    self.news_dict = catch ('dict', lambda: {
      'headline': self.headline,
      'author': self.authors,
      'published_date': self.published_date,
      'image_url': self.image_url,
      'contents': self.content.replace("\n", "").strip(),
      'keyword': self.keywords,
      'url': self.url
    })