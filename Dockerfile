FROM python:3.9.6-buster

RUN apt-get update -y && \
    pip install pipenv==2022.10.12 --no-cache-dir && \
    git clone https://github.com/cyfronet-fid/oms-adapter-jira.git && \
    cd oms-adapter-jira && \
    pipenv install --system && \
    cd oms_jira/services && \
    sed -i "s|first_name: str| # first_name: str|g" mp.py && \
    sed -i "s|last_name: str| # last_name: str|g" mp.py && \
    sed -i "s|voucher_id: int| # voucher_id: int|g" mp.py && \
    sed -i "s|timestamp = datetime.datetime|timestamp: datetime.datetime|g" mp.py &&\
    sed -i "s|params = dict(oms_id=self.oms_id, from_timestamp=from_timestamp.isoformat())|params = dict(oms_id=self.oms_id, from_timestamp=from_timestamp.isoformat() + 'Z')|g" mp.py &&\
    sed -i "s|country: str|country: Optional[str]|g" mp.py

ENV PYTHONPATH "${PYTHONPATH}:/oms-adapter-jira"

COPY . /src

WORKDIR /src

RUN pip install -r requirements/requirements.txt --no-cache-dir && \
    touch src/last_timestamp.txt && \
    pip install flask-restx

ENTRYPOINT [ "python3" ]

CMD [ "/src/src/app.py" ]
