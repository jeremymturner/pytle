#FROM python:3
FROM alpine:latest
RUN apk add --no-cache python3 gcc python3-dev musl-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

#ADD [".", "/tmp/codeenv"]
#RUN pip install  /tmp/codeenv/dist/*.tar.gz

# RUN python3 -m pip install --index-url https://test.pypi.org/simple/ pytle

RUN python3 -m pip install pytle
ENTRYPOINT ["pytle"]

# OLD
# RUN pip install -r /tmp/codeenv/requirements.txt
# RUN python setup.py install
# ENTRYPOINT ["python", "/tmp/codeenv/pytle/cli.py"]
