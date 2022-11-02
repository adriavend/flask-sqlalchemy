FROM python:3.10.8

RUN pip install --upgrade pip setuptools

ADD . /code

WORKDIR /code

RUN pip install -r requirements.txt

# CMD python main.py

ENTRYPOINT ["python"]

CMD ["main.py"]
