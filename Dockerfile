FROM python:3.10.7

WORKDIR /source

COPY requirements.txt /source/

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /source/

EXPOSE 8000

CMD ["gunicorn", "config.wsgi", ":8000"]