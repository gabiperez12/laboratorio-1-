
import math

def analizar_pares_y_entropias(nombre_archivo):
    # 1) Leer archivo como texto
    f = open(nombre_archivo, "r", encoding="utf-8")
    texto = f.read()
    f.close()

    # -------------------------------
    # Distribución simple p(x)
    # -------------------------------
    conteo1 = {}
    total_simbolos = 0

    for c in texto:
        total_simbolos += 1
        if c in conteo1:
            conteo1[c] += 1
        else:
            conteo1[c] = 1

    # -------------------------------
    # Distribución conjunta p(x,y)
    # -------------------------------
    conteo2 = {}
    total_pares = 0

    for i in range(len(texto) - 1):
        par = (texto[i], texto[i+1])
        total_pares += 1

        if par in conteo2:
            conteo2[par] += 1
        else:
            conteo2[par] = 1

    # -------------------------------
    # Entropía simple H(X)
    # -------------------------------
    HX = 0.0
    for c in conteo1:
        p = conteo1[c] / total_simbolos
        HX -= p * math.log(p, 2)

    # -------------------------------
    # Entropía conjunta H(X,Y)
    # -------------------------------
    HXY = 0.0
    for par in conteo2:
        p = conteo2[par] / total_pares
        HXY -= p * math.log(p, 2)

    # -------------------------------
    # Entropía condicional e info mutua
    # -------------------------------
    HY_dado_X = HXY - HX
    IXY = 2 * HX - HXY

    # -------------------------------
    # OUTPUT
    # -------------------------------
    print("===================================")
    print("Archivo:", nombre_archivo)
    print("Total de caracteres:", total_simbolos)
    print("Total de pares de caracteres:", total_pares)
    print("Número de pares distintos:", len(conteo2))

    # Top 20 pares más frecuentes
    pares_ordenados = sorted(conteo2.items(), key=lambda x: x[1], reverse=True)

    print("\nTop 20 pares más frecuentes:")
    for i in range(20):
        (c1, c2), cantidad = pares_ordenados[i]
        p = cantidad / total_pares

        def etiqueta(c):
            if c == " ":
                return "<ESP>"
            elif c == "\n":
                return "<SALTO_LINEA>"
            elif c == "\t":
                return "<TAB>"
            else:
                return c

        print(f"{i+1:2d}. ({etiqueta(c1):>10s}, {etiqueta(c2):<10s})  "
              f"conteo={cantidad:6d}  p={p:.6f}")

    print("\nEntropías e información:")
    print(f"H(X)   = {HX:.6f} bits/símbolo")
    print(f"H(X,Y) = {HXY:.6f} bits/par")
    print(f"H(Y|X) = {HY_dado_X:.6f} bits/símbolo")
    print(f"I(X;Y) = {IXY:.6f} bits/símbolo")


# ------------ Ejecutar -------------
archivos = [
    r"C:\Users\U10145129\OneDrive - BASF\Desktop\texto_en.txt",
    r"C:\Users\U10145129\OneDrive - BASF\Desktop\texto_es.txt"
]

for archivo in archivos:
    analizar_pares_y_entropias(archivo)


# ------------------------------------------------------------
# Interpretación de los resultados
#
# A partir de la distribución conjunta empírica de pares de
# caracteres consecutivos se analizó la dependencia estadística
# entre símbolos adyacentes mediante la entropía conjunta,
# la entropía condicional y la información mutua.
#
# La información mutua I(X;Y) cuantifica cuánta información aporta
# conocer el carácter actual X sobre el carácter siguiente Y.
# Los resultados obtenidos muestran valores positivos y
# significativos en ambos textos, lo que indica que los caracteres
# consecutivos no son independientes.
#
# En el texto en inglés se obtuvo I(X;Y) ≈ 1.13 bits por símbolo,
# mientras que en el texto en español el valor fue mayor,
# I(X;Y) ≈ 1.33 bits por símbolo. Esto implica que conocer el
# carácter anterior reduce la incertidumbre sobre el siguiente
# en aproximadamente 1.13 bits en inglés y 1.33 bits en español.
#
# Esta reducción de la incertidumbre se observa también en la
# entropía condicional H(Y|X), que es menor que la entropía simple
# H(X) en ambos casos. Sin contexto, un carácter presenta una
# incertidumbre cercana a 4.2 bits; al conocer el carácter previo,
# dicha incertidumbre disminuye a aproximadamente 3.12 bits en
# inglés y 2.90 bits en español.
#
# La comparación entre idiomas muestra que la dependencia entre
# caracteres consecutivos es mayor en español que en inglés. Esto
# se refleja en una mayor información mutua y una menor entropía
# condicional en el texto en español. La causa principal de este
# comportamiento se atribuye a la mayor regularidad estructural
# del español, la alta frecuencia de terminaciones vocálicas y la
# abundancia de combinaciones de letras muy recurrentes (como
# “de”, “la”, “es”), lo que incrementa la redundancia del idioma.
#
# En conclusión, conocer el carácter anterior aporta información
# relevante sobre el siguiente en ambos idiomas, pero esta
# contribución es mayor en español, lo que indica una mayor
# previsibilidad y dependencia estadística entre caracteres
# consecutivos en dicho idioma.
# ------------------------------------------------------------
