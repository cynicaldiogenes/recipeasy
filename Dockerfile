FROM python:3.8.13-slim

RUN useradd recipeasy

WORKDIR /home/recipeasy

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql cryptography

COPY app app
COPY migrations migrations
COPY recipeasy.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP recipeasy.py

RUN chown -R recipeasy:recipeasy ./
USER recipeasy

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]