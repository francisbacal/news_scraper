from src.utils import colorama, pymongo, MongoClient, os, join, dirname, unidecode
from dotenv import load_dotenv
from googlesearch import search as googlesearch

#Set up environment variables
dotenv_path = join('./',dirname(__file__), '.env')
load_dotenv(dotenv_path)

PY_ENV = os.environ.get("PY_ENV")
errors = {'None': None, 'list': [], 'dict': {}}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def catch(default, func, handle=lambda e: e, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except:
        return errors[default]


def news_content(text):
  return unicode(' '.join(text.replace('’', '').split()))


def unicode(text: str) -> bool:
    return unidecode.unidecode(text).strip()


def db_connect():
  if PY_ENV == 'production':
    DB_URI = os.environ.get("DB_URI")
  else:
    DB_URI = 'mongodb://localhost:27017/'
  
  print(f"{colorama.Fore.CYAN}\nConnecting to MongoDB {DB_URI}...{bcolors.ENDC}")

  try:
      conn = MongoClient(DB_URI, serverSelectionTimeoutMS=5000)
      conn.server_info()
      print(f"{bcolors.OKGREEN}Connected.\n{bcolors.ENDC}")
      
  except pymongo.errors.ServerSelectionTimeoutError as err:
      print(f'{bcolors.FAIL}\nConnection to MongoDB failed. \n {err} {bcolors.ENDC}')

  return conn

def google(keyword: str, count=20):
  """get links by google search
  :param keyword {str} -- search query
  :param count {int} -- number of result links to parse
  """
  query = keyword
  print(f"{colorama.Fore.CYAN}\nGoogling keyword {bcolors.UNDERLINE}{query}...{bcolors.ENDC}")
  google = googlesearch(query, tld = 'com', lang='en', num = 10, start = 0, stop=count, pause = 2.0)
 
  results = []
  for i in google:
    results.append({'link': i})
  
  return results