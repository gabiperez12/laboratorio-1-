import struct
!pip install bitarray
# ------------------------------
# LZW ENCODE
# ------------------------------
def lzw_encode(data: bytes, max_dict_size: int = 65536) -> list[int]:
    dictionary = {bytes([i]): i for i in range(256)}
    dict_size = 256

    w = b""
    output_codes = []

    for byte in data:
        c = bytes([byte])
        wc = w + c

        if wc in dictionary:
            w = wc
        else:
            output_codes.append(dictionary[w])
            if dict_size < max_dict_size:
                dictionary[wc] = dict_size
                dict_size += 1
            w = c

    if w:
        output_codes.append(dictionary[w])

    return output_codes


# ------------------------------
# LZW DECODE
# ------------------------------
def lzw_decode(compressed: list[int], max_dict_size: int = 65536) -> bytes:
    dictionary = {i: bytes([i]) for i in range(256)}
    dict_size = 256

    w = dictionary[compressed[0]]
    result = bytearray(w)

    for k in compressed[1:]:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            # CASO CRÍTICO
            entry = w + w[:1]
        else:
            raise ValueError("Código inválido en LZW")

        result.extend(entry)

        if dict_size < max_dict_size:
            dictionary[dict_size] = w + entry[:1]
            dict_size += 1

        w = entry

    return bytes(result)


# ------------------------------
# PACK / UNPACK (16 bits por código)
# ------------------------------
def pack_codes(codes):
    return b''.join(struct.pack('>H', c) for c in codes)

def unpack_codes(data):
    return [struct.unpack('>H', data[i:i+2])[0]
            for i in range(0, len(data), 2)]


# ==============================
# TEST CON EJEMPLO
# ==============================
print("=== TEST CON EJEMPLO ===")
data = b"ABABABAABABA"

codes = lzw_encode(data)
compressed = pack_codes(codes)

decoded_codes = unpack_codes(compressed)
recovered = lzw_decode(decoded_codes)

print("Original:", data)
print("Recuperado:", recovered)
print("Iguales:", recovered == data)

print("Tamaño original:", len(data))
print("Tamaño comprimido:", len(compressed))
print("Ratio:", len(compressed) / len(data))


# ==============================
# TEST CON ARCHIVO .txt
# ==============================
print("\n=== TEST CON ARCHIVO ===")

try:
    with open("texto_es.txt", "rb") as f:
        data = f.read()

    codes = lzw_encode(data)
    compressed = pack_codes(codes)
    recovered = lzw_decode(unpack_codes(compressed))

    print("Reconstrucción correcta:", recovered == data)
    print("Original:", len(data), "bytes")
    print("Comprimido:", len(compressed), "bytes")
    print("Ratio:", len(compressed) / len(data))

# ==============================
#  2 TAMAÑOS DIFERENTES DE DICCIONARIOS
# ==============================
    for size in [4096, 65536]:
        codes = lzw_encode(data, max_dict_size=size)
        compressed = pack_codes(codes)
        recovered = lzw_decode(unpack_codes(compressed), max_dict_size=size)

        print(f"\nDiccionario: {size}")
        print("Reconstrucción correcta:", recovered == data)
        print("Original:", len(data))
        print("Comprimido:", len(compressed))
        print("Ratio:", len(compressed)/len(data))
    #--

except FileNotFoundError:
    print("No se ha encontrado archivo 'texto_es.txt'")


    #------

# ==============================
# HUFFMAN + COMPARACIÓN CON LZW
# ==============================

import heapq
from collections import Counter
from bitarray import bitarray


# ------------------------------
# Nodo de Huffman
# ------------------------------
class HuffmanNode:
    def __init__(self, freq, symbol=None, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


# ------------------------------
# Construir árbol
# ------------------------------
def huffman_tree(frequencies):
    heap = [HuffmanNode(freq, symbol=sym) for sym, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = HuffmanNode(n1.freq + n2.freq, left=n1, right=n2)
        heapq.heappush(heap, merged)

    return heap[0]


# ------------------------------
# Generar códigos
# ------------------------------
def build_codes(node, prefix="", codebook={}):
    if node.symbol is not None:
        codebook[node.symbol] = prefix
    else:
        build_codes(node.left, prefix + "0", codebook)
        build_codes(node.right, prefix + "1", codebook)
    return codebook


# ------------------------------
# Codificar
# ------------------------------
def huffman_encode(data: bytes):
    freq = Counter(data)
    tree = huffman_tree(freq)
    codebook = build_codes(tree, "", {})

    bits = bitarray()
    for b in data:
        bits.extend(codebook[b])

    return bits.tobytes(), codebook


# ------------------------------
# Decodificar
# ------------------------------
def huffman_decode(compressed: bytes, codebook: dict):
    reverse = {v: k for k, v in codebook.items()}

    bits = bitarray()
    bits.frombytes(compressed)

    decoded = bytearray()
    current = ""

    for bit in bits.to01():
        current += bit
        if current in reverse:
            decoded.append(reverse[current])
            current = ""

    return bytes(decoded)


# ==============================
# COMPARACIÓN LZW vs HUFFMAN
# ==============================

print("\n=== COMPARACIÓN LZW vs HUFFMAN ===")

with open("texto_es.txt", "rb") as f:
    data = f.read()

# ----- LZW (usamos el mejor caso: 65536) -----
codes = lzw_encode(data, max_dict_size=65536)
lzw_compressed = pack_codes(codes)
lzw_ratio = len(lzw_compressed) / len(data)

# ----- HUFFMAN -----
huff_compressed, codebook = huffman_encode(data)
huff_decoded = huffman_decode(huff_compressed, codebook)
huff_ratio = len(huff_compressed) / len(data)

# ==============================
# RESULTADOS
# ==============================
print("\n--- LZW ---")
print("Correcto:", lzw_decode(unpack_codes(lzw_compressed), 65536) == data)
print("Tamaño:", len(lzw_compressed))
print("Ratio:", lzw_ratio)

print("\n--- HUFFMAN ---")
print("Correcto:", huff_decoded == data)
print("Tamaño:", len(huff_compressed))
print("Ratio:", huff_ratio)
