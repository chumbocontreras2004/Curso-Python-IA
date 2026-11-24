from collections import Counter
import re

texto = "Los participantes en la gala, presidida por Salvador Illa, subrayan el papel de las emociones en la actividad creativa y la importancia de la cultura como instrumento de la proyección del país"
palabras = re.findall(r"\b\w+\b", texto.lower())

# 1. Comprobando si la clave ya existe
conteo_if = {}
for palabra in palabras:
	if palabra in conteo_if:
		conteo_if[palabra] += 1
	else:
		conteo_if[palabra] = 1

# 2. Usando get(clave, 0) + 1
conteo_get = {}
for palabra in palabras:
	conteo_get[palabra] = conteo_get.get(palabra, 0) + 1

# 3. Usando Counter
conteo_counter = Counter(palabras)

print(conteo_if)
print(conteo_get)
print(conteo_counter)
