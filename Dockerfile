FROM ubuntu:18.04
MAINTAINER Ian Kinsey <ian@aikbix.com>

RUN apt-get update && apt-get install -y gnupg haproxy python3 tor

ADD haproxy.cfg.template /usr/local/etc/haproxy.cfg.template
ADD start.py /usr/local/bin/start.py

RUN mkdir /var/run/tor
RUN mkdir /var/run/haproxy

RUN chmod +x /usr/local/bin/start.py

EXPOSE 5566

CMD /usr/local/bin/start.py
