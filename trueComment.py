import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line
import os.path
import requests
from bs4 import BeautifulSoup
import re
from googleapi import google
import mysql.connector



define("port", default=8887, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


class db:
    def connectdb():
        mydb = mysql.connector.connect(
        host="172.22.0.20",
        user="root",
        passwd="123456",
        database="truecomment",
        auth_plugin="mysql_native_password"
        )
        return mydb



class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        return  self.get_argument("url")

class searchUrl(BaseHandler):
    def DigikalaUrl(self,url):
        #url = str(self.get_argument("url"))
        #ur = url
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        name = soup.find(class_="c-product__title")
        if name:
            image = str(soup.find(class_="c-gallery__img"))
            img = re.search("https://(.*?)/?.jpg",image)
            prud = soup.find(class_="c-product__params js-is-expandable")
            tit = []
            for string in prud.strings:
                tit.append(string)
            price = soup.find(class_="c-product__seller-price-real")

            hi = ("hi this is fake comment","thiss is secend comment")
            i = {"name": name.text.strip(), "image":img.group(),
                "price": price.text.strip(), "tit":tit,"hi":hi}
            return i
            #self.render("comment.html", message=params)

    # select to database
    def DigikalaSelect(self,sql,urlName):
        #url = str(self.get_argument("url"))
        #sql = "SELECT `url`, `id` FROM `url` WHERE `url` = %s "
        test = db.connectdb()
        mycursor = test.cursor()
        mycursor.execute(sql,(urlName, ))
        myresult = mycursor.fetchall()
        return myresult

    def  DigikalaInsert(self):
        url = self.get_argument("url")
        i = searchUrl.DigikalaUrl(self)
        name = i ["name"]
        #print (url , "" ,name)
        sql = "INSERT INTO `url`(`url`,`urlName`) VALUES (%s , %s)"
        test = db.connectdb()
        mycursor = test.cursor()
        val = (url,name)
        mycursor.execute(sql, val)
        test.commit()
        return
    
        # update to database
    def DigikalaUpdate(self,sql,url,url_id):
        #url = str(self.get_argument("url"))
        ur = url
        print(url_id)
        test = db.connectdb()
        mycursor = test.cursor()
        mycursor.execute(sql,(url ,url_id, ))
        #myresult = mycursor.fetchall()
        test.commit()
        return 
                
class InsertComment(BaseHandler):
    def get(self):
        #print(url)
        #i = searchUrl.DigikalaUrl(self)
        self.render("comment.html", message= i)
        pass 
    def post(self):
        #print(url)
        i = searchUrl.DigikalaUrl(self,url)
        comment = self.get_argument("commentbox")       
        print(comment)
        urlName= i["name"]
        print(urlName)
        sql = "SELECT `id` FROM `url` WHERE `urlName` = %s "
        selectId = searchUrl.DigikalaSelect(self,sql,urlName)
        for x in selectId :
           Id = x[0]
           print (Id)
        sql = "INSERT INTO `comment` (`comment`, `id`) VALUES ( %s, %s )"
        test = db.connectdb()
        mycursor = test.cursor()
        val = (comment,Id)
        mycursor.execute(sql, val)
        test.commit()
        i = searchUrl.DigikalaUrl(self,url)
        self.render("comment.html", message= i)
    

class MainHandler(BaseHandler):
    def get(self):
        self.render("url.html",error='')
    def post(self):
        global url
        url = str(self.get_argument("url"))
        # update find  url 
        if "https://www.digikala.com/" in url:
            i = searchUrl.DigikalaUrl(self, url)
            urlName = i ["name"]
            if urlName:
                sql = "SELECT `url`, `id` ,`urlName` FROM `url` WHERE `urlName` = %s "
                myresult = searchUrl.DigikalaSelect(self , sql, urlName)
                print (myresult)
                if  not myresult:
                        searchUrl.DigikalaInsert(self)
                        i = searchUrl.DigikalaUrl(self)
                        self.render("comment.html", message=i)
                        print("i am inser name")
                elif  myresult:        
                    for row in myresult:
                        if row[2] == urlName:
                            self.render("comment.html", message=i)
                            url_id = row[1]
                            sql = "UPDATE `url` SET `url` = %s  WHERE `url`.`id` = %s ;"
                            searchUrl.DigikalaUpdate(self, sql , url , url_id)
                            print(" i am update")
                    return
        
        #find  fast search modual
        
        else:
            print ("hii search")
            sealink=[]
            seadec=[]
            search_results = google.search(url, 3)
            for result in search_results:
                    #print(result.link)
                sealink.append(str(result.link))
                seadec.append(str(result.description))

            sea = {"link":sealink , "dec":seadec}
            self.render("search.html", message=(sea))
        #else:

#self.render("url.html", error="please enter anything!")

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/comment", InsertComment),
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
