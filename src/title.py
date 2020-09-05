from bs4 import BeautifulSoup
from src.compare import Compare
import nltk
from nltk.corpus import stopwords
import re
import time

class Title:
  """Instantiate the most probable title of article
  """
  def __init__(self, html: str):

    self.soup = BeautifulSoup(html, 'lxml')
    self.elems = ['h1', 'h2', 'h3']
    self.title = None

    #check title tag
    title_tag = self.soup.find('title').string
    filtered_title_tag = re.sub(r'[\W_]\s', ' ', title_tag)
    self.title_tag_tokens = nltk.word_tokenize(filtered_title_tag.upper())

    #get all text from h1, h2, h3
    def iterate_el(elements):  
      time.sleep(2)
      for el in elements:
        text = el.get_text(separator=" ", strip=True)
        if text != None:
          text_tokens = nltk.word_tokenize(text.upper())
          count = 0
          for token in text_tokens:
            
            if token in self.title_tag_tokens:
              count += 1
   
          similarity = count / len(text_tokens)
          if similarity >= 0.75:
            return text
          
      
    #iterate over all h elements
    for i in range(len(self.elems)):
      blocks = set(self.soup.find_all(self.elems[i]))
      probab_title = iterate_el(blocks)
      
      if probab_title != None:
        self.title = probab_title
        break
    

  def text(self):
    """Return the article title
    """
    if self.title == None:
      return None

    return self.title