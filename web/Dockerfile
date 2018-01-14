FROM python:3.4
EXPOSE 8000
COPY . /app
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python"]
CMD ["src/notes.py"]
