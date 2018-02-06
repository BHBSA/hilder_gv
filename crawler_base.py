from abc import ABC, abstractmethod


class Crawler(ABC):

    @abstractmethod
    def start_crawler(self):
        print('未实现crawler_base方法')
        raise NotImplementedError
