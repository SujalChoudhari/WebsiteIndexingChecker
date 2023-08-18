import numpy as np

class ProxyManager:
    """
        # ProxyManager
        Proxymanager keeps track of proxies submitted by user.
        It has a record of which proxies are used, and which are not.
        When imported, it shuffles the proxies, and returns a proxy one by one to the indexer.
        Everytime the the list of unused proxies is empty, it shuffles the list again.
        
        ### Failed Proxies
        It also has a record of which proxies failed, and which are not.
        If a proxy is failed then it is not used again, saving time.

        ### Using Proxies
        It will shuffle all the proxies check which proxies are working and which are not.
        If a proxy is working, it will be used for the next request, untill it fails. i.e. 20-25 requests.
        A failed proxy will not be used again.

    """
    def __init__(self, proxies: list):
        self.proxies = np.array(proxies)
        self.available_proxies_index = np.arange(len(self.proxies))
        self.current_index = 0
        self.working_proxies = np.array([])
        self.current_proxy = None
        self.update_proxy()

    def shuffle_proxies(self) -> None:
        self.working_proxies = np.unique(self.working_proxies)
        np.random.shuffle(self.working_proxies)

    def get_proxy_for_request(self):
        if self.current_proxy is None:
            return None
        p = self.current_proxy.split(":")
        if len(p) < 4:
            return None
        proxy = p[2] + ":" + p[3] + "@" + p[0] + ":" + p[1]
        return {"http": "http://" + proxy, "https": "http://" + proxy}


    def current_proxy_worked(self):
        self.working_proxies.add(self.current_index)
        self.working_proxies = np.unique(self.working_proxies)

    def update_proxy(self):
        proxy_index = 0
        if(self.available_proxies_index.size != 0):
            proxy_index = self.available_proxies_index[0]
            self.available_proxies_index = np.delete(self.available_proxies_index, 0)
        elif (self.working_proxies.size != 0) :
            proxy_index = np.random.choice(self.working_proxies)
        else:
            self.current_index = 0
            self.current_proxy = None
            return
        
        self.current_index = proxy_index
        self.current_proxy = self.proxies[proxy_index]


    def reset_chain(self):
        self.shuffle_proxies()
        self.working_proxies = np.array([])

    def get_proxy_list(self):
        return self.proxies.tolist()

    def get_remaining_proxies_amount(self):
        return len(self.working_proxies)

