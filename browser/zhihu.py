#! coding=utf-8
from pynput import keyboard
from bs4 import BeautifulSoup
from browser import Browser


class Zhihu(Browser):

    @staticmethod
    def _get_command():
        def on_release(key):
            nonlocal command
            command = str(key)[1]
            return False
        command = None
        with keyboard.Listener(on_release=on_release) as kl:
            kl.join()
        print()
        return command

    def show_hot(self):
        response = self.get_response("https://www.zhihu.com")
        bs = BeautifulSoup(response.text, "html.parser")
        contents = bs.findAll(name="div", class_="HotItem-content")
        i = 0
        while i < len(contents):
            content = contents[i]
            # print("title:", content.a.h2.text)
            print(f"question: {i}/{len(contents)}")
            self._display(content.get_text())
            print("1: 查看回答; "
                  "p: 上一条; "
                  "q: 退出; "
                  "其他: 下一条")
            command = self._get_command()
            print("command:", command)
            if command == "p":
                if i > 0:
                    i -= 1
                continue
            if command == "q":
                return
            if command == "1":
                self._show_answer(content.a["href"])
            i += 1

    def _show_answer(self, href):
        response = self.get_response(href)
        bs = BeautifulSoup(response.text, "html.parser")
        answers = bs.findAll(name="div", class_="List-item")
        for i, content in enumerate(answers):
            print(f"answer {i + 1}/{len(answers)}:")
            self._display(content.text)
            command = self._get_command()
            if command == "q":
                return


if __name__ == "__main__":
    Zhihu().show_hot()
