FROM python:3.8-buster

ADD rebrand.py /usr/local/bin/rebrand
RUN chmod +x /usr/local/bin/rebrand

ADD rebrand_nault.py /usr/local/bin/rebrand-nault
RUN chmod +x /usr/local/bin/rebrand-nault