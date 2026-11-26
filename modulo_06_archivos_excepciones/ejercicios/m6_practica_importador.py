"""Módulo 6 - Práctica 6: importador de ventas en CSV.

Lee un CSV de ventas, valida cada fila, registra las que no valen y exporta
un resumen por región.
"""

import csv
import logging
import math
from datetime import date
from pathlib import Path

logger = logging.getLogger(__name__)

CAMPOS = ["fecha", "vendedor", "region", "producto", "categoria", "unidades", "precio"]
CAMPOS_RESUMEN = ["region", "ventas", "unidades", "importe"]


class ErrorDeImportacion(Exception):
    pass


class FicheroNoValido(ErrorDeImportacion):
    pass


class FilaNoValida(ErrorDeImportacion):
    pass


def validar_fila(fila: dict) -> dict:
    """Devuelve la venta de una fila con los tipos convertidos.

    Recibe un diccionario de cadenas y devuelve uno NUEVO con los mismos
    campos sin espacios alrededor, ``unidades`` como ``int`` y ``precio``
    como ``float``. Lanza ``FilaNoValida`` con uno de estos mensajes,
    comprobados en este orden:

    - "falta el campo <nombre>" si algún campo de ``CAMPOS`` está vacío
    - "fecha no válida: <valor>" si la fecha no es una fecha ISO
    - "unidades no válidas: <valor>" si no es un entero mayor que cero
    - "precio no válido: <valor>" si no es un número mayor que cero
    """
    limpia = {}
    for campo in CAMPOS:
        valor = fila.get(campo)
        if valor is None:
            limpia[campo] = ""
        else:
            limpia[campo] = str(valor).strip()

        if not limpia[campo]:
            raise FilaNoValida(f"falta el campo {campo}")

    fecha = limpia["fecha"]
    try:
        fecha_convertida = date.fromisoformat(fecha)
        if fecha_convertida.isoformat() != fecha:
            raise ValueError
    except ValueError:
        raise FilaNoValida(f"fecha no válida: {fecha}")

    unidades_texto = limpia["unidades"]
    try:
        unidades = int(unidades_texto)
        if unidades <= 0:
            raise ValueError
    except ValueError:
        raise FilaNoValida(f"unidades no válidas: {unidades_texto}")

    precio_texto = limpia["precio"]
    try:
        precio = float(precio_texto)
        if not math.isfinite(precio) or precio <= 0:
            raise ValueError
    except (TypeError, ValueError):
        raise FilaNoValida(f"precio no válido: {precio_texto}")

    limpia["unidades"] = unidades
    limpia["precio"] = precio
    return limpia


def importar_ventas(ruta) -> tuple[list[dict], list[str]]:
    """Lee el CSV y devuelve una tupla (ventas válidas, errores).

    Cada error es un texto "Línea N: motivo", donde N es el número de línea
    en el fichero (la cabecera es la línea 1) y el motivo es el mensaje de
    ``FilaNoValida``. Por cada fila descartada se registra además un aviso
    con ``logger.warning``.

    Lanza ``FicheroNoValido``:

    - "No existe el fichero <ruta>" si no se encuentra, encadenada con el
      ``FileNotFoundError`` original
    - "Faltan columnas: <nombres separados por coma y espacio>" si a la
      cabecera le falta alguna de ``CAMPOS``, en el orden de ``CAMPOS``
    """
    ruta = Path(ruta)
    try:
        fichero = open(ruta, encoding="utf-8", newline="")
    except FileNotFoundError as error:
        raise FicheroNoValido(f"No existe el fichero {ruta}") from error

    with fichero:
        lector = csv.DictReader(fichero)
        cabecera = lector.fieldnames or []
        faltan = [campo for campo in CAMPOS if campo not in cabecera]
        if faltan:
            raise FicheroNoValido(
                f"Faltan columnas: {', '.join(faltan)}"
            )

        ventas = []
        errores = []
        for numero_linea, fila in enumerate(lector, start=2):
            try:
                ventas.append(validar_fila(fila))
            except FilaNoValida as error:
                mensaje = f"Línea {numero_linea}: {error}"
                errores.append(mensaje)
                logger.warning("Línea %d: %s", numero_linea, error)

    return ventas, errores


