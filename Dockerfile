FROM python:buster

ADD rebrand.py /usr/local/bin/rebrand
RUN chmod +x /usr/local/bin/rebrand