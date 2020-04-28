FROM python:3.7
MAINTAINER Christian
ADD ofo/ /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD exec python3 manage.py runserver 0.0.0.0:8000