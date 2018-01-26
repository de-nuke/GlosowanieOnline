FROM python:3.4
EXPOSE 8000
RUN mkdir /app
VOLUME /app
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install pyOpenSSL
COPY . /app
WORKDIR /app
#COPY requirements.txt .
RUN echo nameserver 10.30.0.133 >> /etc/resolv.conf && pip3 install -r requirements.txt
CMD ["python", "src/myapp.py"]
