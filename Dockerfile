FROM python:3.8-buster

ADD rebrand_lib.py /usr/local/bin/rebrand_lib.py

ADD rebrand.py /usr/local/bin/rebrand
RUN chmod +x /usr/local/bin/rebrand

ADD rebrand_nault.py /usr/local/bin/rebrand-nault
RUN chmod +x /usr/local/bin/rebrand-nault

ADD rebrand_ninja.py /usr/local/bin/rebrand-ninja
RUN chmod +x /usr/local/bin/rebrand-ninja

ADD rebrand_boompow.py /usr/local/bin/rebrand_boompow
RUN chmod +x /usr/local/bin/rebrand_boompow

ADD asset/xno-symbol-blank.svg /opt/asset/xno-symbol-blank.svg