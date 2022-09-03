from requests import request as req
from bs4 import BeautifulSoup


class Request:

    def __init__(self,
                 base_url) -> None:
        self.base_url = base_url

    def request(self,
                method,
                endpoint,
                params=None,
                data=None,
                is_json=False):

        res = req(method=method,
                  url=f'{self.base_url}/{endpoint}',
                  data=data,
                  params=params,
                  headers={
                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
                  })

        if is_json:
            return res.json()
        return BeautifulSoup(res.content, 'lxml')
