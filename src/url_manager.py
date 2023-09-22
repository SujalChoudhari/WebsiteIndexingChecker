"""
URLManager
"""

import requests
import bs4
import numpy as np
from src.sheet_manager import SpreadsheetManager


class URLManager:
    """
        # URLManager
        URLManager keeps track of urls, and also how many urls have been checked.
        All the URLs are stored as a numpy array, for faster processing.
        It also gets the URLs from the sitemap files, via the `SpreadsheetManager`

        Note:
        - URLManager is not responsible for checking if the url is indexed
        - It only gets all the unique urls from the sitemap files
        - It returns a url one by one to the indexer
    """
    def __init__(self, sheet_manager: SpreadsheetManager):
        self.sheet_manager= sheet_manager
        self.sitemaps = np.array(sheet_manager.get_sitemaps())
        self.urls = np.array([])
        self.current_url_index = -1

    def process(self,has_to_resume=False):
        """
        Generate an np.array of all urls
        """
        for sitemap in self.sitemaps:
            self.urls = np.append(self.urls, self.get_url_from_xml(sitemap))
        self.urls = np.unique(self.urls)

        if has_to_resume:
            data = self.sheet_manager.get_unindexed_sheet()
            if len(data) > 0 and "completed" in data[0]:
                done_index = int(data[0].split("/")[0])
                print(done_index)
                self.current_url_index  = max(0,done_index -1)
                
    def get_url_from_xml(self, xml_url):
        """
        Extract Urls from given sitemap list
        """
        if not xml_url.endswith(".xml"):
            return [xml_url]
        res = requests.get(xml_url)
        soup = bs4.BeautifulSoup(res.text, features="xml")
        urls = soup.find_all("loc")
        result_urls = []
        for url in urls:
            if url.prefix != "image":
                url = url.text
                result_urls.append(url)
        return result_urls

    def has_more_urls(self):
        """
        Returns `True` if there are more urls to be tested
        """
        return self.current_url_index < len(self.urls)

    def get_next_url(self):
        """
        Returns next url for testing
        """
        if self.current_url_index + 1 < len(self.urls):
            self.current_url_index += 1
            return self.urls[self.current_url_index]
        else:
            return None
