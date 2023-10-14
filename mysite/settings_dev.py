from pathlib import Path


DEBUG = True
SECRET_KEY = '1'
ALLOWED_HOSTS = ['127.0.0.1', 'localhost','project-a-15-django-3d66f46ae005.herokuapp.com/']
BASE_DIR = Path(__file__).resolve().parent.parent
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }