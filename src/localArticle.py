from newspaper import Article
import io

class localArticle(Article):
    def __init__(self, url, **kwargs):
        # set url to be file_name in __init__ if it's a file handle
        super().__init__(url if isinstance(url, str) else url.name, **kwargs)
        # set standalone _url attr so that parse will work as expected
        self._url = url

    def parse(self):

        # sets html and things for you
        if isinstance(self._url, str):
            with open(self._url, 'rb') as fh:
                self.html = fh.read()

        elif isinstance(self._url, (io.TextIOWrapper, io.BufferedReader)):
            self.html = self._url.read()

        else:
            raise TypeError(f"Expected file path or file-like object, got {self._url.__class__}")

        self.download_state = 2
        # now parse will continue on with the proper params set
        super(localArticle, self).parse()


a = localArticle('file.html') # pass your file name here
a.parse()

a.text[:10]