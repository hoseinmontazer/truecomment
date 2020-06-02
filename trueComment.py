import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line
import os.path
import requests
from bs4 import BeautifulSoup
import re

define("port", default=8887, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


class db:
    def coneectdb():
        mydb = mysql.connector.connect(
        host="172.17.0.4",
        user="root",
        passwd="123456",
        database="url",
        auth_plugin="mysql_native_password"
        )
        return mydb



class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return  self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    def get(self):
        self.render("url.html",)
    def post(self):
        url = str(self.get_argument("url"))
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        name = soup.find(class_="c-product__title")
        image = str(soup.find(class_="c-gallery__img"))
        img = re.search("https://(.*?)/?.jpg",image)
        print(img.group())
        i = {"name": name.text.strip()}
        self.render("comment.html", message=i)     


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
    (r"/", MainHandler),    
    ], cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=False,
        debug=options.debug)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()