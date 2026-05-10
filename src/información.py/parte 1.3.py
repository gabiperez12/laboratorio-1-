
import random
import math

# ------------------------------------------------------------
# Generación de un archivo binario de 100 KB
# Fuente DMS: p(0) = 0.9, p(1) = 0.1
# ------------------------------------------------------------

# Tamaño del archivo
tamano_bytes = 100 * 1024          # 100 KB
total_bits = tamano_bytes * 8      # bits totales

# Probabilidades DMS
p_cero = 0.9
p_uno = 0.1

# Lista para almacenar bits generados
bits = []

# 1) Generar bits según la DMS
for _ in range(total_bits):
    r = random.random()  # número uniforme en [0,1)
    if r < p_cero:
        bits.append(0)
    else:
        bits.append(1)

# 2) Convertir bits a bytes
bytes_salientes = bytearray()

for i in range(0, total_bits, 8):
    byte = 0
    for j in range(8):
        byte = (byte << 1) | bits[i + j]
    bytes_salientes.append(byte)

# 3) Escribir archivo binario DMS
nombre_archivo = r"C:\Users\U10145129\OneDrive - BASF\Desktop\fuente_DMS_100KB.bin"

f = open(nombre_archivo, "wb")
f.write(bytes_salientes)
f.close()

# 4) Mensaje final DMS
print("Archivo DMS generado correctamente.")
print("Nombre:", nombre_archivo)
print("Tamaño:", len(bytes_salientes), "bytes")
print("Probabilidades: p(0)=0.9, p(1)=0.1")


# ------------------------------------------------------------
# Generación de un segundo archivo binario de 100 KB
# Fuente de Markov de orden 1:
# P(0|0)=0.95, P(1|0)=0.05
# P(0|1)=0.30, P(1|1)=0.70
# ------------------------------------------------------------

# Probabilidades de transición
p0_dado_0 = 0.95
p1_dado_0 = 0.05
p0_dado_1 = 0.30
p1_dado_1 = 0.70

# Estado inicial (bit anterior). Se fija en 0 por simplicidad.
# (También podría inicializarse aleatoriamente; no cambia la idea del modelo.)
estado = 0

bits_markov = []

# 1) Generar bits según Markov de orden 1
for _ in range(total_bits):
    r = random.random()

    if estado == 0:
        # Si el estado actual es 0: usar P(0|0)
        if r < p0_dado_0:
            siguiente = 0
        else:
            siguiente = 1
    else:
        # Si el estado actual es 1: usar P(0|1)
        if r < p0_dado_1:
            siguiente = 0
        else:
            siguiente = 1

    bits_markov.append(siguiente)
    estado = siguiente  # actualizar estado

# 2) Convertir bits Markov a bytes
bytes_markov = bytearray()

for i in range(0, total_bits, 8):
    byte = 0
    for j in range(8):
        byte = (byte << 1) | bits_markov[i + j]
    bytes_markov.append(byte)

# 3) Escribir archivo binario Markov
nombre_archivo_markov = r"C:\Users\U10145129\OneDrive - BASF\Desktop\fuente_Markov_100KB.bin"

f = open(nombre_archivo_markov, "wb")
f.write(bytes_markov)
f.close()

# 4) Mensaje final Markov
print("\nArchivo Markov generado correctamente.")
print("Nombre:", nombre_archivo_markov)
print("Tamaño:", len(bytes_markov), "bytes")
print("Transiciones:")
print("P(0|0)=0.95, P(1|0)=0.05, P(0|1)=0.30, P(1|1)=0.70")

# ------------------------------------------------------------
# Cálculo de la entropía empírica H(X) de un archivo binario
# ------------------------------------------------------------
def entropia_empirica_binaria(nombre_archivo):
    f = open(nombre_archivo, "rb")
    datos = f.read()
    f.close()

    conteo = {0: 0, 1: 0}
    total_bits = 0

    for byte in datos:
        for i in range(8):
            bit = (byte >> (7 - i)) & 1
            conteo[bit] += 1
            total_bits += 1

    H = 0.0
    for bit in [0, 1]:
        if conteo[bit] > 0:
            p = conteo[bit] / total_bits
            H -= p * math.log(p, 2)

    return H, conteo, total_bits

