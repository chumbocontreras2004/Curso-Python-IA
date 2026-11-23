"""Módulo 3 - Práctica 3: librería de validación de datos.

El paquete agrupa las validaciones en tres módulos: ``texto``, ``numeros`` y
``fechas``. Este fichero reexporta las funciones más usadas.
"""

# TODO: reexporta aquí las funciones indicadas en el enunciado y define __all__
from .texto import esta_vacio, normalizar_nombre, es_dni, es_email
from .numeros import es_entero, es_decimal, a_decimal, en_rango
from .fechas import es_fecha, edad, es_mayor_de_edad, MAYORIA_DE_EDAD

__all__ = [
    "a_decimal",
    "edad",
    "en_rango",
    "es_decimal",
    "es_dni",
    "es_email",
    "es_entero",
    "es_fecha",
    "es_mayor_de_edad",
    "esta_vacio",
    "normalizar_nombre",
]

__version__ = "1.0.0"
