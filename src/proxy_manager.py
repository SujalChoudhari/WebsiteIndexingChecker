import numpy as np


class ProxyManager:
    def __init__(self, proxies: list):
        self.proxies = np.array(proxies)
        self.used_indices = set()
        self.remaining_indices = list(range(len(self.proxies)))
        self.current_proxy = self.update_proxy()
        self.shuffle_proxies()

    def shuffle_proxies(self) -> None:
        np.random.shuffle(self.remaining_indices)

    def get_proxy_for_request(self) -> dict:
        p = self.current_proxy.split(":")
        proxy = p[2] + ":" + p[3] + "@" + p[0] + ":" + p[1]
        proxies = {"http": "http://" + proxy, "https": "http://" + proxy}
        return proxies

    def update_proxy(self) -> None:
        if not self.remaining_indices:
            self.reset_chain()
        proxy_index = self.remaining_indices.pop(0)
        self.used_indices.add(proxy_index)
        proxy = self.proxies[proxy_index]
        self.current_proxy = proxy
        return proxy

    def reset_chain(self) -> None:
        self.remaining_indices.extend(self.used_indices)
        self.used_indices.clear()
        self.shuffle_proxies()

    def get_used_proxies(self) -> list:
        return [self.proxies[index] for index in self.used_indices]

    def get_remaining_proxies(self) -> list:
        return [self.proxies[index] for index in self.remaining_indices]

    def get_proxy_list(self):
        return self.proxies.tolist()

    def get_remaining_proxies_amount(self):
        return len(self.remaining_indices)


if __name__ == "__main__":
    # Example usage
    proxies = ["proxy1", "proxy2", "proxy3", "proxy4", "proxy5"]
    proxy_manager = ProxyManager(proxies)

    for _ in range(10):
        print("Selected Proxy:", proxy_manager.get_proxy_for_request())

    print("Used Proxies:", proxy_manager.get_used_proxies())
    print("Remaining Proxies:", proxy_manager.get_remaining_proxies())
