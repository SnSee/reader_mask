import requests
from cookie_manager import CookieMgr


class Browser:

    _max_len = 40

    @classmethod
    def _display(cls, content):
        print("")
        first_line = True
        while content:
            print("\t" if first_line else "", content[:cls._max_len])
            content = content[cls._max_len:]
            first_line = False

    @classmethod
    def get_response(cls, url):
        if not url.startswith("https://"):
            url = "https://" + url
        cookie_jar = CookieMgr.get_cookie(url)
        headers = {
            "method": "GET",
            "scheme": "https",
            "accept": "text/html,"
                      "image/avif,image/webp,image/apng,*/*;"
                      "q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "utf-8",
            "accept-language": "zh-CN,zh;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/103.0.0.0 "
                          "Safari/537.36"
        }
        response = requests.request("GET", url, headers=headers, cookies=cookie_jar)
        return response
        # with open("test.html", "w", encoding="utf-8") as fj:
        #     fj.write(bs.prettify())
        # print(bs.prettify())


if __name__ == "__main__":
    Browser.get_response("https://www.zhihu.com")
