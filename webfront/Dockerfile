FROM ubuntu:latest
MAINTAINER Rajdeep Dua "dua_rajdeep@yahoo.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN pip install --upgrade pip
RUN pip install pyOpenSSL
COPY requirements.txt /app/requirements.txt
COPY . /app
WORKDIR /app
RUN echo nameserver 10.30.0.133 >> /etc/resolv.conf && pip install -r requirements.txt
WORKDIR /app/src
ENTRYPOINT ["python"]
CMD ["onlinevotingclient.py"]
