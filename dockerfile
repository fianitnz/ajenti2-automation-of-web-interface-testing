FROM ubuntu:rolling
MAINTAINER fianitnz

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install software-properties-common -y && \
    add-apt-repository universe && \
    apt-get update && \
    apt-get upgrade -y

RUN apt-get install build-essential \
                    python3-pip \
                    python3-dev \
                    python3-lxml \
                    libssl-dev \
                    python3-dbus \
                    python3-augeas \
                    python3-apt \
                    ntpdate -y

RUN pip3 install setuptools \
                 pip \
                 wheel -U

#minimal install
#RUN pip3 install ajenti-panel \
#                  ajenti.plugin.core \
#                  ajenti.plugin.dashboard \
#                  ajenti.plugin.settings \
#                  ajenti.plugin.plugins

#with all plugins
RUN pip3 install ajenti-panel \
                 ajenti.plugin.ace \
                 ajenti.plugin.augeas \
                 ajenti.plugin.auth-users \
                 ajenti.plugin.core \
                 ajenti.plugin.dashboard \
                 ajenti.plugin.datetime \
                 ajenti.plugin.filemanager \
                 ajenti.plugin.filesystem \
                 ajenti.plugin.network \
                 ajenti.plugin.notepad \
                 ajenti.plugin.packages \
                 ajenti.plugin.passwd \
                 ajenti.plugin.plugins \
                 ajenti.plugin.power \
                 ajenti.plugin.services \
                 ajenti.plugin.settings \
                 ajenti.plugin.terminal

EXPOSE 8000/tcp
