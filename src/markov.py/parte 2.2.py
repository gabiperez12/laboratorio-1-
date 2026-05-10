
import math
import matplotlib.pyplot as plt

# 2.2
# ------------------------------------------------------------
# Funciones auxiliares
# ------------------------------------------------------------

def leer_texto(ruta):
    f = open(ruta, "r", encoding="utf-8")
    texto = f.read()
    f.close()
    return texto

def estimar_transiciones(texto, k):
    conteo_contexto = {}      # contexto -> total
    conteo_ctx_sig = {}       # contexto -> {simbolo -> conteo}

    n = len(texto)

    for i in range(n - k):
        if k == 0:
            contexto = ""
            siguiente = texto[i]
        else:
            contexto = texto[i:i+k]
            siguiente = texto[i+k]

        conteo_contexto[contexto] = conteo_contexto.get(contexto, 0) + 1

        if contexto not in conteo_ctx_sig:
            conteo_ctx_sig[contexto] = {}
        conteo_ctx_sig[contexto][siguiente] = (
            conteo_ctx_sig[contexto].get(siguiente, 0) + 1
        )

    return conteo_contexto, conteo_ctx_sig

def tasa_entropia_empirica(conteo_contexto, conteo_ctx_sig):
    total = sum(conteo_contexto.values())
    Hk = 0.0

    for c in conteo_contexto:
        Nc = conteo_contexto[c]
        pc = Nc / total

        H_local = 0.0
        for x in conteo_ctx_sig[c]:
            Ncx = conteo_ctx_sig[c][x]
            p = Ncx / Nc
            H_local -= p * math.log(p, 2)

        Hk += pc * H_local

    return Hk

# ------------------------------------------------------------
# Cálculo de H_k para ambos idiomas
# ------------------------------------------------------------

archivo_en = r"C:\Users\U10145129\OneDrive - BASF\Desktop\texto_en.txt"
archivo_es = r"C:\Users\U10145129\OneDrive - BASF\Desktop\texto_es.txt"

texto_en = leer_texto(archivo_en)
texto_es = leer_texto(archivo_es)

ks = [0, 1, 2, 3, 4]

H_en = []
H_es = []

for k in ks:
    c_en, cs_en = estimar_transiciones(texto_en, k)
    c_es, cs_es = estimar_transiciones(texto_es, k)

    H_en.append(tasa_entropia_empirica(c_en, cs_en))
    H_es.append(tasa_entropia_empirica(c_es, cs_es))

# ------------------------------------------------------------
# Gráfico
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))
plt.plot(ks, H_en, marker='o', linewidth=2, label='Inglés')
plt.plot(ks, H_es, marker='s', linewidth=2, label='Español')

plt.xlabel("Orden del modelo k")
plt.ylabel("Tasa de entropía empírica  Ĥₖ  (bits/símbolo)")
plt.title("Tasa de entropía empírica vs orden del modelo de Markov")
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()

plt.tight_layout()
plt.show()

#b)
#A partir de las tasas de entropía empíricas estimadas para k=0,1,2,3,4k = 0,1,2,3,4k=0,1,2,3,4 se verifica que la sucesión H_0≥H_1≥H_2≥...
# es no creciente tanto para el texto en inglés como para el texto en español. Esta propiedad se observa directamente en los valores numéricos obtenidos
# y se confirma visualmente en el gráfico correspondiente. El resultado es consistente con la teoría de la información, ya que el aumento del contexto reduce
# la incertidumbre promedio del siguiente símbolo.


#c)
#La tasa de entropía empírica decrece más rápidamente en el texto en inglés que en el español conforme aumenta el orden del modelo de Markov.
# Esto indica que, en inglés, el uso de contextos relativamente cortos es suficiente para reducir fuertemente la incertidumbre del siguiente carácter, 
# debido a la alta frecuencia de patrones lingüísticos muy repetitivos. En contraste, el español, aunque presenta mayor previsibilidad para contextos cortos, 
# mantiene una mayor variabilidad en órdenes altos, reflejando una estructura morfológica más rica y diversa. En conjunto, los resultados evidencian diferencias 
# fundamentales en la organización estadística de ambos idiomas.
