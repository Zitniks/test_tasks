from internal.proxy.processor import process_html


def test_process_html_adds_trademark():
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


def test_process_html_modifies_forms():
    html = '<html><body><form action="/submit"></form></body></html>'
    result = process_html(html, 'http://127.0.0.1:8232')
    assert 'action="http://127.0.0.1:8232/submit"' in result


def test_process_html_ignores_script_style():
    html = '<html><body><script>var visual = "test";</script></body></html>'
    result = process_html(html, 'http://127.0.0.1:8232')
    assert 'visual™' not in result
