# Pull base image
FROM python:3.8

RUN apt update -y
RUN apt install -y wkhtmltopdf
RUN apt install -y locales-all
RUN apt install -y locales
RUN apt install -y libpq-dev
RUN localedef -c -i es_MX -f UTF-8 es_MX.UTF-8
RUN ln -sf /usr/share/zoneinfo/Mexico/General /etc/localtime

RUN apt clean

WORKDIR /
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /logs

COPY . .

RUN mkdir -p /files/cdc/xml/success
RUN mkdir -p /files/cdc/xml/fail
RUN mkdir -p /files/cdc/pdf

VOLUME [ "/files/" ]

EXPOSE 5000
CMD [ "gunicorn" ]
