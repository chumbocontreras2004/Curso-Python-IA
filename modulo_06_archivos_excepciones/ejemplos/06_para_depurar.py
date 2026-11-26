"""Módulo 6 - Ejemplo 6: un programa con tres errores para practicar con el depurador.

El programa debería imprimir:

    Ventas leídas: 20
    Importe total: 21686.80
    Mejor vendedor: Ada (7435.30)

No corrijas a ojo. Para cada error:

1. Ejecuta con F5 y lee la traza o el resultado incorrecto.
2. Pon un punto de ruptura (F9) donde creas que empieza el problema.
3. Avanza con F10 y F11 mirando el panel de variables.
4. Corrige y vuelve a ejecutar.

Las soluciones están comentadas en el guion del profesor.
"""

import csv
from pathlib import Path

RUTA = Path(__file__).parent.parent / "datos" / "ventas.csv"


def leer_ventas(ruta):
    with open(ruta, encoding="utf-8", newline="") as fichero:
        return list(csv.DictReader(fichero))


def importe(venta):
    unidades = int(venta["unidades"])
    precio = float(venta["precio"])
    return unidades * precio


def total(ventas):
    suma = 0
    for venta in ventas:
        suma += importe(venta)
    return suma


def mejor_vendedor(ventas):
    por_vendedor = {}
    for venta in ventas:
        nombre = venta["vendedor"]
        por_vendedor[nombre] = por_vendedor.get(nombre, 0) + importe(venta)
    nombre = max(por_vendedor, key=por_vendedor.get)
    return nombre, por_vendedor[nombre]


def main():
    ventas = leer_ventas(RUTA)
    print(f"Ventas leídas: {len(ventas)}")
    print(f"Importe total: {total(ventas):.2f}")
    nombre, vendido = mejor_vendedor(ventas)
    print(f"Mejor vendedor: {nombre} ({vendido:.2f})")


if __name__ == "__main__":
    main()
