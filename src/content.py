from bs4 import BeautifulSoup
from src.compare import Compare
import nltk
from nltk.corpus import stopwords
import re


class Content:
  """Instantiate the most probable text content of article
  """
  def __init__(self, html: str, headline: str):

    self.soup = BeautifulSoup(html, 'lxml')
    self.elems = ['div']
    self.content = None

    # Instantiate Comparison logic
    headline_tokens = nltk.word_tokenize(headline)
    stop_words = set(stopwords.words('english'))
    self.filtered_headline_tokens = [tok for tok in headline_tokens if not tok in stop_words]
    self.data = Compare(self.filtered_headline_tokens)

    #get all text per div
    def iterate_el(elements):
      highest = 0

      for el in elements:
        text = " ".join(el.strings)
        result = self.data.eval(text)

        if (len(result) == len(self.filtered_headline_tokens)):
          
          if result[0]['matches'] > highest:
            highest = result[0]['matches']
            self.content = text
    
    #iterate over all div
    for i in range(len(self.elems)):
      blocks = set(self.soup.find_all(self.elems[i]))
      iterate_el(blocks)
    

  def text(self):
    """Return the article content
    """
    if self.content == None:
      return None
    if len(self.content) == 0:
        return None
    else:
      return self.content
  
  def check(self, content):
    """Check content word count and relativity
    """
    self.content_3k = content.strip()
    relativity = self.data.eval(content)
    relativity_len = len(relativity)
    headline_tokens_len = len(self.filtered_headline_tokens)
    token_match = relativity_len / headline_tokens_len
    
    sum = 0
    for i in range(relativity_len):
      sum +=  int(re.search(r'\d+', relativity[i]['similarity']).group())

    average = (sum / relativity_len) / 100

    relation = token_match / average
    
    if relation >= 0.70:
      return content
    else:
      if self.content == None:
        return self.content_3k
      if len(self.content) == 0:
        return self.content_3k
      else:
        return self.content