# ------------------------------------------------------------
# Entropía condicional empírica H(X_n | X_{n-1})
# para una fuente binaria de Markov
# ------------------------------------------------------------
def entropia_condicional_markov(nombre_archivo):
    f = open(nombre_archivo, "rb")
    datos = f.read()
    f.close()

    # Extraer todos los bits
    bits = []
    for byte in datos:
        for i in range(8):
            bits.append((byte >> (7 - i)) & 1)

    # Conteo de transiciones
    trans = {
        (0, 0): 0,
        (0, 1): 0,
        (1, 0): 0,
        (1, 1): 0
    }

    conteo_prev = {0: 0, 1: 0}

    for i in range(len(bits) - 1):
        x = bits[i]
        y = bits[i + 1]
        trans[(x, y)] += 1
        conteo_prev[x] += 1

    # Cálculo de H(X_n | X_{n-1})
    H_cond = 0.0

    for x in [0, 1]:
        if conteo_prev[x] == 0:
            continue

        for y in [0, 1]:
            n_xy = trans[(x, y)]
            if n_xy > 0:
                p_xy = n_xy / (len(bits) - 1)
                p_y_given_x = n_xy / conteo_prev[x]
                H_cond -= p_xy * math.log(p_y_given_x, 2)

    return H_cond, trans



# ------------------------------------------------------------
# Evaluación de los archivos generados
# ------------------------------------------------------------

archivos = [
    (r"C:\Users\U10145129\OneDrive - BASF\Desktop\fuente_DMS_100KB.bin", "DMS"),
    (r"C:\Users\U10145129\OneDrive - BASF\Desktop\fuente_Markov_100KB.bin", "Markov")
]

for nombre, tipo in archivos:
    H_emp, conteo, total_bits = entropia_empirica_binaria(nombre)

    print("\n===================================")
    print("Archivo:", nombre)
    print("Total de bits:", total_bits)
    print("Conteo de bits:", conteo)
    print(f"Entropía empírica Ĥ(X) = {H_emp:.6f} bits/símbolo")

    if tipo == "DMS":
        H_teorica = -0.9 * math.log(0.9, 2) - 0.1 * math.log(0.1, 2)
        print(f"Entropía teórica DMS = {H_teorica:.6f} bits/símbolo")

    if tipo == "Markov":
        # Tasa de entropía teórica de la fuente de Markov
        pi0 = 0.3 / (0.3 + 0.05)
        pi1 = 1 - pi0

        H0 = -0.95 * math.log(0.95, 2) - 0.05 * math.log(0.05, 2)
        H1 = -0.3 * math.log(0.3, 2) - 0.7 * math.log(0.7, 2)

        H_teorica = pi0 * H0 + pi1 * H1
        print(f"Tasa de entropía teórica Markov = {H_teorica:.6f} bits/símbolo")

# ------------------------------------------------------------
# Comparación con tasa de entropía teórica de Markov
# ------------------------------------------------------------
H_emp_cond, trans = entropia_condicional_markov(
    r"C:\Users\U10145129\OneDrive - BASF\Desktop\fuente_Markov_100KB.bin"
)

# Tasa teórica
pi0 = 0.3 / (0.3 + 0.05)
pi1 = 1 - pi0

H0 = -0.95 * math.log(0.95, 2) - 0.05 * math.log(0.05, 2)
H1 = -0.3 * math.log(0.3, 2) - 0.7 * math.log(0.7, 2)

H_teorica = pi0 * H0 + pi1 * H1

print("\n--- Fuente de Markov ---")
print("Entropía condicional empírica Ĥ(X_n|X_{n-1}) =", round(H_emp_cond, 6))
print("Tasa de entropía teórica               =", round(H_teorica, 6))
print("Tabla de transiciones:", trans)
