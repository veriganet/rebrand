FROM python:3.8-buster

ADD rebrand_lib.py /usr/local/bin/rebrand_lib.py

ADD rebrand.py /usr/local/bin/rebrand
RUN chmod +x /usr/local/bin/rebrand

ADD rebrand_nault.py /usr/local/bin/rebrand-nault
RUN chmod +x /usr/local/bin/rebrand-nault

ADD rebrand_nanocurrency_js.py /usr/local/bin/rebrand-nanocurrency-js
RUN chmod +x /usr/local/bin/rebrand-nanocurrency-js