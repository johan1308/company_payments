"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

import sys 

# Agrega la ruta del proyecto Django al PYTHONPATH
project_path = "/var/www/html/validator.movilpay.app/company_payments"
sys.path.append(project_path)
sys.path.append("/var/www/html/validator.movilpay.app/company_payments/config")

from django.core.wsgi import get_wsgi_application

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

application = get_wsgi_application()
