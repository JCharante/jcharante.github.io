FROM python:3.8

ARG APP_USER=appuser

RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

RUN mkdir webapp

ADD requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ webapp/

WORKDIR /webapp

USER ${APP_USER}:${APP_USER}

EXPOSE 3401

CMD ["gunicorn", "-b 0.0.0.0:3401", "-w 3", "app:app"]

