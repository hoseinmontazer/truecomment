FROM python:3
ADD trueComment.py /
ADD templates/ /templates
ADD static/ /static
RUN pip3 install requests
RUN pip3 install mysql.connector
RUN pip3 install pycurl
RUN pip3 install uuid
RUN pip3 install asyncio
RUN pip3 install tornado
RUN pip3 install git+https://github.com/abenassi/Google-Search-API
CMD [ "python3", "-u","./trueComment.py" ]
