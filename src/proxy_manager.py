import numpy as np

class ProxyManager:
    def __init__(self, proxies: list):
        self.proxies = np.array(proxies)
        self.failed_indices = set()
        self.used_indices = set()
        self.current_index = 0
        self.remaining_indices = list(range(len(self.proxies)))
        self.current_proxy = self.update_proxy()
        self.shuffle_proxies()

    def shuffle_proxies(self) -> None:
        np.random.shuffle(self.remaining_indices)

    def get_proxy_for_request(self):
        p = self.current_proxy.split(":")
        if len(p) < 4:
            return None
        proxy = p[2] + ":" + p[3] + "@" + p[0] + ":" + p[1]
        return {"http": "http://" + proxy, "https": "http://" + proxy}

    def current_proxy_failed(self):
        self.failed_indices.add(self.current_index)

    def update_proxy(self):
        if not self.remaining_indices:
            self.reset_chain()

        proxy_index = self.remaining_indices.pop(0)
        while proxy_index in self.failed_indices and len(self.remaining_indices) > 1:
            proxy_index = self.remaining_indices.pop(0)

        if len(self.remaining_indices) == 1:
            self.failed_indices.clear()

        self.current_index = proxy_index
        self.used_indices.add(proxy_index)
        proxy = self.proxies[proxy_index]
        self.current_proxy = proxy  # Set the formatted proxy string

        return proxy

    def reset_chain(self):
        self.remaining_indices.extend(self.used_indices)
        self.used_indices.clear()
        self.shuffle_proxies()

    def get_used_proxies(self):
        return [self.proxies[index] for index in self.used_indices]

    def get_remaining_proxies(self):
        return [self.proxies[index] for index in self.remaining_indices]

    def get_proxy_list(self):
        return self.proxies.tolist()

    def get_remaining_proxies_amount(self):
        return len(self.remaining_indices)

