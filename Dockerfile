FROM ubuntu:20.04

ADD requirements.txt /tmp/requirements.txt

RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
&& sed -i s/security.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list \
&& apt-get clean \
&& apt update \
&& apt install -y wget zip curl wget python3 python3-pip  \
&& pip3 install -r /tmp/requirements.txt 

ENV DEBIAN_FRONTEND noninteractive 

ADD tools/chrome/google-chrome-stable_current_amd64.deb /tmp/google-chrome-stable_current_amd64.deb
ADD tools/chrome/chromedriver_linux64.zip /tmp/chromedriver_linux64.zip
RUN dpkg -i /tmp/google-chrome-stable_current_amd64.deb || apt install -fy || dpkg -i /tmp/google-chrome-stable_current_amd64.deb
RUN unzip /tmp/chromedriver_linux64.zip -d /tmp \
&& mv /tmp/chromedriver /usr/bin/chromedriver \
&& chmod +x /usr/bin/chromedriver
RUN apt install libpcap-dev redis-server -y

RUN mkdir /app && mkdir /app/PDScan
ADD . /app/PDScan
RUN chmod -R 777 /app/PDScan
RUN chmod +x /app/PDScan/run.sh
WORKDIR /app/PDScan

EXPOSE 8888

ENTRYPOINT ["sh", "run.sh"]
