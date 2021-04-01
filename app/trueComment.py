import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line
import os.path
import requests
from bs4 import BeautifulSoup
import re
from googleapi import google
import mysql.connector
import sys
from PIL import Image, ImageDraw, ImageFont
import random
import string
from PIL import Image
from claptcha import Claptcha
from captcha.image import ImageCaptcha
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import io
import time
import glob


define("port", default=8887, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")

url=""
urlName=""


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
        global url
        url= self.get_argument("url")
        return  url

class captchagenerator(BaseHandler):
    def gen_cap():
        n = random.randint(10000,99999)
        image = ImageCaptcha()

        data = image.generate(str(n))
        image.write(str(n), './static/captcha/'+str(n)+'.png')
        #print(n)
        return n

class searchUrl(BaseHandler):
    def get(self):
        n = captchagenerator.gen_cap()
        print("captcah is;",n)
        captcha = glob.glob('82822.png')
    def DigikalaUrl(self,url):
        
        truecomment=[]
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        name = soup.find(class_="c-product__title")
        #n = captchagenerator.gen_cap()
        #print("captcah is;",n)
        #captcha = Image.open('./static/captcha/'+str(n)+'.png')
        #captcha = cv2.imread('82822.png')
        #with open('./static/captcha/'+str(n)+'.png','wb', errors='ignore') as f:
        #    captcha = f.read()
        #print(type(captcha))
        captcha = glob.glob('82822.png')
        #print("captcha2 is:",captcha)
        if name:
            image = str(soup.find(class_="c-gallery__img"))
            img = re.search("https://(.*?)/?.jpg",image)
            prud = soup.find(class_="c-product__params js-is-expandable")
            tit = []
            for string in prud.strings:
                tit.append(string)
            price = soup.find(class_="c-product__seller-price-real")
            sql = ("SELECT `id` FROM `url` WHERE `urlName` = '%s' " %(name.text.strip()))
            selectId = searchUrl.DigikalaSelect(self,sql)
            for x in selectId :
                    Id = x[0]
            sql1 = ("SELECT `comment` FROM `comment` WHERE `id` = '%s'  " %(Id))
            SqlComment = searchUrl.DigikalaSelect(self,sql1)
            for c in SqlComment:
                truecomment.append(str(c[0]))
            i = {"name": name.text.strip(), "image":img.group(),
                "price": price.text.strip(), "tit":tit,"hi":truecomment,"captcha":captcha}
            print(i)
            return i

    # select to database
    def DigikalaSelect(self,sql):
        #url = str(self.get_argument("url"))
        test = db.connectdb()
        mycursor = test.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        return myresult

    def  DigikalaInsert(self):
        url = self.get_argument("url")
        i = searchUrl.DigikalaUrl(self,url)
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
        test = db.connectdb()
        mycursor = test.cursor()
        mycursor.execute(sql,(url ,url_id, ))
        #myresult = mycursor.fetchall()
        test.commit()
        return 

class InsertComment(BaseHandler):

    def get(self):
        comment=""
        email=""
        self.render("comment.html",error='', message= i)

    def post(self):
        global Id
        comment = self.get_argument("commentbox")
        email=  self.get_argument("email")
        forbiden_words=["سکس","زمین","خدا",]     
        i = searchUrl.DigikalaUrl(self,url)
        if  not comment:
            print ("comment is:",comment)
            self.render("comment.html",error="لطفانظر خود را وارد کنید" , message=i)
        elif not email:
            self.render("comment.html",error="لطفاایمیل خود را وارد کنید" , message=i)
        else:    
            for f in forbiden_words:
                if f in comment:
                    self.render("comment.html",error="شما از کلمه '%s' نمیتوانید در نظرات استغاده کنید" %(f) , message=i)
                    break
                else:

                    sql = ("SELECT `id` FROM `url` WHERE `urlName` = '%s' " %(urlName))
                    selectId = searchUrl.DigikalaSelect(self,sql)
                    for x in selectId :
                        Id = x[0]
                        print (Id)
                    sql = "INSERT INTO `comment` (`comment`, `id`, `email`) VALUES ( %s, %s, %s )"
                    test = db.connectdb()
                    mycursor = test.cursor()
                    val = (comment,Id,email)
                    mycursor.execute(sql, val)
                    test.commit()
                    i = searchUrl.DigikalaUrl(self,url)
                    #self.redirect("comment",message=i)
                    self.redirect("/")

                    return
class Contact(BaseHandler):
   
    def get(self):
        self.render("contact.html",error='')

    def post (self):
        self.render("contact.html")


class MainHandler(BaseHandler):
   
    def get(self):
        captcha = glob.glob('82822.png')
        self.render("url.html",error='')

    def post (self):
            global url
            global urlName
            url = str(self.get_argument("url"))
            # update find  url 
            if "https://www.digikala.com/" in url:
                i = searchUrl.DigikalaUrl(self, url)
                urlName = i ["name"]
                if urlName:
                    sql = ("SELECT `url`, `id` ,`urlName` FROM `url` WHERE `urlName` = '%s' " %(urlName))
                    myresult = searchUrl.DigikalaSelect(self , sql )
                    if  not myresult:
                            print("i am here")
                            searchUrl.DigikalaInsert(self)
                            i = searchUrl.DigikalaUrl(self,url)
                            self.render("comment.html", message=i)
                            print("i am insert name")
                    elif  myresult:
                        print("i am here!!!!")     
                        for row in myresult:
                            if row[2] == urlName:
                                self.render("comment.html", error='', message=i)
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
                print(sealink)
                sea = {"link":sealink , "dec":seadec}
                self.render("search.html", message=(sea))
           
            
def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/comment", InsertComment),
    (r"/contact",Contact),
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