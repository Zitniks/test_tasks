from pkg.utils.text import add_trademark


def test_add_trademark_six_letter_words():
    text = 'The visual description of the colliding files'
    result = add_trademark(text)
    assert 'visual™' in result
    assert 'description™' in result


def test_add_trademark_not_six_letters():
    text = 'The cat sat on mat'
    result = add_trademark(text)
    assert 'cat™' not in result
    assert 'sat™' not in result
    assert 'mat™' not in result


def test_add_trademark_mixed():
    text = 'Basically, each PDF contains a single large image'
    result = add_trademark(text)
    assert 'single™' in result
    assert 'large™' in result
    assert 'image™' in result


def test_add_trademark_preserves_punctuation():
    text = 'Hello, world!'
    result = add_trademark(text)
    assert ',' in result
    assert '!' in result
