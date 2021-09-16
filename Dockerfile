FROM python:3.7
COPY .  /myapp
WORKDIR /myapp
RUN pip install -r requirements.txt
EXPOSE  9000
CMD ["python", "bookmanager.py"]
