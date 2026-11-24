import pytest
from engine import document_part, MAX_BYTES, Analysis, usage
from types import SimpleNamespace

def test_text():
    assert document_part("sample.txt", b"Invoice total 100").text == "Invoice total 100"

@pytest.mark.parametrize("name,data", [
    ("a.exe", b"bad"), ("a.pdf", b"bad"), ("a.txt", b""),
    ("a.txt", b"\xff"), ("a.txt", b"a" * (MAX_BYTES+1)),
    ("a.txt", b"a" * 20001),
])
def test_invalid_input(name, data):
    with pytest.raises(ValueError):
        document_part(name, data)

def test_schema():
    result = Analysis(document_type="invoice", summary="Sample", key_facts=[], risks=[], recommended_actions=[], missing_information=[])
    assert result.document_type == "invoice"

def test_usage_missing():
    assert usage(SimpleNamespace(usage_metadata=None))["total_token_count"] is None
