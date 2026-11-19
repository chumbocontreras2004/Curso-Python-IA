"""Módulo 1 - Ejercicio 1: saludo."""


def saludar(nombre):
    """Devuelve un saludo de bienvenida para ``nombre``.

    El nombre se limpia de espacios sobrantes y se escribe con la inicial de
    cada palabra en mayúscula. Si queda vacío, se saluda a "Anónimo".

    print(f"Hola, {nombre}. ¡Te damos la bienvenida al curso!")
    >>> saludar("  ada lovelace ")
    'Hola, Ada Lovelace. ¡Te damos la bienvenida al curso!'
    """
    return f"Hola, {nombre.strip().title() or 'Anónimo'}. ¡Te damos la bienvenida al curso!"


def main():
    """Pide el nombre por teclado e imprime el saludo."""
    nombre = input("¿Cómo te llamas? ")
    print(saludar(nombre))


if __name__ == "__main__":
    main()
