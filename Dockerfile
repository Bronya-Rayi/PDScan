FROM ubuntu:22.04
ENV DEBIAN_FRONTEND noninteractive 

RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
&& sed -i s/security.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list \
&& apt-get clean \
&& apt update \
&& apt install -y wget zip curl wget python3 python3-pip nginx libpcap-dev redis-server -y 

ADD worker/tools/chrome/google-chrome-stable_current_amd64.deb /tmp/google-chrome-stable_current_amd64.deb
ADD worker/tools/chrome/chromedriver_linux64.zip /tmp/chromedriver_linux64.zip
RUN dpkg -i /tmp/google-chrome-stable_current_amd64.deb || apt install -fy || dpkg -i /tmp/google-chrome-stable_current_amd64.deb
RUN unzip /tmp/chromedriver_linux64.zip -d /tmp \
&& mv /tmp/chromedriver /usr/bin/chromedriver \
&& chmod +x /usr/bin/chromedriver

RUN mkdir /app && mkdir /app/PDScan
ADD ./requirements.txt /app/PDScan/requirements.txt
RUN pip3 install -r /app/PDScan/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
ADD . /app/PDScan
RUN chmod -R 777 /app/PDScan
RUN chmod +x /app/PDScan/run.sh
RUN mv /app/PDScan/web/nginx/default /etc/nginx/sites-enabled/default
WORKDIR /app/PDScan

EXPOSE 8443

ENTRYPOINT ["sh", "run.sh"]