def resumen_por_region(ventas: list[dict]) -> list[dict]:
    """Agrupa las ventas por región.

    Devuelve una lista de diccionarios con las claves de ``CAMPOS_RESUMEN``:
    la región, el número de ventas, las unidades totales y el importe total
    con dos decimales. Ordenada de mayor a menor importe.
    """
    resumen = {}
    for venta in ventas:
        region = venta["region"]
        if region not in resumen:
            resumen[region] = {
                "region": region,
                "ventas": 0,
                "unidades": 0,
                "importe": 0.0,
            }
        resumen[region]["ventas"] += 1
        resumen[region]["unidades"] += venta["unidades"]
        resumen[region]["importe"] += venta["unidades"] * venta["precio"]

    filas = list(resumen.values())
    for fila in filas:
        fila["importe"] = round(fila["importe"], 2)
    filas.sort(key=lambda fila: fila["importe"], reverse=True)
    return filas


def exportar_resumen(ruta, ventas: list[dict]) -> None:
    """Escribe en un CSV el resumen por región, con la cabecera ``CAMPOS_RESUMEN``."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="") as fichero:
        escritor = csv.DictWriter(
            fichero, fieldnames=CAMPOS_RESUMEN, extrasaction="ignore"
        )
        escritor.writeheader()
        escritor.writerows(resumen_por_region(ventas))


def escribir_errores(ruta, errores: list[str]) -> None:
    """Escribe los errores en un fichero de texto, uno por línea."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as fichero:
        for error in errores:
            fichero.write(f"{error}\n")


def procesar(entrada, carpeta_salida) -> dict:
    """Importa el fichero y deja los resultados en la carpeta de salida.

    Crea la carpeta si no existe y escribe en ella ``resumen.csv`` y
    ``errores.txt``. Registra con ``logger.info`` un mensaje final con las
    cantidades. Devuelve un diccionario con las claves "leidas", "validas"
    y "descartadas".

    Si el fichero de entrada no vale, ``FicheroNoValido`` sube sin capturar
    y no se escribe nada.
    """
    ventas, errores = importar_ventas(entrada)
    carpeta_salida = Path(carpeta_salida)
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    exportar_resumen(carpeta_salida / "resumen.csv", ventas)
    escribir_errores(carpeta_salida / "errores.txt", errores)

    leidas = len(ventas) + len(errores)
    cantidades = {
        "leidas": leidas,
        "validas": len(ventas),
        "descartadas": len(errores),
    }
    logger.info(
        "Importación completada: %d válidas y %d descartadas",
        cantidades["validas"],
        cantidades["descartadas"],
    )
    return cantidades


def main(argumentos: list[str] | None = None) -> int:
    """Punto de entrada. Se entrega hecho: es el único sitio donde se capturan
    los errores del importador y donde se configura el logging.

    Uso: python m6_practica_importador.py [entrada.csv] [carpeta_salida]
    """
    import sys

    argumentos = sys.argv[1:] if argumentos is None else argumentos
    datos = Path(__file__).parent.parent / "datos"
    entrada = argumentos[0] if argumentos else datos / "ventas_con_errores.csv"
    salida = argumentos[1] if len(argumentos) > 1 else Path("salida_practica_6")

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        cantidades = procesar(entrada, salida)
    except ErrorDeImportacion as error:
        logger.error("No se ha podido importar: %s", error)
        return 1
    print(f"Leídas {cantidades['leidas']} filas: {cantidades['validas']} válidas "
          f"y {cantidades['descartadas']} descartadas. Resultados en {salida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
