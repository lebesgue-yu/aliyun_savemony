FROM python:3.8

WORKDIR /apps

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./aliyun_savemoney .

CMD [ "python", "./manager.py" ]
