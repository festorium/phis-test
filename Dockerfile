FROM python:3.9

ENV ADMIN_SECRET_KEY="django-insecure-56qpm)0!+&klyv)ak0u%q8pb$@zlx_!pj8^=vq028*(d_4^-g^"

RUN apt update && apt install -y gcc libmariadb-dev-compat

RUN pip install gunicorn

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

CMD python manage.py migrate

EXPOSE 80/tcp