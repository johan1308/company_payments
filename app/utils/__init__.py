import os
from typing import Any, Union
from dotenv import load_dotenv
load_dotenv('.env')
#load_dotenv('/var/www/html/validator.movilpay.app/company_payments/.env')

def get_env(name: str, default: Any = None) -> str:

    """
    Obtener variable de entorno.
    :param name: Nombre de la variable de entorno.
    :param default: valor predeterminado si la variable de entorno no está configurada.  # noqa: E501
    :return: valor de la variable de entorno.
    """
    if name in os.environ:
        return os.environ[name]
    return default


def bool_from_str(value: str) -> Union[bool, None]:
    """
    Convertir string a boolean.
    :param value: string a convertir.
    :return: valor booleano.
    """
    if value is None:
        return None
    if value.lower() in ['true', '1', 'yes', 'y', 't', 'True']:
        return True
    elif value.lower() in ['false', '0', 'no', 'n', 'f', 'False']:
        return False
    return None
