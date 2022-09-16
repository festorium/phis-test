FROM python:3.9

ENV JWT_SECRET_KEY="QYmXTKt6bnzaFi76H7R88FQ"

ENV ADMIN_SECRET_KEY="django-insecure-56qpm0&klyvak0uq8pb@zlx_pj8^vq028d_4-"

RUN apt update && apt install -y gcc libmariadb-dev-compat

RUN pip install gunicorn

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

CMD python manage.py migrate

EXPOSE 80/tcp