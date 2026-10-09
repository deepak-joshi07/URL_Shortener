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
    with pytest.raises(ValueError, match="Input must be a integer"):
        base62.encode_base62(number)


def test_encode_rejects_value_greater_than_62bits():
    number = 2**62 + 1

    with pytest.raises(
        ValueError,
        match="Number exceeds the maximum allowable size of 62 bits.",
    ):
        base62.encode_base62(number)


def test_return_first_alpha():
    number = 0

    encoded_id = base62.encode_base62(number)

    assert encoded_id == "a"


def test_decode_rejects_invalid_value():
    encoded_id = "12#$%"


    with pytest.raises(
        ValueError,
        match=f"Invalid character.*Base62 string",
    ):
        base62.decode_base62(encoded_id)

