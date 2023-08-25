import numpy as np

class ProxyManager:
    """
        # ProxyManager
        Proxymanager keeps track of proxies submitted by user.
        It has a record of which proxies are used, and which are not.
        When imported, it shuffles the proxies, and returns a proxy one by one to the indexer.
        Everytime the the list of unused proxies is empty, it shuffles the list again.
    """
    def __init__(self, proxies: list):
        self.proxies = np.array(proxies)
        self.available_proxies_index = np.arange(len(self.proxies))
        self.shuffle_proxies()
        self.current_index = 0
        self.current_proxy = None
        self.update_proxy()

    def shuffle_proxies(self) -> None:
        np.random.shuffle(self.available_proxies_index)

    def get_proxy_for_request(self):
        if self.current_proxy is None:
            return None
        p = self.current_proxy.split(":")
        if len(p) < 4:
            return None
        proxy = p[2] + ":" + p[3] + "@" + p[0] + ":" + p[1]
        return {"http": "http://" + proxy, "https": "https://" + proxy}

    def update_proxy(self):
        proxy_index = 0
        if(self.available_proxies_index.size == 0):
            self.reset_chain()
        
        proxy_index = self.available_proxies_index[0]
        self.available_proxies_index = np.delete(self.available_proxies_index, 0)
        
        self.current_index = proxy_index
        self.current_proxy = self.proxies[proxy_index]


    def reset_chain(self):
        self.available_proxies_index = np.arange(len(self.proxies))
        self.shuffle_proxies()
        
    def get_proxy_list(self):
        return self.proxies.tolist()

    def get_remaining_proxies_amount(self):
        return len(self.proxies)