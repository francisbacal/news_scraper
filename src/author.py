from bs4 import BeautifulSoup
from src.compare import Compare
from nltk.corpus import stopwords
import nltk
import re

class Author:
  """Instantiate the most probable title of article
  """
  def __init__(self, html: str):

    self.soup = BeautifulSoup(html, "html.parser")
    self.name = None

    self.stop_words = set(stopwords.words('english'))

    #setup keys for comparison and instantiate Compare
    comment_keys = ["COMMENT"]
    self.comment_data = Compare(comment_keys)

    #clean up dom
    dom_tags = [tag for tag in self.soup()]

    i=0
    while i < len(dom_tags):
      attr_values = dom_tags[i].attrs.values()

      for attr_val in attr_values:

        if attr_val == "":
          continue

        if isinstance(attr_val, list):
          continue
        
        result = self.comment_data.eval(attr_val)

        if result:
          dom_tags[i].decompose()

      i += 1
    
    ul_tags = self.soup.find_all('ul')

    for ul_tag in ul_tags:
      ul_tag.decompose()
    
    #setup keys for author comparison
    author_keys = ["AUTHOR"]
    self.author_data = Compare(author_keys)

    auth_tags = ["a", "p", "div"]

    def iterate_tag(blocks):
      # highest = 0
      i=0
      while i < len(blocks):
        attr_values = blocks[i].attrs.values()

        for attr_val in attr_values:
        
          if attr_val == "":
            continue

          if isinstance(attr_val, list):
            for val in attr_val:
              result = self.author_data.eval(val)
              
              if result:
                
                possible_auth = blocks[i].text.strip().replace("\n", " ")
                possible_auth_tokens = nltk.word_tokenize(possible_auth)
                filtered_auth = [word for word in possible_auth_tokens if word.lower() not in self.stop_words]
                possible_auth = " ".join(filtered_auth)
                return possible_auth

            continue
          
          result = self.author_data.eval(attr_val)
                  
          if result:
            possible_auth = blocks[i].text.strip().replace("\n", " ")
            possible_auth_tokens = nltk.word_tokenize(possible_auth)
            filtered_auth = [word for word in possible_auth_tokens if word.lower() not in self.stop_words]
            possible_auth = " ".join(filtered_auth)
            return possible_auth

        i += 1

    
    for auth_tag in auth_tags:
      blocks = self.soup.find_all(auth_tag)
      author = iterate_tag(blocks)

      if author != None:
        self.name = author
        break
    