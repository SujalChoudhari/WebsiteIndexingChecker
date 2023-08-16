import numpy as np
import requests
import bs4
import re
from googlesearch import search as google_search
import random
from src.sheet_manager import SpreadsheetManager
from src.url_manager import URLManager
from src.proxy_manager import ProxyManager
from src.helpers import INDEXING_SEARCH_STRING


class Indexer:
    def __init__(
        self,
        proxy_manager: ProxyManager,
        url_manager: URLManager,
        sheet_manager: SpreadsheetManager,
    ):
        self.url_manager = url_manager
        self.sheet_manager = sheet_manager
        self.proxy_manager = proxy_manager
        self.unindexed_urls = np.array([])
        self.current_proxy = None

    def process(self):
        self.check_next_url()

    def check_next_url(self):
        response = self.proxy_request(
            INDEXING_SEARCH_STRING.format(self.url_manager.get_next_url())
        )
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        result = soup.find_all("a")
        print(result)

    def proxy_request(self, url, **kwargs):
        while self.proxy_manager.get_remaining_proxies_amount() > 0:
            current_proxy = self.proxy_manager.get_proxy_for_request()
            print("Using Proxy: ", current_proxy, end="\t")
            # self.proxy_manager.update_proxy()
            try:
                response = requests.get(url, proxies=current_proxy, timeout=8)
                if response.status_code == 200:
                    print("Success!")
                    return response
                else:
                    print("Failed!")
                    self.proxy_manager.update_proxy()
            except Exception as e:
                print("Failed!")
                self.proxy_manager.update_proxy()

        print("No proxies left!")
        return requests.get(url, **kwargs)
