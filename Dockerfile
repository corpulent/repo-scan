FROM python:3.8
FROM shiftleft/scan

WORKDIR /srv/src

COPY ./requirements.txt /srv/requirements.txt
RUN pip install -r /srv/requirements.txt

COPY ./main.py /srv/main.py
COPY ./reposcan/* /srv/reposcan/

RUN chmod -R +x /srv/main.py
RUN chmod -R +x /srv/reposcan/
