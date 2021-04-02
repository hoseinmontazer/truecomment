FROM python:3
workdir /app
COPY app .
#RUN apt-get update
#RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install requests
RUN pip3 install mysql.connector
RUN pip3 install pycurl
RUN pip3 install uuid
RUN pip3 install asyncio
RUN pip3 install tornado
RUN pip3 install google-search
RUN pip3 install googlesearch-python
RUN pip3 install pillow
RUN pip3 install claptcha
RUN pip3 install captcha
#RUN pip3 install opencv-python
#RUN pip3 install matplotlib
CMD [ "python3", "-u","./trueComment.py" ]
