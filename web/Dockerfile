FROM python:3.4
EXPOSE 8000
VOLUME /usr/src/web/static
WORKDIR /usr/src/web
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY src .
CMD ["/usr/local/bin/gunicorn", "-w", "2", "-b", ":8000", "app:app"]
