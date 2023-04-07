import project1.main as project1

def test_unicode_char():
    word = '6 APRIL 1995'
    result = '\u2588' + ' ' + '\u2588\u2588\u2588\u2588\u2588' + ' ' + '\u2588\u2588\u2588\u2588'
    expected = project1.unicodeChar(word)
    assert expected == result