FROM python:3.11
COPY requirements.txt /opt/app/
RUN pip3 install -r /opt/app/requirements.txt
COPY parser.py /opt/app/
WORKDIR /opt/app/
CMD ["python", "parser.py"]