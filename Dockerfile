FROM python:3.12.11-slim-trixie

# Installs packages needed to build C-extensions
RUN apt-get update && apt-get install -y build-essential

RUN mkdir /web

WORKDIR /root

COPY requirements.txt /web/requirements.txt
RUN python -m pip install -r /web/requirements.txt --no-cache-dir

WORKDIR /web

COPY . /web

ENV PORT 5000

EXPOSE ${PORT}

COPY start.sh /web/start.sh

RUN chmod +x /web/start.sh

CMD ["/web/start.sh"]