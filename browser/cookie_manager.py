import os
import json
from requests.cookies import cookiejar_from_dict
from requests.cookies import RequestsCookieJar


class _CookieManager:
    _cookie_file = "./cookies.json"

    def __init__(self):
        self._cookies = {}
        self._open = open   # 保存open函数，因为在__del__时open已不存在
        self._load()
        self._cookie_modified = False

    def __del__(self):
        self._save()

    def _save(self):
        if not self._cookie_modified:
            return
        with self._open(self._cookie_file, "w") as fp:
            fp.write(json.dumps(self._cookies, indent=2))

    def _load(self):
        if os.path.exists(self._cookie_file):
            with open(self._cookie_file) as fp:
                self._cookies = json.load(fp)

    @staticmethod
    def _standard_url(url: str):
        if url.startswith("https://"):
            url = url[8:]
        if "/" in url:
            url = url[:url.index("/")]
        return url

    def add_cookie(self, url: str, cookie):
        self._cookies[self._standard_url(url)] = cookie
        self._cookie_modified = True

    def get_cookie(self, url):
        cookies = {}
        for c in self._cookies.get(self._standard_url(url), "").split(";"):
            pos = c.index("=")
            key, value = c[:pos], c[pos + 1:]
            cookies[key] = value
        return cookiejar_from_dict(cookies)


CookieMgr = _CookieManager()
cj = RequestsCookieJar()
