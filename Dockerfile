FROM python:3
ADD trueComment.py /
ADD templates/ /templates
RUN pip3 install requests
RUN pip3 install mysql.connector
RUN pip3 install pycurl
RUN pip3 install uuid
RUN pip3 install asyncio
RUN pip3 install tornado
CMD [ "python3", "./trueComment.py" ]
