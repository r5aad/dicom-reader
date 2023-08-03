from app.services.dicom_service import transform_from_hex_to_dec
import pytest

def test_transform_to_hex():
    tag_str = "0010,0010"
    expected_result = (16, 16)
    assert transform_from_hex_to_dec(tag_str) == expected_result

    tag_str = "0008,0020"
    expected_result = (8, 32)
    assert transform_from_hex_to_dec(tag_str) == expected_result

    tag_str = "0018,A004"
    expected_result = (24, 40964)
    assert transform_from_hex_to_dec(tag_str) == expected_result

    tag_str = "0020,000e"
    expected_result = (32, 14)
    assert transform_from_hex_to_dec(tag_str) == expected_result

    tag_str = "00100010"
    with pytest.raises(ValueError):
        transform_from_hex_to_dec(tag_str)

    tag_str = "0010,00G0"
    with pytest.raises(ValueError):
        transform_from_hex_to_dec(tag_str)
