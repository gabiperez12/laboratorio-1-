
import math
import matplotlib.pyplot as plt
# Distribución empírica y entropía, a nivel de bytes (0..255)
def distribucion_empirica_bytes(nombre_archivo):
    # 1) Leer el archivo como bytes
    f = open(nombre_archivo, "rb")
    datos = f.read()
    f.close()

    # 2) Inicializar conteo para los 256 bytes posibles
    conteo = {}
    for b in range(256):
        conteo[b] = 0

    # 3) Contar byte a byte
    total = 0
    for b in datos:
        total = total + 1
        conteo[b] = conteo[b] + 1

    # 4) Probabilidades empíricas
    prob = {}
    for b in range(256):
        prob[b] = conteo[b] / total

    # 5) Entropía empírica H(X)
    H = 0.0
    for b in range(256):
        p = prob[b]
        if p > 0:
            H = H - p * math.log(p, 2)

    return total, conteo, prob, H


# Etiqueta legible para algunos bytes comunes (solo para mostrar/plotear mejor)
def etiqueta_byte(b):
    if b == 32:
        return "ESP"
    elif b == 10:
        return "\\n"
    elif b == 9:
        return "\\t"
    elif 32 <= b <= 126:
        return chr(b)  # ASCII imprimible
    else:
        return str(b)  # para bytes no imprimibles / UTF-8 multibyte


# (c) Histograma de frecuencias de los 20 bytes más frecuentes
def graficar_top20(conteo, archivo):
    # 1) Convertir diccionario a lista de pares (byte, conteo)
    pares = []
    for b in range(256):
        pares.append((b, conteo[b]))

    # 2) Ordenar por conteo descendente
    pares_ordenados = sorted(pares, key=lambda x: x[1], reverse=True)

    # 3) Tomar los 20 primeros
    top20 = pares_ordenados[:20]

    # 4) Separar para graficar
    x_labels = []
    y_freq = []
    for (b, c) in top20:
        x_labels.append(etiqueta_byte(b))
        y_freq.append(c)

    # 5) Graficar (barras)
    plt.figure(figsize=(10, 5))
    plt.bar(x_labels, y_freq)

    plt.title("Top 20 bytes más frecuentes\n" + archivo)
    plt.xlabel("Byte (etiqueta)")
    plt.ylabel("Frecuencia (conteo)")

    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.show()


# --- Ejecutar para cada archivo ---
archivos = [
    r"C:\Users\U10145129\OneDrive - BASF\Desktop\texto_en.txt",
    r"C:\Users\U10145129\OneDrive - BASF\Desktop\texto_es.txt"
]

for archivo in archivos:
    total, conteo, prob, H = distribucion_empirica_bytes(archivo)

    # Contar cuántos bytes distintos aparecen
    distintos = 0
    for b in range(256):
        if conteo[b] > 0:
            distintos = distintos + 1

    print("===================================")
    print("Archivo:", archivo)
    print("Total de bytes:", total)
    print("Símbolos posibles:", 256)
    print("Símbolos distintos (bytes con conteo>0):", distintos)

    print(f"Entropía empírica H(X) = {H} bits/byte")

    # Top 20 bytes más probables (opcional: para ver en consola)
    ordenados = sorted(prob.items(), key=lambda x: x[1], reverse=True)
    print("\nTop 20 bytes más probables:")
    for i in range(20):
        b = ordenados[i][0]
        p = ordenados[i][1]
        print(f"{i+1:2d}. byte={b:3d} ({etiqueta_byte(b):>3s})  conteo={conteo[b]:6d}  p={p:.6f}")

    # (c) Graficar histograma top 20
    graficar_top20(conteo, archivo)
