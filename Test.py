num = int("11100111"[::-1], 2)

b = bytearray()

b += num.to_bytes(1, "little")

print(b)