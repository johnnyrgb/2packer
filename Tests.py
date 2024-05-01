import os
import random

for alphabet_size in [4, 16, 64, 128, 256, 512, 1024, 16384, 32768, 65536]:
    byte_set = set()
    while len(byte_set) < alphabet_size:
        byte_set.add(os.urandom(2))
    byte_list = list(byte_set)
    for file_size in range(100 * 1024, (1000 + 1) * 1024, 100 * 1024):
        with open(f"Tests/2Bytes/alphabet_{alphabet_size}_size_{file_size / 1024 * 2}kb.txt", "ab") as file:
            random_byte = b''
            for _ in range(0, file_size):
                byte_to_write = byte_list[random.randint(0, len(byte_set) - 1)]
                while byte_to_write == random_byte:
                    byte_to_write = byte_list[random.randint(0, len(byte_set) - 1)]
                file.write(byte_to_write)
