FROM python:3.6

ENV PYTHONUNBUFFERED=1

RUN mkdir /var/log/cotizador

RUN chmod 777 /var/log/cotizador

RUN mkdir /cotizador

WORKDIR /cotizador

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .


