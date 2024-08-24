import os
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LostNFound.settings')

application = get_wsgi_application()

# Run collectstatic during deployment
execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])

app = application