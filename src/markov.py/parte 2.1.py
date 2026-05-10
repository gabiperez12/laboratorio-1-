
import math

# ------------------------------------------------------------
# Estimar transiciones empíricas Markov orden k sobre caracteres
# y calcular tasa de entropía empírica H_k
# k = 0,1,2,3,4
# ------------------------------------------------------------

def leer_texto(ruta):
    f = open(ruta, "r", encoding="utf-8")
    texto = f.read()
    f.close()
    return texto

def etiqueta_simbolo(c):
    if c == " ":
        return "<ESP>"
    if c == "\n":
        return "<SALTO_LINEA>"
    if c == "\t":
        return "<TAB>"
    return c

def estimar_transiciones(texto, k):
    # Alfabeto empírico
    alfabeto = sorted(set(texto))

    conteo_contexto = {}      # contexto -> total apariciones
    conteo_ctx_sig = {}       # contexto -> {simbolo -> conteo}

    n = len(texto)
    # número de predicciones hechas = n-k (si k=0 es n)
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
        conteo_ctx_sig[contexto][siguiente] = conteo_ctx_sig[contexto].get(siguiente, 0) + 1

    return alfabeto, conteo_contexto, conteo_ctx_sig

def top_contextos(conteo_contexto, top=10):
    items = list(conteo_contexto.items())
    items.sort(key=lambda x: x[1], reverse=True)
    return items[:top]

def tasa_entropia_empirica(conteo_contexto, conteo_ctx_sig):
    """
    H_k = - sum_c p(c) sum_x p(x|c) log2 p(x|c)
    con:
      p(c) = N(c) / N_total
      p(x|c) = N(c,x) / N(c)
    """
    # Total de contextos (total de predicciones)
    total = 0
    for c in conteo_contexto:
        total += conteo_contexto[c]

    Hk = 0.0

    for c in conteo_contexto:
        Nc = conteo_contexto[c]
        pc = Nc / total

        # Entropía condicional local para este contexto: H(X|c)
        H_local = 0.0

        # iterar solo símbolos observados dado el contexto
        for x in conteo_ctx_sig[c]:
            Ncx = conteo_ctx_sig[c][x]
            px_dado_c = Ncx / Nc
            H_local -= px_dado_c * math.log(px_dado_c, 2)

        # ponderar por p(c)
        Hk += pc * H_local

    return Hk

# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
archivos = [
    r"C:\Users\U10145129\OneDrive - BASF\Desktop\texto_en.txt",
    r"C:\Users\U10145129\OneDrive - BASF\Desktop\texto_es.txt"
]

ks = [0, 1, 2, 3, 4]

for ruta in archivos:
    texto = leer_texto(ruta)

    print("===================================")
    print("Archivo:", ruta)
    print("Total de caracteres:", len(texto))

    for k in ks:
        alfabeto, conteo_contexto, conteo_ctx_sig = estimar_transiciones(texto, k)
        Hk = tasa_entropia_empirica(conteo_contexto, conteo_ctx_sig)

        print("\n--- Orden k =", k, "---")
        print("Tamaño del alfabeto:", len(alfabeto))
        print("Contextos distintos:", len(conteo_contexto))
        print(f"Tasa de entropía empírica H_{k} = {Hk:.6f} bits/símbolo")

        top = top_contextos(conteo_contexto, top=10)
        print("Top 10 contextos más frecuentes (contexto, conteo):")
        for ctx, c in top:
            if k == 0:
                ctx_print = "<VACIO>"
            else:
                ctx_print = "".join(etiqueta_simbolo(ch) for ch in ctx)
            print(" ", repr(ctx_print), c)
