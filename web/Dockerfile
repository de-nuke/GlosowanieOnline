FROM python:3.4
EXPOSE 8000
RUN mkdir /app
VOLUME /app
COPY . /app
WORKDIR /app
COPY requirements.txt .
RUN echo nameserver 10.30.0.132 >> /etc/resolv.conf && pip3 install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python"]
CMD ["src/notes.py"]
