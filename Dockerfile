# debian:latest codepad
FROM hub.c.163.com/library/debian:latest

MAINTAINER Hanaasagi <>

RUN echo "deb http://mirrors.163.com/debian jessie main non-free contrib" >/etc/apt/sources.list
RUN echo "deb-src http://mirrors.163.com/debian jessie main non-free contrib" >>/etc/apt/sources.list

RUN apt-get update && \
    apt-get install -y python \
                       python-dev \
                       python-pip  \
    && apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 

RUN mkdir -p /app
WORKDIR /app
CMD ["bash"]
