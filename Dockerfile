FROM ubuntu:18.04
MAINTAINER Ian Kinsey <ian@aikbix.com>

RUN apt-get update && apt-get install -y gnupg haproxy python3
RUN echo 'deb http://deb.torproject.org/torproject.org bionic main' | tee /etc/apt/sources.list.d/torproject.list
RUN gpg --keyserver keys.gnupg.net --recv 886DDD89
RUN gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | apt-key add -
RUN apt-get update && apt-get install -y tor
RUN update-rc.d -f tor remove

ADD haproxy.cfg.template /usr/local/etc/haproxy.cfg.template
ADD start.py /usr/local/bin/start.py

RUN mkdir /var/run/tor
RUN mkdir /var/run/haproxy

RUN chmod +x /usr/local/bin/start.py

EXPOSE 5566

CMD /usr/local/bin/start.py
