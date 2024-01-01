python3 manage.py migrate &&
  python3 manage.py compress &&
  python3 manage.py collectstatic --noinput &&
  uwsgi --socket :8000 --wsgi-file ahmadiwoodwork/wsgi.py