"""Тесты обработки HTML: ™, ссылки, формы."""

from internal.proxy.processor import process_html


def test_process_html_adds_trademark():
    """Слова из 6 букв получают ™."""
    html = '<html><body><p>The visual description</p></body></html>'
    result = process_html(html, 'http://127.0.0.1:8232')
    assert 'visual™' in result
    assert 'description™' in result


def test_process_html_modifies_links():
    html = '<html><body><a href="/item?id=123">Link</a></body></html>'
    result = process_html(html, 'http://127.0.0.1:8232')
    assert 'href="http://127.0.0.1:8232/item?id=123"' in result


def test_process_html_modifies_full_urls():
    html = '<html><body><a href="https://news.ycombinator.com/item?id=123">Link</a></body></html>'
    result = process_html(html, 'http://127.0.0.1:8232')
    assert 'href="http://127.0.0.1:8232/item?id=123"' in result


def test_process_html_does_not_rewrite_fake_hn_domain():
    """Ссылки на поддельный хост (news.ycombinator.com.evil.com) не переписываются."""
    html = '<html><body><a href="https://news.ycombinator.com.evil.com/item">Link</a></body></html>'
    result = process_html(html, 'http://127.0.0.1:8232')
    assert 'https://news.ycombinator.com.evil.com/item' in result


def test_process_html_modifies_forms():
    html = '<html><body><form action="/submit"></form></body></html>'
    result = process_html(html, 'http://127.0.0.1:8232')
    assert 'action="http://127.0.0.1:8232/submit"' in result


def test_process_html_ignores_script_style():
    html = '<html><body><script>var visual = "test";</script></body></html>'
    result = process_html(html, 'http://127.0.0.1:8232')
    assert 'visual™' not in result


def test_process_html_empty_string_unchanged():
    """Пустой или только пробельный HTML возвращается без изменений."""
    assert process_html("", "http://127.0.0.1:8232") == ""
    assert process_html("   ", "http://127.0.0.1:8232") == "   "


def test_process_html_form_full_url_with_trailing_slash_base():
    """Форма с полным URL HN переписывается при любом формате base (с/без слэша)."""
    html = '<html><body><form action="https://news.ycombinator.com/submit">X</form></body></html>'
    result = process_html(html, "http://127.0.0.1:8232")
    assert 'action="http://127.0.0.1:8232/submit"' in result
