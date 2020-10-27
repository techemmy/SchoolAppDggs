web: gunicorn app:app
init: python manage.py db.create_all()
migrate: python manage.py db migrate
upgrade: python manage.py db upgrade