import pytest
from app import base62


def test_decode_reverses_encode():
    number = 124533

    assert base62.decode_base62(base62.encode_base62(number)) == number

def test_encode_rejects_negative_number():
    number = -125
    with pytest.raises(ValueError, match="Negative values are not allowed"):
        base62.encode_base62(number)

def test_encode_rejects_non_integer_input():
    number = "133"
    with pytest.raises(TypeError, match="Input must be an integer"):
        base62.encode_base62(number)

def test_encode_rejects_boolean_input():
    number = True
    with pytest.raises(TypeError , match="Input must be an integer"):
        base62.encode_base62(number)

def test_encode_zero_returns_first_character():
    number = 0

    encoded_id = base62.encode_base62(number)

    assert encoded_id == "a"


def test_decode_rejects_invalid_string():
    encoded_id = "12#$%"


    with pytest.raises(
        ValueError,
        match=r"Invalid string.*entered",
    ):
        base62.decode_base62(encoded_id)

def test_decode_rejects_non_string_input():
    with pytest.raises(TypeError, match="Input must be a string"):
        base62.decode_base62(123)
