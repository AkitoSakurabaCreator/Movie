#!/bin/sh
python ./src/manage.py makemigrations --noinput
python ./src/manage.py migrate --noinput
python ./src/manage.py createcachetable
python ./src/manage.py collectstatic --noinput
# 環境変数のDEBUGの値がTrueの時はrunserverを、Falseの時はgunicornを実行します
if [ $DEBUG = "True" ]
then
    python ./src/manage.py runserver 0.0.0.0:8000
else
    gunicorn ./src/mysite.wsgi:application --bind 0.0.0.0:8000
fi
