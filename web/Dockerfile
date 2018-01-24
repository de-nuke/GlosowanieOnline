FROM python:3.4
EXPOSE 8000
RUN mkdir /app
VOLUME /app
COPY . /app
WORKDIR /app
COPY requirements.txt .
RUN echo nameserver 10.30.0.133 >> /etc/resolv.conf && pip3 install -r requirements.txt
#ENTRYPOINT ["python"]
CMD ["python", "src/myapp.py"]
