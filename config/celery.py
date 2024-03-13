import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
CELERYD_LOG_LEVEL = 'INFO'


# instanciando celery
app = Celery(
    'config', 
    broker='pyamqp://guest@localhost//',
    include=['app.tasks']
)


# las tareas en Celery se limpien automáticamente después de un período de tiempo específico 
# para evitar el almacenamiento excesivo de resultados no utilizados.
app.conf.update(
    result_expires=3600 * 12,
    broker_connection_retry_on_startup=True,  # Habilitar reintentos de conexión con el broker durante el inicio

)


# app: se refiere a la instancia de Celery que se ha creado.
# config_from_object: es un método de la instancia de Celery que se utiliza para cargar la configuración desde un objeto Python.
# 'django.conf:settings': especifica el objeto donde se cargará la configuración. En este caso: settings.py
# namespace='CELERY': llamar las configuraciones de celery en el settings.py con el prefijo CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# busca automáticamente las tareas definidas en los modulos de APPS
app.autodiscover_tasks()


app.conf.update(
    task_routes = {
        'app.tasks.add': {'queue': 'facturacion'},
    },
)