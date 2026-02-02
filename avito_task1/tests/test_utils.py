"""Unit tests for pkg.utils.url."""

from pkg.utils.url import generate_short_code, validate_short_code, validate_url


def test_generate_short_code():
    code = generate_short_code()
    assert len(code) == 6
    assert code.isalnum()


def test_generate_short_code_custom_length():
    code = generate_short_code(10)
    assert len(code) == 10


def test_validate_url_valid():
    assert validate_url('https://www.example.com') is True


def test_validate_url_invalid_format():
    assert validate_url('not-a-url') is False
    assert validate_url('http://') is False
    assert validate_url('ftp://example.com') is False


def test_validate_short_code_valid():
    assert validate_short_code('abc123') is True
    assert validate_short_code('test-link') is True
    assert validate_short_code('test_link') is True
    assert validate_short_code('a' * 10) is True


def test_validate_short_code_invalid():
    assert validate_short_code('') is False
    assert validate_short_code('ab') is False
    assert validate_short_code('a' * 51) is False
    assert validate_short_code('test@link') is False
    assert validate_short_code('test link') is False
