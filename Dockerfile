FROM python:3.9

ENV JWT_SECRET_KEY="QYmXTKt6bnzaFi76H7R88FQ"

RUN apt update && apt install -y gcc libmariadb-dev-compat

RUN pip install --upgrade pip

RUN pip install gunicorn

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

CMD sleep 5

CMD python manage.py migrate

EXPOSE 80/tcp

ENTRYPOINT gunicorn -w 4 -b 0.0.0.0:80 admin.wsgi