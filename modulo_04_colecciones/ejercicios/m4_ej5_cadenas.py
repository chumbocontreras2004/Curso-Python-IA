"""Módulo 4 - Ejercicio 5: manipulación de cadenas."""

VOCALES = "aeiouáéíóúü"


def es_palindromo(texto: str) -> bool:
    """Indica si el texto se lee igual en los dos sentidos.

    No tiene en cuenta mayúsculas, espacios ni signos de puntuación: solo se
    comparan las letras y los dígitos.

    >>> es_palindromo("Anita lava la tina")
    True
    >>> es_palindromo("Python")
    False
    """
    return (texto := "".join(c.lower() for c in texto if c.isalnum())) == texto[::-1]


def contar_vocales(texto: str) -> int:
    """Cuenta las vocales del texto, con o sin tilde, mayúsculas o minúsculas.

    >>> contar_vocales("Programación")
    5
    """
    return sum(1 for c in texto.lower() if c in VOCALES)


def invertir_palabras(frase: str) -> str:
    """Devuelve la frase con las palabras en orden inverso y un solo espacio entre ellas.

    >>> invertir_palabras("  hola   mundo cruel ")
    'cruel mundo hola'
    """
    return " ".join(frase.split()[::-1])


def a_snake_case(texto: str) -> str:
    """Convierte un texto con palabras separadas por espacios o guiones en snake_case.

    >>> a_snake_case("Fecha de Alta")
    'fecha_de_alta'
    >>> a_snake_case("  codigo-postal ")
    'codigo_postal'
    """
    return "_".join(texto.replace("-", " ").strip().lower().split())


def enmascarar(numero: str, visibles: int = 4) -> str:
    """Sustituye por asteriscos todos los caracteres salvo los últimos ``visibles``.

    Si el texto no es más largo que ``visibles``, se devuelve tal cual.

    >>> enmascarar("4532123456789012")
    '************9012'
    >>> enmascarar("123")
    '123'
    """
    visibles = max(0, visibles)
    return "*" * max(0, len(numero) - visibles) + (numero[-visibles:] if visibles else "")
    # Cuidado con numero[-visibles:]: si visibles es 0, numero[-0:] es la cadena entera


def son_anagramas(a: str, b: str) -> bool:
    """Indica si las dos palabras tienen las mismas letras en distinto orden.

    No distingue mayúsculas de minúsculas ni tiene en cuenta los espacios.

    >>> son_anagramas("Roma", "amor")
    True
    """
    return sorted(c.lower() for c in a if not c.isspace()) == sorted(
        c.lower() for c in b if not c.isspace()
    )


def parsear_configuracion(texto: str) -> dict[str, str]:
    """Convierte un texto ``clave=valor;clave=valor`` en un diccionario.

    Quita los espacios alrededor de claves y valores, ignora los fragmentos
    vacíos y los que no tienen signo igual. Si un valor contiene más signos
    igual, se conservan.

    >>> parsear_configuracion("host = localhost; puerto=8080;; modo=debug")
    {'host': 'localhost', 'puerto': '8080', 'modo': 'debug'}
    """
    return {
        clave.strip(): valor.strip()
        for fragmento in texto.split(";")
        if "=" in fragmento
        for clave, valor in [fragmento.split("=", 1)]
    }


def formatear_tabla(filas: list[tuple[str, float]]) -> str:
    """Devuelve una tabla de texto con una línea por fila.

    El nombre se alinea a la izquierda en 12 caracteres y el importe a la
    derecha en 10, con dos decimales. Las líneas se separan con saltos de
    línea, sin salto al final.

    >>> print(formatear_tabla([("teclado", 45), ("monitor", 189.5)]))
    teclado          45.00
    monitor         189.50
    """
    return "\n".join(f"{nombre:<12}{importe:>10.2f}" for nombre, importe in filas)
