ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
BASE = len(ALPHABET)


def encode_base62(number: int) -> str:
    if isinstance(number, bool) or not isinstance(number, int):
        raise TypeError("Input must be an integer")

    if number < 0:
        raise ValueError("Negative values are not allowed")
    

    
    if number == 0:
        return ALPHABET[0]
    

    arr = []

    while number > 0:
        number, rem = divmod(number, BASE)
        arr.append(ALPHABET[rem])

    return "".join(reversed(arr))


def decode_base62(st: str) -> int:
    if not isinstance(st , str):
        raise TypeError("Input must be a string")

    if not st: 
        raise ValueError("Base62 string cannot be empty")
    
    result = 0

    for char in st:
        if char not in ALPHABET:
            raise ValueError(f"Invalid string '{st}' entered")

        result = result * BASE + ALPHABET.index(char)

    return result