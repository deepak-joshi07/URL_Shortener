ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
BASE = len(ALPHABET)


def encode_base62(number: int) -> str:
    if number == 0:
        return ALPHABET[0]

    arr = []

    while number > 0:
        number, rem = divmod(number, BASE)
        arr.append(ALPHABET[rem])

    return "".join(reversed(arr))


def decode_base62(st: str) -> int:
    result = 0

    for char in st:
        if char not in ALPHABET:
            raise ValueError(f"Invalid character '{char}' in Base62 string")

        result = result * BASE + ALPHABET.index(char)

    return result