import gzip
import bz2
import lzma
import time

print("\n=== PARTE 5 - COMPARATIVA ===")

with open("texto_es.txt", "rb") as f:
    data = f.read()

original_size = len(data)

# ==============================
# HUFFMAN
# ==============================
start = time.perf_counter()

huff_compressed, codebook = huffman_encode(data)

huff_encode_time = time.perf_counter() - start

start = time.perf_counter()

huffman_decode(huff_compressed, codebook)

huff_decode_time = time.perf_counter() - start

# ==============================
# LZW
# ==============================
start = time.perf_counter()

codes = lzw_encode(data, max_dict_size=65536)
lzw_compressed = pack_codes(codes)

lzw_encode_time = time.perf_counter() - start

start = time.perf_counter()

lzw_decode(unpack_codes(lzw_compressed), 65536)

lzw_decode_time = time.perf_counter() - start

# ==============================
# GZIP
# ==============================
start = time.perf_counter()

gzip_compressed = gzip.compress(data)

gzip_encode_time = time.perf_counter() - start

start = time.perf_counter()

gzip.decompress(gzip_compressed)

gzip_decode_time = time.perf_counter() - start

# ==============================
# BZ2
# ==============================
start = time.perf_counter()

bz2_compressed = bz2.compress(data)

bz2_encode_time = time.perf_counter() - start

start = time.perf_counter()

bz2.decompress(bz2_compressed)

bz2_decode_time = time.perf_counter() - start

# ==============================
# LZMA
# ==============================
start = time.perf_counter()

lzma_compressed = lzma.compress(data)

lzma_encode_time = time.perf_counter() - start

start = time.perf_counter()

lzma.decompress(lzma_compressed)

lzma_decode_time = time.perf_counter() - start

# ==============================
# RESULTADOS
# ==============================
print("\nMétodo\t\tTamaño\tRatio\t\tCodif(s)\tDecodif(s)")

print(f"Huffman\t\t{len(huff_compressed)}\t{len(huff_compressed)/original_size:.4f}\t\t{huff_encode_time:.6f}\t{huff_decode_time:.6f}")

print(f"LZW\t\t{len(lzw_compressed)}\t{len(lzw_compressed)/original_size:.4f}\t\t{lzw_encode_time:.6f}\t{lzw_decode_time:.6f}")

print(f"gzip\t\t{len(gzip_compressed)}\t{len(gzip_compressed)/original_size:.4f}\t\t{gzip_encode_time:.6f}\t{gzip_decode_time:.6f}")

print(f"bz2\t\t{len(bz2_compressed)}\t{len(bz2_compressed)/original_size:.4f}\t\t{bz2_encode_time:.6f}\t{bz2_decode_time:.6f}")

print(f"lzma\t\t{len(lzma_compressed)}\t{len(lzma_compressed)/original_size:.4f}\t\t{lzma_encode_time:.6f}\t{lzma_decode_time:.6f}")
