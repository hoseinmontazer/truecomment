import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line
import os.path

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


class db:
    def coneectdb():
        mydb = mysql.connector.connect(
        host="172.17.0.4",
        user="hoseinm",
        passwd="123456",
        database="chat",
        auth_plugin="mysql_native_password"
        )
        return mydb



class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return  self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    def get(self):
        self.render("index.html",)
    def post(self):
        url = self.get_argument("url")
        print(url)


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