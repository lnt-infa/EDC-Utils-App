FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY edcUtils .
EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0:8000" ]
