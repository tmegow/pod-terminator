FROM python:3.5-slim

RUN pip install --upgrade pip
RUN printf "kubernetes\npyyaml\n" >> /requirements.txt

COPY pod_terminator.py /
COPY timer_threads.py /

RUN apt-get update && \
    apt-get install -y gcc && \
    pip3 install -r requirements.txt --upgrade && \
    apt-get remove -y gcc && \
    apt-get autoremove -y

ENTRYPOINT ["python", "/pod_terminator.py"]
