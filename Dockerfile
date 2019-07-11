FROM python:3.7

WORKDIR /src
ADD . /src

RUN pip install -r requirements.txt --upgrade

CMD [ "python3", "termify.py" ]
