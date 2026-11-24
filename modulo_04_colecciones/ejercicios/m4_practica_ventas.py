"""Módulo 4 - Práctica 4: análisis de ventas en memoria.

Cada venta es un diccionario con las claves "fecha", "vendedor", "region",
"producto", "categoria", "unidades" y "precio". Ninguna función modifica la
lista de ventas que recibe.
"""

from m4_datos_ventas import VENTAS

ANCHO = 44


def importe(venta: dict) -> float:
    """Devuelve el importe de una venta: unidades por precio, con dos decimales.

    >>> importe({"unidades": 3, "precio": 19.9})
    59.7
    """
    return round(venta.get("unidades", 0) * venta.get("precio", 0.0), 2)


def total_ventas(ventas: list[dict]) -> float:
    """Devuelve la suma de los importes de todas las ventas, con dos decimales."""
    return round(sum(importe(venta) for venta in ventas), 2)


def filtrar_ventas(ventas: list[dict], *, region: str | None = None,
                   categoria: str | None = None, vendedor: str | None = None,
                   desde: str | None = None, hasta: str | None = None) -> list[dict]:
    """Devuelve las ventas que cumplen todos los criterios indicados.

    Un criterio que vale ``None`` no se aplica. ``desde`` y ``hasta`` son
    fechas ISO y las dos están incluidas en el intervalo.
    """
    return [venta for venta in ventas if (region is None or venta.get("region") == region) and
            (categoria is None or venta.get("categoria") == categoria) and
            (vendedor is None or venta.get("vendedor") == vendedor) and
            (desde is None or venta.get("fecha") >= desde) and
            (hasta is None or venta.get("fecha") <= hasta)]
    # Las fechas ISO se pueden comparar como texto: su orden alfabético
    # coincide con el cronológico.


def importe_por(ventas: list[dict], campo: str) -> dict[str, float]:
    """Agrupa las ventas por ``campo`` y devuelve el importe total de cada grupo.

    Los importes van redondeados a dos decimales.

    >>> importe_por([{"region": "Norte", "unidades": 2, "precio": 10.0}], "region")
    {'Norte': 20.0}
    """
    return {
        valor: round(
            sum(importe(venta) for venta in ventas if venta.get(campo) == valor), 2
        )
        for valor in {venta.get(campo) for venta in ventas}
    }


def unidades_por_producto(ventas: list[dict]) -> dict[str, int]:
    """Devuelve las unidades totales vendidas de cada producto."""
    return {
        producto: sum(
            venta.get("unidades", 0) for venta in ventas if venta.get("producto") == producto
        )
        for producto in {venta.get("producto") for venta in ventas}
    }


def ranking(ventas: list[dict], campo: str, cantidad: int = 3) -> list[tuple[str, float]]:
    """Devuelve los ``cantidad`` grupos con mayor importe, como tuplas (clave, importe).

    De mayor a menor importe. A igual importe, por orden alfabético de la clave.
    """
    return sorted(
        importe_por(ventas, campo).items(),
        key=lambda grupo: (-grupo[1], grupo[0]),
    )[:max(0, cantidad)]


def producto_mas_vendido(ventas: list[dict]) -> str | None:
    """Devuelve el producto con más unidades vendidas, o ``None`` si no hay ventas.

    En caso de empate, el primero por orden alfabético.
    """
    unidades = unidades_por_producto(ventas)
    return min(unidades, key=lambda producto: (-unidades[producto], producto), default=None)


def ticket_medio(ventas: list[dict]) -> float:
    """Devuelve el importe medio por venta, con dos decimales. Sin ventas, 0.0."""
    return round(total_ventas(ventas) / len(ventas), 2) if ventas else 0.0


def generar_informe(ventas: list[dict]) -> str:
    """Devuelve el informe de ventas como texto, con el formato del enunciado."""
    resumen = [
        ("Ventas registradas", f"{len(ventas):,}"),
        ("Importe total", f"{total_ventas(ventas):,.2f}"),
        ("Ticket medio", f"{ticket_medio(ventas):,.2f}"),
        ("Producto más vendido", producto_mas_vendido(ventas) or "-"),
    ]

    lineas = [
        "=" * ANCHO,
        "INFORME DE VENTAS".center(ANCHO),
        "=" * ANCHO,
        *(f"{etiqueta:<30}{valor:>14}" for etiqueta, valor in resumen),
        "-" * ANCHO,
    ]
    for titulo, campo in (
        ("Por región", "region"),
        ("Por categoría", "categoria"),
        ("Por vendedor", "vendedor"),
    ):
        lineas.append(titulo)
        lineas.extend(
            f"  {clave:<28}{valor:>14,.2f}"
            for clave, valor in ranking(ventas, campo, len(importe_por(ventas, campo)))
        )
        lineas.append("-" * ANCHO)
    lineas[-1] = "=" * ANCHO
    return "\n".join(lineas)

def main():
    print(generar_informe(VENTAS))
    print()
    print("Solo la región Sur, segunda quincena:")
    print(generar_informe(filtrar_ventas(VENTAS, region="Sur", desde="2026-10-16")))


if __name__ == "__main__":
    main()
